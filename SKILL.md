---
name: ne-slop-text
description: Write or fix text for people so that it reads as written by this person, not by the average of the internet. Pipeline - philosophy (material and the reader first), a loop that pushes the draft away from what default models write for the same task (StoryScope-style discourse features with weights learned from the user's blind-test marks), then a surface lint. Any language. Use for letters, messages to hiring teams, cover letters, CV sections, bios, posts, READMEs, video scripts. Triggers - "не слоп", "ne-slop", "по-человечески", "живее", "звучит как ChatGPT", "sounds like AI", "unslop", "humanize", "fix this text", "write a message to".
---

# ne-slop-text

Slop is the average: what a model writes when it fills a gap with the most likely move, or when it is asked to
"make it better". It lives in decisions (what is said outright, who drives the events, how it ends, what is listed,
what is named), not in words. Swapping words does not fix it: StoryScope (Russell et al., COLM 2026) separates AI
from human stories at 93% F1 on discourse features alone, and professional surface rewriting moved detection only
from 95.5% to 93.9%. Models cluster in one region; people scatter. So this skill does not apply a fixed recipe. It
finds, for each task, where the default models land, and moves the draft away from there with material from the
person.

How the pipeline was found and tested: `docs/evidence.md`. Paths below are relative to this skill's directory.

## Inputs

- A task (what to write, for whom, why) or a source (a text to fix).
- Context, optional: documents, facts, the person's own words (voice transcripts, chats, internal notes).

## Pick the mode

- Short (under ~120 words: chat replies, short messages, titles): Step 1, then Step 3. The loop has no signal at
  this length; in a blind test, 100-word summaries written five different ways were indistinguishable.
- Full (anything longer that goes to other people): Steps 1, 2, 3, 4. Step 5 when the text matters or the user asks.

## Step 1. Philosophy, before writing

1. **Material first.** Find what only this person has: a specific episode; an opinion they hold; a force other than
   them that shaped events (someone pushed, something was inherited, something failed); a hedge or a limit; their own
   wording. Old texts of the same genre (previous CVs and letters) give facts, not voice.
2. **Missing material.** If the text matters, ask 1 to 3 short questions; voice answers are best, keep the transcript
   as material. Ask open questions that do not suggest the answer: "how did it actually happen", "was there a case",
   "what do you think about X", "what can't you do yet". If you cannot ask, use verifiable specifics (names, numbers,
   sources) and leave gaps visible. Never fill a gap with the average.
3. **The reader and their code.** What did they literally ask for? What words and jokes do they use? Answering with
   their own words is alive when it makes a point ("Your ad asks for justice, so I won't claim to be the best: I
   haven't met the other candidates"). Using their words as labels or headings is slop.
4. **Render close to the material.** The person's order of thought, their hedges ("probably", "on the whole"),
   literal rather than idiomatic translation, first person with short verbs: "I lead 3 QA engineers and sign off
   releases" was marked alive; "Lead a team of 3 QA engineers and own release sign-off" was marked slop.
5. **Genre lives in the container** (format, length, greeting, required fields), not in every sentence. Lists go where
   lists belong (a skills section, a table, the attached CV); a sentence carries one episode or one mechanism.
6. **Doubt what comes easily.** If a sentence arrived without a decision, it is probably the average.

## Step 2. The loop: away from the default (full mode)

1. **Defaults.** Spawn 3 fresh agents on different models (e.g. opus, sonnet, haiku). Give each the plain task and
   the same context with `loop/default_prompt.md`. They must not see this skill, the draft, or each other.
2. **Annotate.** One more fresh agent, on a different model from the writer, annotates the draft and the defaults
   with `loop/questionnaire.json`, following `loop/annotator.md`. Output: `features.json`.
3. **Report.**
   `python3 loop/consensus.py loop/questionnaire.json features.json D1,D2,D3 DRAFT TEXTS_DIR > report.txt`
   gives P1 (the draft does what every default does, and it leans machine-like), P2 (leans machine-like by weight),
   Keep (human-leaning, do not lose), the 4-grams shared with the defaults and how close the opening sentence is to
   theirs.
4. **Revise.** A fresh agent applies `loop/reviser.md` to the draft with the report and the context. Material beats
   weights: a sentence that renders the person's own words stays even if a feature flags it.
5. **Stop** after at most 2 rounds, or when P1 is empty. The text must not get longer.

Cost: about 6 to 8 agent calls and 3 to 5 minutes. Consensus alone is not slop: when the context is rich, every
default has a specific episode too. A flag needs both: the defaults agree, and the feature leans machine-like. Some
agreement is just the genre (a README says how to install); tell the reviser what the container is.

## Step 3. Lint, last

`python3 lint/lint.py FILE --lang en` (or `ru`), then read `lint/en.md` or `lint/ru.md`. Fix only what it flags; do
not restructure at this stage. The word lists are the weakest signal and the first to age.

## Step 4. Output

Give the user: the text; what changed and why, in a few lines; open questions and gaps that stayed visible. When
context was used, offer a "line ← source" map. Never edit the user's original files; write drafts next to them.

## Step 5. Learn

- **Blind test** for important texts:
  `python3 tools/blind.py out.html key.json "Title" "Subtitle" name=path=label ...`
  Several processings of the same material, ranking without ties, sentence marks (slop / alive). Compare at least two
  paragraphs; short snippets do not separate.
- **Marks become weights.** Append the user's marks to `learn/marks.jsonl` with a pattern tag from
  `learn/patterns.md`, then run `python3 learn/update_weights.py`. It shows which patterns are settled and which
  questionnaire weights disagree with them; edit `loop/questionnaire.json` to match. A new pattern marked slop twice
  and never alive becomes a new feature.
- **Rejections teach more than praise.** When the user edits your text, diff it: what they cut is a mark too.

## What not to do (each was tested)

- Polishing toward the genre ("make it more professional"): resume-speak and the solo hero come back, and episodes
  get mangled.
- Generating from good material in one pass: the model dissolves the voice into the average and drops the opinion.
- Performing casualness: jokes written as constructions ("The joke answer is...; the real answer is..."),
  "add personality" rewrites. This is the humanizer signature that people spot.
- Taking an opinion from old notes instead of from the person, live. The notes said one thing; the person said another.
- Chasing rare words. Living text is lexically ordinary; the rarity is in its decisions.
- Clever turns, even the person's own ("talk to engineers like an engineer", "...and the team hands tickets to one").
- Text about itself ("The X first, since you asked for it explicitly").

## Where other approaches fit

- `ne-slop` (the parent skill, for any creative work): Step 1 is its text-specific part. Real material, many small
  explicit decisions, several unlike variants, the person chooses, rejections are remembered, look at the result.
- StoryScope: the theory behind Step 2 and the seed of the questionnaire weights.
- unslop: the portability test (would this sentence fit another person or company?) and its guardrails against
  invented facts belong to Steps 1 and 3; its word lists feed the lint.
- humanizer: its pattern list feeds the lint. Its rewriting with "personality and soul" is excluded on purpose.
