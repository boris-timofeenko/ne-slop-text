# ne-slop-text

A Claude Code skill for writing and fixing text so it does not read as machine-made: letters, cover letters,
messages to hiring teams, CV sections, bios, posts, READMEs, video scripts. Any language; the surface lint has
notes for English and Russian.

## Where it comes from

Boris Timofeenko, a QA lead, made a quest game in Godot, "Belgrade 2026". Its graphics came out alive rather than
AI-slop. His phone photos of Belgrade were ruined by a script (800x600, 16 colours, JPEG at the edge of falling
apart), the characters were drawn in code with brushes, the hero is a friend's photo cut out with Apple Vision with
the white fringe of a "magic eraser" left on, and the MIDI music is bad on purpose. That approach became his
`ne-slop` skill for creative work.

For text it was not enough. Text run through the humanizer skill he could spot "from a mile away". This skill was
built with Claude in November 2026 and tested on his own texts: a CV and letters to employers.

## The idea

Slop here is the average, what a model writes when it fills a gap with the most likely move. It sits in decisions
(what is said outright, who drives the events, how the text ends, what gets listed) more than in words. StoryScope
(Russell et al., COLM 2026) separates AI from human stories at 93% F1 on discourse features alone, and professional
surface rewriting moved detection only from 95.5% to 93.9%.

So the skill has no fixed recipe. For each task it has default models write the same text, sees where they land,
and moves the draft away from there with material only the person has.

## Pipeline

1. **Before writing.** Find the person's own material: a specific episode, an opinion, a force other than them that
   shaped events, a hedge, their own wording. If the text matters, ask 1 to 3 open questions; voice answers work
   best. Check what the reader literally asked for. Stay close to the material: "I lead 3 QA engineers and sign off
   releases" was marked alive, "Lead a team of 3 QA engineers and own release sign-off" was marked slop.
2. **The loop**, for texts over about 120 words. Three fresh agents on different models write the plain task without
   seeing the skill, the draft or each other. Another agent annotates the draft and the defaults with a
   questionnaire of discourse features. `consensus.py` flags what the draft does together with every default when
   that feature leans machine-like, and a reviser fixes only that. At most two rounds, and the text must not get
   longer. About 6 to 8 agent calls and 3 to 5 minutes.
3. **Lint, last.** `lint.py` checks surface patterns. Fix only what it flags.
4. **Output.** The text, what changed and why, and the gaps that stayed open.
5. **Learn**, when the text matters. A blind-test page where the person ranks variants and marks sentences as slop
   or alive. Marks go into `learn/marks.jsonl`; `update_weights.py` shows where the questionnaire weights disagree
   with them.

Short texts skip the loop. In a blind test, 100-word summaries written five different ways could not be told apart.

## Evidence

Three rounds of blind tests in November 2026. Boris judged them and did not know which variant came from which
method until he had ranked them. Details in `docs/evidence.md`.

- Seven CV summaries of about 100 words. Methods did not separate.
- One voice interview turned into text five ways. A translation close to the speech came first. Opus writing from
  the same transcript in one pass came last; it dropped the opinion and the outside push.
- A message to the hiring team for a QA role whose ad asked for stoic virtues, with no text to start from. The
  ne-slop draft plus one round of the loop came first, the same draft without the loop third, the Opus default last
  (Boris guessed it).

Limits: one judge, three tasks, one domain (job search), 39 marked sentences so far. The questionnaire is annotated
by a model, which shares blind spots with the writers, so the person stays the final judge.

## Install

```
git clone https://github.com/boriswinner/ne-slop-text ~/.claude/skills/ne-slop-text
```

Needs Python 3 (standard library only) for the scripts, and Claude Code with subagents for the loop.

Ask Claude Code to write or fix a text "ne-slop" (or "не слоп"), or run `/ne-slop-text`.

## Files

```
SKILL.md                the pipeline
loop/
  default_prompt.md     prompt for the default writers
  annotator.md          instructions for the annotating agent
  questionnaire.json    discourse features, each with a lean and a weight
  consensus.py          report: what the draft shares with the defaults
  reviser.md            allowed and forbidden moves for the reviser
lint/
  lint.py               surface lint
  en.md, ru.md          what to do with its flags, per language
learn/
  marks.jsonl           blind-test marks
  patterns.md           pattern tags for the marks
  update_weights.py     checks questionnaire weights against the marks
tools/blind.py          builds a blind-test page
docs/evidence.md        how the pipeline was found
```

## Related

- `ne-slop`, the parent skill for creative work. Step 1 of this pipeline is its text part.
- humanizer, built on Wikipedia's "Signs of AI writing" patterns. Its pattern list feeds the lint; its rewriting
  with "personality and soul" is left out on purpose.
- unslop, a guardrail against slop in German and English. Its portability test and word lists are used in steps 1
  and 3.
- Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. "StoryScope: Investigating
  idiosyncrasies in AI fiction". COLM 2026. arXiv:2604.03136. The theory behind the loop and the seed of the
  questionnaire weights.
