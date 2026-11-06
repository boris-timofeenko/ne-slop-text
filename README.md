# ne-slop-text

Boris Timofeenko made a quest game, "Belgrade 2026", and its graphics came out alive: photos from his phone ruined by
a script, characters drawn in code, a hero cut out of a friend's photo with the white fringe of a magic eraser left
on. That became the `ne-slop` skill. For text it was not enough. Text run through the humanizer skill he could spot
from a mile away. In November 2026 he built this Claude Code skill with Claude, on his own texts (a CV, letters to
employers), and tested it blind on himself.

## The tests

Before the tests, the unslop skill audited Boris's CV and found nothing serious, though the CV read as partly
machine-made. Its pattern lists and the humanizer's now feed only the surface lint (`lint/lint.py`).

In round two Boris answered five open questions by voice, unprepared. The answers had what no written source had, such
as an outside push ("management told us to go faster") and a bug: an AI agent that did not know today's date turned
away people who had just turned 18. A translation close to his speech came first; Opus writing from the same
transcript in one pass came last and dropped the push. When such material is missing and the text matters, the skill
asks one to three questions, by voice if possible, and writes close to the answers.

The last round was a message to a hiring team. Four default writers got the same material and no method; the two Opus
letters had the same skeleton down to the closing line, "I'd be glad to have that coffee". An annotator marked them
and the ne-slop draft on 21 discourse features (`loop/questionnaire.json`), `loop/consensus.py` flagged where the
draft did what every default did and the feature leaned machine-like, and a reviser changed only that. It cut three
clever turns and three of four phrases quoted from the ad, and the draft moved from third place to first. Claude's
hand-written letter, with everything learned earlier, came fourth; the plain Opus letter came last, and Boris
recognised it.

The 21 features were seeded from StoryScope (Russell et al., COLM 2026): across 61,608 stories by people and five
models, narrative decisions alone told AI from human at 93% F1, and rewriting the clichés moved detection only from
95.5% to 93.9%. `learn/update_weights.py` compares their weights with Boris's marks.

One judge, three tasks, one domain so far. Read the numbers as a direction. The rounds, including what failed, are in
`docs/evidence.md`.

## Install

```bash
git clone https://github.com/boriswinner/ne-slop-text ~/.claude/skills/ne-slop-text
```

Then ask Claude Code to write or fix a text "ne-slop" (or "не слоп"), or run `/ne-slop-text`. Texts under about 120
words skip the loop; on longer ones it runs three default writers and up to two revisions, 6 to 8 agent calls and a
few minutes. The scripts need Python 3 and nothing else.

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

## This README

It went through the skill. Three fresh agents (Opus, Sonnet, Haiku) wrote their own READMEs from the same context, and
all three opened like the first draft did: "A Claude Code skill for...". The report also flagged two clever turns and a
moral stated after the story. One revision moved the game to the top and told the mechanism through the tests. The
draft, the defaults and the report are in `docs/readme-loop/`.

## Credits

- Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. "StoryScope: Investigating
  idiosyncrasies in AI fiction". COLM 2026. arXiv:2604.03136.
- The humanizer and unslop skills: their pattern and word lists feed the lint.
- `ne-slop`, Boris's skill for creative work in general; this is its part for text.
