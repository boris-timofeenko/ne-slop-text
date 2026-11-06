# ne-slop-text

A Claude Code skill for writing and fixing text so that it reads as written by a particular person. It was built on
Boris Timofeenko's own texts (a CV, letters to employers) and tested blind on him in November 2026.

## Why it exists

Boris made a quest game, "Belgrade 2026", and its graphics came out alive: photos from his phone ruined by a script,
characters drawn in code, a hero cut out of a friend's photo with the white fringe of a magic eraser left on. That
became the `ne-slop` skill. It worked for pictures. For text it did not: a letter run through the humanizer skill he
could spot from a mile away.

StoryScope (Russell et al., COLM 2026) shows why. Across 61,608 stories by people and five models, the narrative
decisions alone told AI from human at 93% F1, and rewriting the clichés moved detection only from 95.5% to 93.9%.
Models write from one narrow region; people are scattered. Replacing words leaves the decisions where they were.

## How it works

1. **Philosophy.** Before writing, find what only this person has: an episode, an opinion, someone else who shaped
   the events, a hedge, their own wording. If it is missing and the text matters, ask one to three questions, by voice
   if possible. Write close to their words.
2. **The loop.** Three fresh agents on different models write the same text with no method. Another agent annotates
   them and the draft on 21 discourse features (`loop/questionnaire.json`). `loop/consensus.py` flags where the draft
   does what every default does and the feature leans machine-like. A reviser changes only that, at most twice.
3. **Lint.** Regexes and a short checklist for what is left on the surface: em dashes, "not just X but Y", trailing
   clauses that explain significance, stock phrases. English and Russian.

The weights of the 21 features started from StoryScope and are corrected by the user's own marks. `learn/marks.jsonl`
holds every sentence Boris labelled slop or alive in blind tests; `learn/update_weights.py` shows where the
questionnaire disagrees with them.

## Does it work

In the last blind test (a message to a hiring team, five letters from the same material) the letter after the loop
came first and the plain Opus letter came last; Boris recognised it. A letter Claude wrote by hand, with everything
learned in the earlier rounds, came fourth, behind the procedure. The rounds, including what failed, are in
`docs/evidence.md`.

One judge, three tasks, one domain so far. Read the numbers as a direction, not a benchmark.

## Install

```bash
git clone https://github.com/boriswinner/ne-slop-text ~/.claude/skills/ne-slop-text
```

Then ask Claude Code to write or fix a text "ne-slop" (or "не слоп"), or run `/ne-slop-text`. Texts under about 120
words get the philosophy and the lint; longer ones also get the loop, which costs 6 to 8 agent calls and a few minutes.
The scripts need Python 3 and nothing else.

## Blind test

```bash
python3 tools/blind.py out.html key.json "Title" "Subtitle" a=a.txt=label-a b=b.txt=label-b
```

The page shuffles the variants. Click a sentence to mark it slop or alive, rank the variants, press "collect" and paste
the result back to Claude. The marks go to `learn/marks.jsonl`.

## Files

```
SKILL.md                 the pipeline, as Claude reads it
loop/questionnaire.json  21 features with weights
loop/consensus.py        where the draft sits with the defaults
loop/reviser.md          what the reviser may and may not do
loop/annotator.md        instructions for the annotating agent
loop/default_prompt.md   how to brief the default writers
lint/lint.py             surface checks, en and ru
learn/marks.jsonl        the user's marks
learn/update_weights.py  marks against weights
tools/blind.py           blind test page
docs/evidence.md         how the pipeline was found
```

## Credits

- Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. "StoryScope: Investigating
  idiosyncrasies in AI fiction". COLM 2026. arXiv:2604.03136.
- The humanizer and unslop skills: their pattern and word lists feed the lint.
- `ne-slop`, Boris's skill for creative work in general; this is its part for text.
