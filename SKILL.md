---
name: ne-slop-text
description: Write or fix text for people so that it reads as written by this person, not by the average of the internet. v2 pipeline - the person's material and the reader first, a story skeleton, then a loop that compares the draft with what default models write for the same task and edits only the empty, model-like sentences without losing the story; a metric trained on talented human texts vs model defaults is used only as a guard ("still in the machine cloud?"), never as a target; then a surface lint. Any language (metric for English and Russian). Use for letters, messages to hiring teams, cover letters, CV sections, bios, posts, READMEs, video scripts. Triggers - "не слоп", "ne-slop", "по-человечески", "живее", "звучит как ChatGPT", "sounds like AI", "unslop", "humanize", "fix this text", "write a message to".
---

# ne-slop-text v2

Slop is the average: what a model writes when it fills a gap with the most likely move, or when it is asked to
"make it better". It lives in decisions (what is said outright, how it opens and ends, which fact comes first, what
is listed), not in words. Models writing the same task converge: two Opus letters had the same skeleton down to the
closing line; three models opened a paragraph about flaky tests with the same sentence and the same Google figure.

What the tests showed (details in `docs/evidence.md`):
- The strongest lever is material: the person's own words rendered close to the source beat polishing and beat a model
  writing from the same transcript. Without material, real specifics found one step past the obvious ones did the work.
- A metric trained on talented human texts vs model defaults tells a default from a non-default well, but texts pushed
  down its scale got worse for the reader: glosses, links and framing were cut, and a story turned into a list of facts.
  So here it only guards.
- What kept texts good in the loop was its structure: a story skeleton that must survive every edit, "edit, don't
  delete", a clarity floor, and a truth check.

Scripts and briefs below are in this skill's folder; data files (task.md, drafts, annotations) live next to the task.

## Inputs

- A task (what to write, for whom, why, how long) or a source (a text to fix).
- Material, optional: documents, facts, the person's own words (voice transcripts, chats, notes).

## Mode

- Short (under ~120 words: chat replies, short messages, titles): Steps 0, 1, 2, 7. The loop has no signal at this
  length.
- Full (anything longer that goes to other people): all steps. About 10 to 18 agent calls, 10 to 15 minutes.

Who does what. You (the session the user talks to) write the task file and the draft, run the scripts and decide.
Fresh agents do the rest, each seeing only the files named for it: defaults on opus, sonnet and haiku; annotators,
ablation and reader on sonnet; reviser and checker on opus (the checker needs web search when there is no material).
Tell every agent not to use skills.

## Step 0. The task file

Write `task.md` before anything else: who the readers are and what they literally asked; the purpose; the target
length in words of the body, as `python3 loop/batch.py words FILE` counts it (no greeting, sign-off or gaps; if the
task gives none, choose one for the genre and write it down); the elements the text must
contain (a required episode, logistics, a greeting); where the material is; the gap format `(GAP n: what is missing)`.
Every agent below gets this file.

## Step 1. Material and the reader

1. **Material first.** What only this person has: a specific episode, an opinion, a force other than them that shaped
   events, a hedge or a limit, their own wording. Old texts of the same genre give facts, not voice.
2. **Missing material.** If the text matters, ask 1 to 3 open questions that do not suggest the answer ("how did it
   actually happen", "was there a case", "what do you think about X", "what can't you do yet"). Voice answers are best;
   keep the transcript as material. If you cannot ask: real, checkable specifics from the world (web search), and gaps
   left visible. Never fill a gap with the average.
3. **The reader and their code.** What did they literally ask for? Answering in their own words is alive when it makes
   a point; using their words as labels or headings is slop.

## Step 2. Draft with a skeleton

Write the draft yourself, following `loop/writer.md`: 3 to 5 beats first (hook or question, evidence, turn,
consequence, open end) into `beats.json`, then the text close to the material. For a source text (fix mode), extract
its beats instead and keep every sentence that renders the person's material.

## Step 3. Defaults (full mode)

Spawn 3 fresh agents (opus, sonnet, haiku) with the plain task, the same material and the target length, as in
`loop/default_prompt.md`. They must not see this skill, the draft or each other. Then:

```bash
python3 loop/overlap.py draft.txt d1.txt d2.txt d3.txt --material cv.txt --material vacancy.md > overlap.txt
```

It shows what the draft takes from every default at once: an opening close to theirs, specifics every default uses
(facts from the material are listed apart and never flagged), shared phrasing.

## Step 4. Moves, ablation, guard

1. `python3 loop/batch.py texts batch.txt sentences.json DRAFT=draft.txt D1=d1.txt D2=d2.txt D3=d3.txt`
2. Two fresh annotators label the same batch with `loop/annotator.md` → `annA.json`, `annB.json`. Two, because one
   text-level label (a plain opening is worth about 12 points) is the size of the annotator noise.
3. `python3 gate/gate.py annA.json annB.json --lang en --sentences sentences.json` lists every draft sentence with a
   model-leaning move from either annotator and prints `to ablate: 3,5,7`.
4. `python3 loop/batch.py ablate abl.txt draft.txt 3,5,7`; a fresh agent with `loop/ablation.md` reads `task.md` and
   `abl.txt` → which sentences are load-bearing → `lb.json` = `{"DRAFT": [3]}`.
5. `python3 gate/gate.py annA.json annB.json --lang en --sentences sentences.json --load-bearing lb.json`

The verdict is about the sentences: "out of the cloud", "STILL IN" (both annotators agree), "UNCLEAR" (they
disagree) or "NOT MEASURABLE" (the defaults' sentences are themselves within noise of a text with no moves, which is
common when the material is a fact sheet such as a CV). A NOTE says when only the opening or closing label puts the
draft in the cloud. The sentence list marks each one LOAD-BEARING or EMPTY. Text-level decisions are information only.

**Stop here** (go to Step 7) if there are no EMPTY sentences and `overlap.py` flagged nothing. The verdict alone is not
a reason to revise: with nothing empty and nothing shared, there is nothing honest left to change.

## Step 5. Revise, check, read (one round)

1. A fresh reviser with `loop/reviser.md` gets `task.md`, the material, `beats.json`, the draft, both reports and the
   list of sentence numbers it may change: the EMPTY ones, the opening if `overlap.py` flagged it as close to the
   defaults' opening, and the sentences that carry a specific `overlap.py` flagged.
2. `python3 loop/scope.py draft.txt revised.txt 3,5` (the same list). If it reports OUT OF SCOPE, keep the old draft or
   send the reviser back once with the violations.
3. A fresh checker with `loop/checker.md` checks truth (material, or web sources if there is none), restores dropped
   facts and lost beats, turns claims about what the person lacks into gaps, checks the required elements. Remove performed sentences that are not in the material. Count the body with
   `batch.py words`; if it is more than 10% off the target, keep the old draft.
4. A fresh reader with `loop/reader.md` compares the previous and the new version as the intended reader, in random
   order as X and Y (it must not know which is new). If the new one is harder to follow, keep the previous one.
5. If the checked revision is identical to the draft, stop the loop: there is nothing it can change.

## Step 6. Re-check

Build a new batch with the new draft AND the three defaults (`batch.py texts`), have two fresh annotators label it,
and run the guard. Sentence numbers shift when sentences are merged or split, so match by text: a model-leaning
sentence identical to one already found load-bearing stays load-bearing; ablate the rest. Write a fresh `lb.json` with
the new numbers, run the guard and `overlap.py` again. Stop when there are no EMPTY sentences
and nothing flagged by `overlap.py`, or after 2 rounds. If the verdict is still IN after 2 rounds, or UNCLEAR, say so
to the user in one line; do not keep editing to move it.

## Step 7. Lint, then output

`python3 lint/lint.py FILE --lang en` (or `ru`): fix what it flags, then read the lines it lists for checking by eye
(staged colons) with `lint/en.md` or `lint/ru.md`.

Give the user: the text; what changed and why, in a few lines; the guard's verdict in one line; the gaps and the
questions that would fill them. Never edit the user's original files; write drafts next to them.

## Checking a version of the method

- Blind test: `python3 tools/blind.py out.html key.json "Title" "Subtitle" name=path=label ...` (typography is evened
  out across variants; `--raw` to keep it). Several processings of the same material, ranking without ties.
- One judge cannot tell close variants apart: in our tests the same two texts swapped places from one day to the next.
  Trust only large differences (default vs not, story vs list), or use several judges.
- Sentence marks ("slop" / "alive") contradicted each other across sessions; they are notes, not training data.
  `learn/` keeps the v1 marks as history.

## What not to do (each was tested)

- Chasing the metric. Texts pushed down its scale lost their links and framing and read worse; one reviser even read
  the metric's code to game it.
- Deleting framing to look less machine-like. Edit an empty gloss into a concrete consequence instead.
- Polishing toward the genre ("make it more professional"): resume-speak and the solo hero come back.
- Generating from good material in one pass: the model dissolves the voice into the average.
- Performing voice: jokes written as constructions, "add personality" rewrites, asides and slang that are not in the
  material. That is the humanizer signature people spot.
- Taking an opinion from old notes instead of from the person, live.
- Clever turns, even the person's own ("talk to engineers like an engineer").
- Text about itself ("The X first, since you asked").
- Leaving a typographic tell in a blind test (one em dash sank a human original).

## Where other approaches fit

- `ne-slop` (the parent skill, any creative work): Step 1 is its text part.
- StoryScope (Russell et al., COLM 2026): the method behind the guard: decisions instead of words, texts written for
  the same task, an interpretable human-vs-model model. Its finding that surface rewriting barely moves detection is
  why the lint comes last.
- unslop: the portability test and the guardrails against invented facts; its word lists feed the lint.
- humanizer: its pattern list feeds the lint; its rewriting with "personality and soul" is excluded on purpose.
