# Long Form Builder

**A production system for long-form static advertising, built on measurement instead of taste.**

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](./LICENSE)
[![Format](https://img.shields.io/badge/format-long%20form%20static-blue.svg)](#what-long-form-static-is)
[![Status](https://img.shields.io/badge/status-production-green.svg)](#)

---

> **The one-sentence version.** Long Form Builder turns a round of advertising tests into a controlled experiment: one angle per batch, one awareness level per column, one variable in the image, and a set of hard rules derived from classifying 199 live ads so that nobody on the team has to argue about tone again.

---

## Table of contents

- [Why this exists](#why-this-exists)
- [What long form static is](#what-long-form-static-is)
- [The finding that shaped the system](#the-finding-that-shaped-the-system)
- [Architecture](#architecture)
- [The six phases](#the-six-phases)
- [The knowledge base](#the-knowledge-base)
- [The production locks](#the-production-locks)
- [The prose layer](#the-prose-layer)
- [Scripts](#scripts)
- [Installation](#installation)
- [Usage](#usage)
- [Output contract](#output-contract)
- [What this is not](#what-this-is-not)
- [Provenance of the numbers](#provenance-of-the-numbers)
- [License](#license)
- [Versão em português](#versão-em-português)

---

## Why this exists

Most creative teams produce ads the way a kitchen produces dinner: somebody has an idea, somebody writes it, somebody argues about the tone, and it ships. Then the numbers come back and nobody can say which decision caused which result, because forty things changed at once.

The result is an operation that spends real money and, at the end of a quarter, still cannot answer the only question that matters: **which angle converts?**

This system exists because that question is answerable, and answering it is cheap if you design the test correctly before you write a single word.

Three problems it fixes, in order of how much money they waste:

1. **Untestable rounds.** If angle, awareness level, format, offer and destination all vary at once, the round produces anecdotes. This system isolates two variables and locks everything else.
2. **Rules by opinion.** "Long copy is better." "Never be explicit." "Always show the product early." Every one of these is testable, several of them are wrong, and this system replaces them with measured locks that carry their source number.
3. **Winning the wrong lesson.** The single most expensive error observed in the source account: reading an asset's performance as a property of its *label*, and asking somebody to rewrite the label. See below.

---

## What long form static is

A static image on Meta, plus long-form copy in the primary text field.

```
[ Page name ]  ·  Sponsored
{PRIMARY TEXT — only the first ~3 lines are visible}  ... See more
┌────────────────────────────┐
│                            │
│        IMAGE  1:1          │   ← this is the hook
│                            │
└────────────────────────────┘
DOMAIN.COM
{LINK HEADLINE}                       [ CTA BUTTON ]
{LINK DESCRIPTION}
```

Three properties make the format worth building a system around:

- **The image is the hook, not an illustration.** Its only job is to stop the scroll and buy the click on "see more". It does not sell, it does not show the product, it carries no text.
- **The copy carries the angle.** In a measured sweep of 68 live long-form ads from a competitor in the same vertical, the **median primary text was 10,809 characters**, 72% ran above 8,000, and the highest-volume advertiser in the set ran a median of **14,984**. Only 3% ran under 2,500.
- **It is the cheapest way to validate an angle.** Whatever wins here becomes video and advertorial later. Losing here costs a hundred dollars and a day.

---

## The finding that shaped the system

In the source account, one angle looked like a clear champion: ROAS 0.523 across 222 sales.

Then it was cut by period.

| Cut | ROAS | Sales | Tests |
|---|---|---|---|
| Whole set, video | 0.523 | 222 | 10 |
| **Excluding the launch month** | **0.281** | 18 | 8 |
| Launch month only | 0.572 | 204 | **2** |

The angle produced 204 sales in **two** tests during one month, and 18 sales in **eight** tests across the four months after. The operation had read the result as a property of the angle, handed the label to writers, and asked for eight rewrites. Each rewrite lost roughly half the ROAS.

What performed was **that execution**: that copy, that image, that cast. Not the name on top of it.

This produced the rule that governs the whole system:

> ### Do not repeat the label. Repeat the asset.
>
> When a batch wins, what scales is that specific copy paired with that specific image. An angle name handed to another writer is not the winning asset. It is a description of the winning asset, and descriptions do not convert.

A second correction came from the same analysis and is equally counterintuitive:

> **Hook rate is not monotonic. Hold rate is.** In the source set, the highest hook-rate band converted *worse* than the middle band, while hold rate rose cleanly across all four bands (ROAS 0.319 → 0.271 → 0.536 → 0.570). Translated to static: **a high CTR on the image is not a winner signal.** Do not promote a batch on click-through.

---

## Architecture

```
                    ┌─────────────────────────────┐
                    │      round definition       │
                    │  angles, avatars, mechanism │  ← human input, per round
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────▼──────────────────────────┐
        │                     THE MATRIX                      │
        │      N angles  ×  M awareness levels  =  cells      │
        │      each cell = 1 batch = 1 copy + K images        │
        └──────────────────────────┬──────────────────────────┘
                                   │
     ┌─────────────┬───────────────┼───────────────┬─────────────┐
     ▼             ▼               ▼               ▼             ▼
 ┌────────┐  ┌──────────┐   ┌───────────┐   ┌──────────┐  ┌──────────┐
 │ method │  │  locks   │   │  anatomy  │   │  prose   │  │ casting  │
 │ stable │  │ measured │   │16 moves   │   │15 devices│  │  rules   │
 └────────┘  └──────────┘   └───────────┘   └──────────┘  └──────────┘
     │             │               │               │             │
     └─────────────┴───────────────┼───────────────┴─────────────┘
                                   ▼
                        ┌──────────────────────┐
                        │   automated gate     │  ← blocks on violation
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │  delivery + upload   │
                        │  docx + sheet + PNG  │
                        └──────────────────────┘
```

The separation that matters most: **method is stable, round is not.**

- `knowledge/method-batches.md` — how a batch works, signal floors, budget, how to read results. Changes rarely.
- `knowledge/rounds/<ID>.md` — the angles, avatars and mechanism of *this* test. Changes every round.

Angles are a business decision and come from the operator each round. They are never inherited from the previous round by inertia, and never taken from a competitor swipe. Competitor material calibrates **length, rhythm and format**. It does not choose angles.

---

## The six phases

| # | Phase | Produces | Gate |
|---|---|---|---|
| 0 | **Onboarding** | round file, folder, locked offer data | offer must be documented before writing |
| 1 | **Matrix** | `matrix.md`, `tracking/batches.json` | columns must be structurally distinct |
| 2 | **Copy** | one `.md` per batch | length band per angle |
| 3 | **Quality gate** | `gate-report.md` | **blocking** — see below |
| 4 | **Hook and image brief** | `image-brief.md` | hook concepts qualified first |
| 5 | **Generation** | named PNGs, in each cell's folder | 1:1 verified, scene replicated |
| 6 | **Delivery** | two `.docx` per batch (copy + INFOS) + upload sheet | five placement fields present |

### Phase 3 is not optional

The gate runs automatically over every draft and **blocks** on the two violations that cannot be fixed downstream: forbidden punctuation in ad copy, and "trick / secret / hack" vocabulary, which was the worst-performing group in the entire source set.

It also runs six checks that only a human catches, the sharpest being:

**The swap test.** Take the first three lines of the three cells of one angle. If they can be swapped between cells without anything sounding wrong, the awareness columns are not differentiated and the round will measure nothing. The row fails and goes back to Phase 2.

### Phase 4 treats the image as a hook

Because in this format it is one. The phase calls a dedicated hook-generation process before any image prompt is written, so the scene comes from a qualified hook concept rather than from visual taste. Verbal hook archetypes translate to scene:

| Hook archetype | Becomes |
|---|---|
| Ouch factor | the scene the reader recognizes and wishes he did not |
| Open loop | the scene that does not explain itself |
| Contrarian | the scene that contradicts the expectation |
| Bold statement | the object that carries the claim |
| Curiosity | the detail that is out of place |

---

## The knowledge base

| File | What it settles |
|---|---|
| `method-batches.md` | What a batch is, awareness levels, length, budget, signal floors, how to read the result |
| `production-locks.md` | Twelve measured rules, each carrying its source number |
| `longform-anatomy.md` | The sixteen recurring movements of copy that scales |
| `persuasive-prose.md` | Fifteen sentence-level devices, from the rule of three to the closing construction |
| `casting-longform.md` | Avatar rules for this format, and why they supersede the short-form standard |
| `meta-placement.md` | The five fields of the ad and their character limits |
| `publishing-profiles.md` | Why first-person copy cannot run from a brand page, and how profiles map to POV |
| `xquad-routing.md` | Which copywriting voice handles which angle and which block |
| `rounds/_TEMPLATE.md` | The per-round file to fill in |

---

## The production locks

Twelve rules. Each survived a control that excluded the best-performing month and a control restricted to a single product, which is what separates a finding from a coincidence.

| # | Lock | Evidence |
|---|---|---|
| 1 | **Three proof modalities per copy** | 0.427 vs 0.192 with two. The most robust finding in the set, over 100% difference |
| 2 | **Name the product** | 0.411 vs 0.177 when the name is withheld for curiosity |
| 3 | **Product explicit and late. No trick vocabulary** | 0.416 late vs 0.322 early. Trick framing: **0.195**, worst group in the set |
| 4 | **Turn narrative, not direct pitch** | 0.417 vs 0.345 |
| 5 | **The villain is biology** | 0.447 vs 0.317 for a doctor or system villain |
| 6 | **Price in dollars, written** | 0.543 with a dollar figure, 0.355 with none, 0.246 with per-day framing |
| 7 | **Explicit register, moderate aggression** | Explicit language wins in both languages tested. The aggressive *package* loses: conspiracy, fabricated scarcity, unnamed product |
| 8 | **Direct-purchase CTA** | 0.412 vs 0.191 |
| 9 | **Third-party validation** | The result is never declared by the narrator about himself. Present in nearly every winner |
| 10 | **Lab number, always specific** | Sustains the contradiction between a normal report and a broken life |
| 11 | **No em dashes, no quotation marks** | House rule for ad copy output |
| 12 | **First three lines carry the fold** | 200 to 400 characters, a closed block that raises the question without answering it |

And one hypothesis deliberately left unlocked, because it contradicts standard practice and deserves its own cell rather than a policy change: **mentioning a 30-day guarantee outperformed 90 days, 0.486 to 0.296, within the same product.** The suspicion is that "90 days" is heard as "takes 90 days to work".

### Absence is also information

Across 199 classified ads in the source account, four things never appeared: **personal-authority proof** (a narrator with their own credential), **investigative editorial format**, **listicle format**, and **personal letter**. The first is now the highest-expected-value test in the system, precisely because it was never run.

---

## The prose layer

Locks say what the copy must contain. Anatomy says in what order. The prose layer says **how the sentence sounds**, which is what decides whether an 11,000-character post is read to the end or abandoned at the third block.

Fifteen devices, of which the three that carry the most weight:

**The rule of three.** Two reads as coincidence. Four reads as a list. Three reads as a pattern, and a pattern reads as truth. Used in three forms: triad of symptom (three concrete consequences), triad of escalation (each worse than the last), triad of absolution (three denials that remove blame). The common failure is the triad of synonymous adjectives, which is one idea repeated three times and fools nobody.

**Sentence length variation.** Never three consecutive sentences of the same length. After two or three long ones, a sentence of three words. The short cut after accumulation is where the reader breathes, and where he decides to continue.

**Concrete over abstract.** Do not describe the emotion, describe what produces it. Not *the room felt cold and distant*, but *the sheet on his side was smooth. Not even creased.*

---

## Scripts

Three, all tested, all dependency-light.

### `check_locks.py`
The automatic half of the gate. Parses drafts and verifies what is verifiable in text: punctuation, product position, price presence, lab number, opening-block length, enemy block completeness, placement field lengths, length band.

```bash
python scripts/check_locks.py drafts/ --product "PRODUCT NAME"
# exits 1 if any batch is blocked
```

### `build_batch_docx.py`
Builds the two delivery documents per batch and the upload sheet for the round.

- **Copy document**, saved in the cell's folder next to its three images: literally only the copy, the primary text followed by the first three lines. No title, angle, headline or CTA; it is the file that goes to whoever uploads the ad.
- **INFOS document**, saved in `infos/` at the test root: angle, awareness level label, and the locked scene plus the full prompt of each image, read from `image-brief.md`.

Headline, description and CTA live only in the upload sheet.

Both documents are formatted to a strict typographic standard: single font throughout, body at 12pt, 1.5 line spacing, black only, headings in caps and bold, fixed margins.

```bash
python scripts/build_batch_docx.py --folder drafts/ --test T101 --product BRAND-SKU
python scripts/build_batch_docx.py --sheet --folder drafts/ --destination "https://..." --out upload.csv
```

The upload sheet ships with the classification columns already filled — angle, level, variation, cluster. **This is what closes the loop**: the round arrives at the analysis stage already classified, so reading the result does not require reconstructing what was tested.

### `image_batch.py`
Orchestrates image generation. Because image-model calls happen through a tool interface rather than from inside Python, the script owns the queue and the verification while the calls happen outside it.

```bash
python scripts/image_batch.py plan --brief image-brief.md --test T101 --product BRAND-SKU
python scripts/image_batch.py next          # prints the next prompt, ready to paste
python scripts/image_batch.py record --id B1-A1 --url "<result url>"
python scripts/image_batch.py verify        # count, aspect ratio, file size, naming
```

---

## Installation

This is a Claude Code skill. Clone into the skills directory:

```bash
git clone https://github.com/<user>/longform-builder.git ~/.claude/skills/longform-builder
pip install python-docx pillow
```

Then invoke it by name in a Claude Code session, from inside the project folder for the brand you are working on.

---

## Usage

```
> run a long form round for <product>, 5 angles × 3 awareness levels × 3 images
```

Phase 0 will ask for what it cannot infer: test code, product, matrix shape, destination, language, and the angles for this round. It will refuse to proceed without documented offer data, because writing fifteen long-form pieces and then discovering the price was wrong costs the whole round.

---

## Output contract

```
05-Creatives/T### - DDMM [Long Form Ads]/
├── AA BRAND-SKU T###-B1-A/          ← one folder per cell (batch × level)
│   ├── AA BRAND-SKU T###-B1-A.docx   ← copy only
│   ├── AA BRAND-SKU T###-B1-A1.png   ← the 3 image variations
│   ├── AA BRAND-SKU T###-B1-A2.png
│   └── AA BRAND-SKU T###-B1-A3.png
├── AA BRAND-SKU T###-B1-B/ ...       ← 5 batches × 3 levels = 15 folders
├── infos/AA BRAND-SKU T###-B1-A INFOS.docx ← angle, level, image prompts
├── matrix.md
├── image-brief.md
├── gate-report.md
├── upload.csv
├── drafts/                          ← source .md per copy
├── support/                         ← references, swipe, raw prompts
└── tracking/batches.json
```

Each cell folder holds exactly four files: the copy docx and the three images.

Every batch ships five fields or it does not ship: primary text, image, link headline, link description, CTA.

---

## What this is not

- **Not a copy generator.** It is a production system with a measurement discipline attached. The writing still has to be good, and the prose layer exists because it usually is not.
- **Not a scaling system.** Long form static validates angles. Scaling happens in video and advertorial, with the winner already known.
- **Not a substitute for signal floors.** Nothing here entitles anyone to a conclusion below the floor: directional reading requires spend of at least three times the real CPA **and** three conversions; conclusive reading requires ten conversions in the group. Below that, the honest answer is "insufficient signal", and that is usually the correct answer for most cells in a first round.

---

## Provenance of the numbers

Every ROAS figure quoted here comes from one source: a classification of **199 live ads from a single DTC account in the men's health vertical**, covering May to September 2026, roughly US$148,000 in spend and 524 first-purchase sales.

The classification applied twenty dimensions across five layers, and each conclusion was tested against two controls before being written down as a lock:

1. **Exclude the best-performing month**, because one month held the champion asset and contaminated every uncontrolled aggregate.
2. **Restrict to a single product**, because three products ran in the same window at very different ROAS levels.

Findings that did not survive both controls were demoted from lock to hypothesis, and three were. That demotion is the most valuable part of the work, and the reason to trust what remains.

**A standing caveat, stated here because it applies to every number above:** the source revenue is first-purchase only. In a subscription business this compares groups against each other honestly, but it does not establish profitability. No figure here should be read as a claim about margin.

The competitor length figures come from a sweep of a public ad library: 88 active ads, 70 distinct creatives, 13 publishing profiles, collected on a single day in September 2026.

---

## License

**CC BY-NC-ND 4.0** — Attribution, NonCommercial, NoDerivatives. See [LICENSE](./LICENSE).

You may share this. You may not sell it, run it as a paid service, or publish a modified version. Commercial use and derivatives require written permission.

---
---

# Versão em português

**Um sistema de produção para anúncios de long form static, construído sobre medição em vez de gosto.**

---

> **A versão de uma frase.** O Long Form Builder transforma uma rodada de teste de anúncio num experimento controlado: um ângulo por batch, um nível de consciência por coluna, uma variável na imagem, e um conjunto de regras duras tiradas da classificação de 199 anúncios veiculados, para que ninguém no time precise discutir tom de novo.

## Por que isso existe

A maioria dos times de criativo produz anúncio como uma cozinha produz jantar: alguém tem uma ideia, alguém escreve, alguém discute o tom, e sobe. Depois o número volta e ninguém consegue dizer qual decisão causou qual resultado, porque quarenta coisas mudaram ao mesmo tempo.

O resultado é uma operação que gasta dinheiro de verdade e, no fim do trimestre, ainda não responde a única pergunta que importa: **qual ângulo converte?**

Este sistema existe porque essa pergunta tem resposta, e a resposta é barata se o teste for desenhado corretamente antes da primeira palavra.

Três problemas que ele resolve, na ordem de quanto dinheiro cada um queima:

1. **Rodada não testável.** Se ângulo, nível de consciência, formato, oferta e destino variam todos juntos, a rodada produz anedota. Este sistema isola duas variáveis e trava o resto.
2. **Regra por opinião.** "Copy longa é melhor." "Nunca ser explícito." "Mostrar o produto cedo." Todas são testáveis, várias são falsas, e aqui elas viram travas medidas que carregam o número de origem.
3. **Aprender a lição errada.** O erro mais caro observado na conta de origem: ler o desempenho de um ativo como propriedade do **rótulo** e mandar alguém reescrever o rótulo.

## O que é long form static

Imagem estática no Meta, mais copy longa no texto principal.

Três propriedades justificam construir um sistema em cima do formato:

- **A imagem é o hook, não ilustração.** A única função dela é parar o scroll e comprar o clique no ver mais. Ela não vende, não mostra o produto e não carrega texto.
- **A copy carrega o ângulo.** Numa varredura de 68 long forms ativas de um concorrente da mesma vertical, a **mediana do texto principal foi de 10.809 caracteres**, 72% passaram de 8.000, e o anunciante de maior volume rodou mediana de **14.984**. Só 3% ficaram abaixo de 2.500.
- **É a forma mais barata de validar ângulo.** O que vence aqui vira vídeo e advertorial depois. Perder aqui custa cem dólares e um dia.

## O achado que moldou o sistema

Na conta de origem, um ângulo parecia campeão claro: ROAS 0,523 em 222 vendas.

Aí veio o corte por período.

| Recorte | ROAS | Vendas | Testes |
|---|---|---|---|
| Lote inteiro, vídeo | 0,523 | 222 | 10 |
| **Excluindo o mês de lançamento** | **0,281** | 18 | 8 |
| Só o mês de lançamento | 0,572 | 204 | **2** |

O ângulo fez 204 vendas em **dois** testes num mês, e 18 vendas em **oito** testes nos quatro meses seguintes. A operação leu o resultado como propriedade do ângulo, entregou o rótulo para os redatores e pediu oito reescritas. Cada reescrita perdeu por volta de metade do ROAS.

O que performou foi **aquela execução**: aquela copy, aquela imagem, aquele elenco. Não o nome em cima dela.

> ### Não repita o rótulo. Repita o ativo.
>
> Quando um batch vence, o que escala é aquela copy com aquela imagem. Nome de ângulo entregue a outro redator não é o ativo vencedor. É uma descrição do ativo vencedor, e descrição não converte.

E uma segunda correção, igualmente contraintuitiva:

> **Taxa de gancho não é monotônica. Retenção é.** Na base de origem, a faixa mais alta de gancho converteu *pior* que a faixa do meio, enquanto a retenção subiu limpa nas quatro faixas (ROAS 0,319 → 0,271 → 0,536 → 0,570). Traduzindo para estático: **CTR alto na imagem não é sinal de winner.** Não promova batch por clique.

## As seis fases

| # | Fase | Produz | Portão |
|---|---|---|---|
| 0 | **Onboarding** | arquivo do round, pasta, oferta travada | oferta documentada antes de escrever |
| 1 | **Matriz** | `matrix.md`, `tracking/batches.json` | colunas estruturalmente distintas |
| 2 | **Copy** | um `.md` por batch | faixa de comprimento por ângulo |
| 3 | **Quality gate** | `gate-report.md` | **bloqueante** |
| 4 | **Hook e briefing de imagem** | `image-brief.md` | conceito de hook qualificado antes |
| 5 | **Geração** | PNGs nomeados, na pasta de cada célula | 1:1 verificado, cena replicada |
| 6 | **Entrega** | dois `.docx` por batch (copy + INFOS) + planilha | cinco campos de placement |

Cada célula (batch × nível) tem pasta própria com exatamente quatro arquivos: o `.docx` só com a copy (texto principal e as três primeiras linhas) e as três imagens. Num round de 5 batches × 3 níveis são 15 pastas. O `.docx` INFOS de cada célula (ângulo, nível de consciência e o prompt completo de cada imagem) fica em `infos/`, na raiz do teste. Headline, descrição e CTA não entram em nenhum docx: vivem só na planilha de subida.

### A fase 3 não é opcional

O gate roda automático sobre todo rascunho e **bloqueia** nas duas violações que não têm conserto depois: pontuação proibida em ad copy, e vocabulário de truque, que foi o pior grupo de toda a base de origem.

E roda seis checagens que só leitura humana pega, a mais afiada sendo:

**O teste de troca.** Pegue as três primeiras linhas das três células de um ângulo. Se puderem ser trocadas entre si sem soar estranho, as colunas de consciência não estão diferenciadas e a rodada não vai medir nada. A linha reprova e volta para a Fase 2.

## As travas de produção

Doze regras. Cada uma sobreviveu a um controle que excluiu o mês de melhor desempenho e a um controle restrito a um único produto, que é o que separa achado de coincidência.

| # | Trava | Evidência |
|---|---|---|
| 1 | **Três modalidades de prova por copy** | 0,427 contra 0,192 com duas. O achado mais robusto do lote |
| 2 | **Nomear o produto** | 0,411 contra 0,177 quando o nome é retido por curiosidade |
| 3 | **Produto explícito e tardio. Zero vocabulário de truque** | 0,416 tardio contra 0,322 no início. Truque: **0,195**, pior grupo |
| 4 | **Narrativa de virada, não venda direta** | 0,417 contra 0,345 |
| 5 | **O vilão é a biologia** | 0,447 contra 0,317 de vilão médico ou sistema |
| 6 | **Preço em dólar, escrito** | 0,543 com cifra, 0,355 sem preço, 0,246 em dólar por dia |
| 7 | **Registro explícito, agressividade intermediária** | Explícito ganha nos dois idiomas. O *pacote* agressivo perde |
| 8 | **CTA de compra direta** | 0,412 contra 0,191 |
| 9 | **Validação por terceiro** | O resultado nunca é declarado pelo narrador sobre si mesmo |
| 10 | **Número de exame, sempre específico** | Sustenta a contradição entre laudo normal e vida real |
| 11 | **Sem travessão e sem aspas** | Regra da casa para output de ad copy |
| 12 | **As três primeiras linhas carregam o corte** | 200 a 400 caracteres, bloco fechado que levanta a pergunta sem responder |

E uma hipótese deixada de propósito fora das travas: **mencionar garantia de 30 dias bateu 90 dias, 0,486 contra 0,296**, dentro do mesmo produto. A suspeita é que 90 dias é ouvido como demora 90 dias para funcionar.

### Ausência também é informação

Em 199 anúncios classificados, quatro coisas nunca apareceram: **prova por autoridade pessoal**, **formato editorial investigativo**, **listicle** e **carta pessoal**. A primeira virou o teste de maior valor esperado do sistema, justamente por nunca ter sido rodada.

## A camada de prosa

Trava diz o que a copy precisa conter. Anatomia diz em que ordem. A prosa diz **como a frase soa**, que é o que decide se um post de 11 mil caracteres é lido até o fim ou abandonado no terceiro bloco.

Quinze técnicas, das quais as três de maior peso:

**A regra de três.** Dois parece coincidência. Quatro parece lista. Três parece padrão, e padrão parece verdade. Em três formas: tríade de sintoma, tríade de escalada e tríade de absolvição. O erro comum é a tríade de adjetivo sinônimo, que é uma ideia repetida três vezes e não engana ninguém.

**Variação de comprimento de frase.** Nunca três frases seguidas do mesmo tamanho. Depois de duas ou três longas, uma de três palavras. O corte curto depois do acúmulo é onde o leitor respira, e onde ele decide continuar.

**Concreto em vez de abstrato.** Não descreva a emoção, descreva o que a produz. Não *o quarto estava frio e distante*, mas *o lençol do lado dele estava liso. Nem amassado.*

## O que isto não é

- **Não é gerador de copy.** É um sistema de produção com disciplina de medição acoplada. O texto ainda precisa ser bom, e a camada de prosa existe porque normalmente não é.
- **Não é sistema de escala.** Long form static valida ângulo. Escala acontece em vídeo e advertorial, com o vencedor já conhecido.
- **Não substitui piso de sinal.** Nada aqui autoriza conclusão abaixo do piso: leitura direcional exige gasto de no mínimo três vezes o CPA real **e** três conversões; leitura conclusiva exige dez conversões no grupo. Abaixo disso, a resposta honesta é sinal insuficiente, e essa costuma ser a resposta certa para a maioria das células numa primeira rodada.

## Procedência dos números

Todo ROAS citado vem de uma fonte só: a classificação de **199 anúncios veiculados de uma conta DTC da vertical de saúde masculina**, de maio a setembro de 2026, cerca de US$ 148.000 de investimento e 524 vendas de primeira compra.

A classificação aplicou vinte dimensões em cinco camadas, e cada conclusão passou por dois controles antes de virar trava:

1. **Excluir o mês de melhor desempenho**, porque um mês concentrava o ativo campeão e contaminava todo agregado não controlado.
2. **Restringir a um único produto**, porque três produtos rodaram na mesma janela com ROAS muito diferentes.

Achado que não sobreviveu aos dois controles foi rebaixado de trava para hipótese, e três foram. Esse rebaixamento é a parte mais valiosa do trabalho, e a razão para confiar no que sobrou.

**Ressalva permanente, que vale para todo número acima:** a receita de origem é de primeira compra. Num negócio de assinatura isso compara grupos entre si de forma honesta, mas não estabelece lucratividade. Nenhum número aqui deve ser lido como afirmação sobre margem.

## Licença

**CC BY-NC-ND 4.0** — Atribuição, Não Comercial, Sem Derivações. Ver [LICENSE](./LICENSE).

Você pode compartilhar. Não pode vender, rodar como serviço pago, nem publicar versão modificada. Uso comercial e derivação exigem autorização por escrito.
