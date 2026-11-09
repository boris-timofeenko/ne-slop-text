# ne-slop-text

Boris Timofeenko made a quest game, "Belgrade 2026", and its graphics came out alive: photos from his phone ruined by
a script, characters drawn in code, a hero cut out of a friend's photo with the white fringe of a magic eraser left
on. That became the `ne-slop` skill. For text it was not enough. Text run through the humanizer skill he could spot
from a mile away. In November 2026 he built this Claude Code skill with Claude, on his own texts (a CV, letters to
employers), and tested it blind on himself. This is version 2.

## What the tests found

Version 1 compared a draft with what three default models write for the same task and fixed only what the draft
shared with all of them. In blind tests it moved a letter to a hiring team from third place to first, and a
translation close to Boris's voice answers beat both polishing and a model writing from the same transcript. The two
Opus letters in that test had the same skeleton down to the closing line, "I'd be glad to have that coffee".

Version 2 started with a night experiment. Three agents collected 139 texts by 37 talented authors written before 2022
(business letters, engineering posts, Russian business prose), rebuilt the task behind each, and had Opus, Sonnet and
Haiku write it too: 417 defaults. A model learned which sentence moves separate the two. On the model side: glosses,
morals, signposts, recap endings. On the human side: asides, questions, irony, quoted speech. On authors it had not
seen, it ordered 92 of 100 human-model pairs correctly in letters, 95 in Russian and 78 in engineering posts.

Then the loop drove texts down that scale, and they got worse. The metric's order matched Boris's rankings about as
often as chance, and three times its top pick was his last. The reviser had cut every link and frame, and a story
became a list of facts. What worked was structure: a skeleton of 3 to 5 beats that every edit must keep, edits
instead of deletions, a clarity floor checked by a reader agent, and a truth check. With those, the new loop came
second on both of the last two pages and never last. The metric stayed as a guard that answers one question: is the
draft still in the machine cloud of its task?

One judge, a handful of tasks, mostly about work. Treat the numbers as a direction. The rounds, including what failed,
are in `docs/evidence.md`. Version 1 is tagged `v1`.

## Install

```bash
git clone https://github.com/boris-timofeenko/ne-slop-text ~/.claude/skills/ne-slop-text
```

Then ask Claude Code to write or fix a text "ne-slop" (or "не слоп"), or run `/ne-slop-text`. Texts under about 120
words skip the loop; longer ones take 14 to 18 agent calls and 10 to 15 minutes. The scripts need Python 3 and nothing
else.

## Usage

Give it the task or the text, and whatever material you have. Your own speech is the best material: answer a couple
of questions by voice and paste the transcript, in any language.

```
/ne-slop-text write a message to the hiring team for this job: <link>. My CV is cv.pdf. What I said about the project: <transcript>
/ne-slop-text fix this paragraph: <text>. What actually happened: <notes>
```

You get the text back, a few lines on what changed and why, the guard's verdict, and the questions the material could
not answer. The skill does not touch your files; drafts go next to them.

## Example: one paragraph, five ways (made with version 1)

Task: "Write one paragraph for my LinkedIn post about this bug we caught." Material: Boris's spoken answer in
Russian, in [`docs/examples/date-bug/context.md`](docs/examples/date-bug/context.md). Every paragraph below is a real
run, not edited by hand.

**From scratch.** Plain Opus, no method:

> I'm a QA tech lead at a fintech, and one of our products is an AI onboarding agent that registers users in WhatsApp.
> When we tested its very first prototype, I already knew one thing about language models: they don't reliably know
> what today's date is. So I wrote a test for the age boundary, using someone who had turned 18 about a month earlier
> and should be able to sign up without any trouble. The test failed. The model didn't know the current date and
> refused registration to people who were already old enough. We also check the agent's answers with
> LLM-as-a-judge, but this bug was caught by a plain boundary test, written because I knew where models tend to slip.

ne-slop-text, a draft from the material and one round of the loop:

> I know that a language model doesn't always know what today's date is. Someone who has barely turned 18 should
> already be able to sign up, but on the very first prototype of our WhatsApp onboarding agent the model didn't know
> the exact date and blocked people who were just over 18, by a month or so. So I wrote a test that fails on exactly
> that.

**Fixing an existing text.** The source is Sonnet's paragraph for the same task:

> One of the most valuable tests I've written as a QA tech lead caught a bug that no one would have thought to look
> for. Our fintech product has an AI onboarding agent in WhatsApp that registers new users, and on its first prototype
> the LLM didn't know today's date. Because of that, it refused registration to people who had turned 18 only about a
> month earlier. I knew that language models don't reliably know the current date, so I wrote a test for exactly that
> age boundary, and it failed on the prototype. It's a good reminder that when you test AI systems, you have to think
> about what the model fundamentally can't know, and that's why we also check the agent's answers with LLM-as-a-judge.

humanizer:

> One of the best tests I've written as a QA tech lead caught a bug nobody would have thought to look for. Our fintech
> product has an AI onboarding agent in WhatsApp that registers new users. On the first prototype the LLM didn't know
> today's date, so it refused to register people who had turned 18 only about a month earlier. Language models don't
> reliably know the current date. I knew that, so I wrote a test right on that age boundary, and the prototype failed
> it. With AI systems you have to think about what the model can't know, and that's why we also check the agent's
> answers with LLM-as-a-judge.

unslop:

> One of the most valuable tests I've written as a QA tech lead caught a date bug. Our fintech product has an AI
> onboarding agent in WhatsApp that registers new users, and on its first prototype the LLM didn't know today's date.
> Because of that, it refused registration to people who had turned 18 only about a month earlier. I knew that
> language models don't reliably know the current date, so I wrote a test for exactly that age boundary, and it failed
> on the prototype. When you test AI systems, you have to think about what the model fundamentally can't know, and
> that's why we also check the agent's answers with LLM-as-a-judge.

ne-slop-text, fix mode:

> I had to test the very first prototype of the AI agent that registers new users in WhatsApp for our fintech
> product. I know that a neural net doesn't always know what today's date is. If someone has only just turned 18, they
> should already be able to register, but the neural net didn't know the exact date and blocked registration for
> people a little over 18, by about a month. So I wrote a test that would fail on exactly that, and on the prototype
> it failed.

The surface lint finds nothing in any of the five. humanizer and unslop keep "one of the best (most valuable) tests"
and the closing lesson about what the model can't know. ne-slop-text puts Boris's own sentence in their place ("a
neural net doesn't always know what today's date is", from "нейронка не всегда знает, какое сегодня число") and stops
where the test fails. Reports and annotations are in [`docs/examples/date-bug/`](docs/examples/date-bug/).

## Blind test

```bash
python3 tools/blind.py out.html key.json "Title" "Subtitle" a=a.txt=label-a b=b.txt=label-b
```

The page shuffles the variants and evens out the typography: once, a human original was the only text with an em
dash, and a judge trained to read the dash as a sign of AI put it last. Rank the variants, press "collect" and paste
the result back to Claude. One judge cannot tell close variants apart (the same two texts swapped places from one day
to the next), so trust only large differences, or send the page to several people.

## Files

```
SKILL.md                 the pipeline, as Claude reads it
loop/writer.md           the skeleton first, then the text
loop/default_prompt.md   how to brief the three default writers
loop/overlap.py          what the draft takes from every default at once
loop/batch.py            numbered sentences for the annotator, ablation files
loop/scope.py            did the reviser touch only what it was allowed to
loop/annotator.md        sentence moves, by the codebook
loop/ablation.md         does a sentence carry anything
loop/reviser.md          edit, don't delete
loop/checker.md          truth and the skeleton
loop/reader.md           the clarity floor
gate/gate.py             the guard: still in the machine cloud?
gate/codebook.json       25 sentence moves, 5 text decisions
gate/models/             the metric's weights, en and ru
lint/lint.py             surface checks, en and ru
tools/blind.py           blind test page
learn/                   v1 marks, kept as history
docs/evidence.md         how the pipeline was found
```

## This README

The first version of this README went through version 1 of the skill. Three fresh agents (Opus, Sonnet, Haiku) wrote
their own READMEs from the same context, and all three opened like the first draft did: "A Claude Code skill for...".
One revision moved the game to the top and told the mechanism through the tests. That run is in `docs/readme-loop/`.
The version 2 sections were checked with the lint only.

## Credits

- Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. "StoryScope: Investigating
  idiosyncrasies in AI fiction". COLM 2026. arXiv:2604.03136.
- The humanizer and unslop skills: their pattern and word lists feed the lint.
- `ne-slop`, Boris's skill for creative work in general; this is its part for text.
