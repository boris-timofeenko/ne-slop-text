# ne-slop-text

A Claude Code skill for writing and fixing text so that it reads as written by a specific person, not by the average of the internet. Works in any language.

It is meant for letters, messages to hiring teams, cover letters, CV sections, bios, posts, READMEs and video scripts. It does not apply a fixed style recipe. For each task it finds where default models tend to land and moves the draft away from there, using material from the person.

Built by Boris Timofeenko (QA lead) in November 2026, on his own texts: a CV and letters to employers. The idea grew out of a quest game, "Belgrade 2026", where code-drawn graphics came out alive instead of generic. For text, Boris found that rewriting with the humanizer skill was still easy to spot, so this skill was built instead.

## Why it is structured this way

Slop is the average: what a model writes when it fills a gap with the most likely move, or when asked to "make it better". It lives in decisions (what is said outright, who drives the events, how the text ends, what gets listed, what gets named), not in individual words. Swapping words does not fix it.

The approach follows StoryScope (Russell et al., COLM 2026, arXiv:2604.03136), which separates AI-written from human-written stories at 93% F1 using discourse features alone.

## How it works

Pick the mode first:

- Short (under about 120 words: chat replies, short messages, titles): Step 1, then Step 3. A loop has no signal at this length.
- Full (anything longer that goes to other people): Steps 1 to 4. Step 5 when the text matters or on request.

**Step 1. Philosophy, before writing.** Find what only this person has: a specific episode, an opinion they hold, a force outside them that shaped events, a hedge or a limit, their own wording. If the text matters, ask one to three open questions; voice answers work well. If no questions are possible, use verifiable specifics and leave gaps visible. Never fill a gap with the average.

**Step 2. The loop (full mode).**
1. Three fresh agents on different models write the plain task, without seeing the skill or the draft (`loop/default_prompt.md`).
2. A fourth agent, on a different model from the writer, annotates the draft and the defaults with a questionnaire of discourse features (`loop/questionnaire.json`, `loop/annotator.md`).
3. `loop/consensus.py` reports what the draft shares with every default, what leans machine-like, and what is human-leaning and must be kept.
4. A reviser (`loop/reviser.md`) changes only the flagged parts. Material beats weights: a sentence that renders the person's own words stays even if a feature flags it.
5. Stop after at most two rounds, or when nothing is flagged. The text must not get longer.

Cost is about 6 to 8 agent calls and 3 to 5 minutes.

**Step 3. Lint, last.** `python3 lint/lint.py FILE --lang en` (or `ru`), then read `lint/en.md` or `lint/ru.md`. Fix only what it flags. The word lists are the weakest signal and the first to age.

**Step 4. Output.** The text, a short note on what changed and why, and any open questions or gaps. When context was used, a "line ← source" map. The original files are never edited; drafts are written next to them.

**Step 5. Learn.** For important texts, `tools/blind.py` builds a blind comparison of several versions of the same material. Marks go into `learn/marks.jsonl` with a pattern tag from `learn/patterns.md`, and `learn/update_weights.py` shows which questionnaire weights disagree with the marks. When the user edits the text, the diff is treated as a mark too.

## Install

Requirements: Python 3 (standard library only) for the scripts, and Claude Code with subagents for the loop.

```
git clone https://github.com/boriswinner/ne-slop-text ~/.claude/skills/ne-slop-text
```

Invoke it by asking Claude Code to write or fix a text, for example with "ne-slop", "не слоп", "humanize", "sounds like AI", or with `/ne-slop-text`.

## Repository layout

- `SKILL.md`: the skill instructions.
- `loop/`: `questionnaire.json`, `consensus.py`, `reviser.md`, `annotator.md`, `default_prompt.md`.
- `lint/`: `lint.py`, `en.md`, `ru.md`.
- `learn/`: `marks.jsonl`, `patterns.md`, `update_weights.py`.
- `tools/blind.py`: blind comparison builder.
- `docs/evidence.md`: how the pipeline was found and tested.

## Evidence

Three rounds of blind tests, November 2026. The judge was Boris, whose texts these were. He did not know which method produced which variant until he had ranked them. Full details are in `docs/evidence.md`.

- **Round 1, seven CV summaries** (current CV, humanizer, unslop, Opus from facts, and others). Scores were close and Boris found it hard to tell which was not slop. At about 100 words, methods did not separate. He marked sentences that list things and sentences written for their sound.
- **Round 2, one voice interview, five ways to turn it into text.** The version closest to the speech ranked first. A single Opus pass from the same transcript dropped the opinion and the outside push entirely. The same fact in three forms ("I lead 3 QA engineers and sign off releases" against two more formal versions) was alive once and slop twice.
- **Round 3, a hiring-team letter.** The loop moved the ne-slop draft from third place to first. It cut three clever turns and most phrases quoted from the job ad, and kept the push, the specific bug and the opinion. It also cut a line Boris liked, so the rule became: the ad's words can answer the reader, but should not be used as labels.

Marks so far: 39 sentences, and no pattern received mixed labels. Slop marks: inventory, clever turns, resume-speak, process description, staged jokes, text about itself. Alive marks: stance, plain first person, outside force, reader address, a specific episode.

## What not to do

Each of these was tested:

- Polishing toward the genre ("make it more professional"). Resume-speak and the solo hero come back, and episodes get mangled.
- Generating from good material in one pass. The model dissolves the voice into the average and drops the opinion.
- Performing casualness: jokes built as constructions ("The joke answer is...; the real answer is..."), or "add personality" rewrites.
- Taking an opinion from old notes instead of from the person.
- Chasing rare words. Living text is lexically ordinary; the difference is in its decisions.
- Clever turns, even the person's own.
- Text about the text itself ("The X first, since you asked for it explicitly").

## Related skills

- `humanizer`: its pattern list feeds the lint. Its rewriting with "personality and soul" is excluded on purpose.
- `unslop`: the portability test (would this sentence fit another person or company?) and its guardrails against invented facts are used in Steps 1 and 3.
- `ne-slop`: the parent skill for creative work. Step 1 here is its text-specific part.

## Limits

One judge, three tasks, one domain (job search). Rankings between near-identical texts are noisy. The questionnaire is annotated by a model, which shares blind spots with the writers. The human stays the final judge.
