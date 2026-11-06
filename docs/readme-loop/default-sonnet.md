# ne-slop-text

A Claude Code skill for writing and fixing text so that it reads as written by one person, not by the average of the internet.

I'm Boris Timofeenko, a QA lead. I built it with Claude in November 2026 while working on my own texts: a CV and letters to employers.

## Why it exists

I made a quest game, "Belgrade 2026" (Godot), and its graphics came out alive, not AI-slop. The backgrounds were my phone photos of Belgrade, ruined on purpose by a script (800x600, 16 colours, JPEG at the edge of falling apart). The characters were drawn in code with brushes. The hero is a friend's photo cut out with Apple Vision, with the white fringe of a "magic eraser" left in. The MIDI music is deliberately bad. That approach became a skill of mine called `ne-slop`, for creative work in general.

For text it was not enough. Text I ran through the humanizer skill I could spot "from a mile away". So I tested what actually makes a text read as machine-made, and this skill is the result.

## The idea

Slop lives in decisions, not in words: what is said outright, who drives the events, how the text ends, what gets listed, what gets named. Swapping words does not fix it. The StoryScope paper (Russell et al., COLM 2026) separates AI stories from human ones at 93% F1 on discourse features alone, and professional surface rewriting moved detection only from 95.5% to 93.9%.

So the skill does not apply a fixed recipe. For each task it finds where default models land, then moves the draft away from there using material from the person.

## What it does

1. **Philosophy, before writing.** Find the material only this person has: an episode, an opinion, an outside force that shaped events, a hedge, their own wording. Ask one to three open questions if material is missing. Never fill a gap with the average.
2. **The loop (full mode).** Three fresh agents on different models write the plain default for the same task. Another agent annotates the draft and the defaults against a questionnaire of discourse features. `consensus.py` reports what the draft does together with every default and what leans machine-like. A reviser fixes only that. At most two rounds, and the text must not get longer.
3. **Lint, last.** A surface check for words and patterns, in English or Russian.
4. **Learn.** Blind tests, and your marks (slop or alive) become weights in the questionnaire.

Short texts (under about 120 words) skip the loop. At that length it has no signal: in a blind test, 100-word summaries written five different ways were indistinguishable.

The full procedure is in [SKILL.md](SKILL.md). How the pipeline was found, with three rounds of blind tests, is in [docs/evidence.md](docs/evidence.md).

## Install

Clone the repo into your skills folder:

```
git clone https://github.com/boriswinner/ne-slop-text ~/.claude/skills/ne-slop-text
```

## Use

Ask Claude Code to write or fix a text "ne-slop" or "не слоп", or invoke `/ne-slop-text`. It works for letters, messages to hiring teams, cover letters, CV sections, bios, posts, READMEs and video scripts, in any language.

The loop costs about 6 to 8 agent calls and 3 to 5 minutes.

## Requirements

- Claude Code with subagents (for the loop).
- Python 3, standard library only (for the scripts).

## Layout

```
SKILL.md                  the skill
loop/                     questionnaire.json, consensus.py, reviser.md, annotator.md, default_prompt.md
lint/                     lint.py, en.md, ru.md
learn/                    marks.jsonl, patterns.md, update_weights.py
tools/blind.py            builds a blind-test page from several versions of one text
docs/evidence.md          how the pipeline was found
```

## What the tests showed

The judge was me, ranking variants without knowing which method made which. A few results:

- A rules-based audit of my CV found nothing serious, yet the CV still read as partly machine-made. Rules catch what is in a text; they do not see what is missing.
- In the letter test, one round of the loop moved the ne-slop draft from third place to first. A letter written by hand, using everything learned earlier, lost to the procedure.
- The humanizer applied on top of a default was close to noise.
- "I lead 3 QA engineers and sign off releases" was marked alive three times. "Lead a team of 3 QA engineers and own release sign-off" was marked slop.

Of 39 marked sentences, no pattern got mixed labels. Slop: inventory lists, clever turns, resume-speak. Alive: stance, plain first person, an outside force, a specific episode.

## Limits

One judge, three tasks, one domain (job search). Ranks between near-identical texts are noisy. The questionnaire is annotated by a model, which shares blind spots with the writers, so the human stays the final judge. The lint word lists are the weakest signal and the first to age.

## Related

- Paper: Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. "StoryScope: Investigating idiosyncrasies in AI fiction". COLM 2026. arXiv:2604.03136.
- `humanizer`: Wikipedia's "Signs of AI writing" patterns. Its pattern list feeds the lint here; its rewriting for "personality" is excluded on purpose.
- `unslop`: a guardrail against slop in German and English prose. Its portability test and word lists are used here.
- `ne-slop`: the parent skill for creative work in general.
