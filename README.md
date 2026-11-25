# ne-slop-text

Boris Timofeenko made a quest game, "Belgrade 2026", and its graphics came out alive: photos from his phone ruined by
a script, characters drawn in code, a hero cut out of a friend's photo with the white fringe of a magic eraser left
on. That became the `ne-slop` skill. For text it was not enough. Text run through the humanizer skill he could spot
from a mile away. In November 2026 he built this Claude Code skill with Claude, on his own texts (a CV, letters to
employers), and tested it blind on himself.

There are three versions now, and each can be installed on its own (see Versions below). Version 3, from November
2026, is the one `SKILL.md` describes. It is shorter than version 2: Boris read sixteen tasks blind, and most of what
had been built on top of a simple base made no difference to him.

## How version 3 works

You give a request ("write a post about X for Y"), with material or with none. Claude then goes through seven
steps.

1. **The task.** It writes down who the reader is, what they already know, and the job of the text in one line:
   what the reader does or knows after reading. It sets a word limit, 250 for a post or an announcement and 350 for
   a blog or newsletter piece.
2. **Whose knowledge.** Your own words, episodes and numbers come first, and the text stays close to them. Things
   only you can know (your prices, rules, dates, people) are never guessed. Claude writes up to five questions and
   a short text that holds whatever the answers turn out to be.
3. **Facts.** If the material does not cover the subject, Claude must search: 4 to 8 queries, every fact written
   down with its URL. A fact gets into the text only if Claude opened the page and saw it there.
4. **Plan and draft.** The point in one sentence, then a chain, one line per paragraph, each saying how it follows
   from the one before. The draft goes along the chain. It opens where the reader stands, carries at most two short
   quotes, and its last paragraph is what the reader does next.
5. **Form pass.** A fresh agent gets the plan and the facts, never the draft. It reads four letters by Chekhov
   (essays by Twain for English) and writes the same content again. It takes the way paragraphs hand over to each
   other and the way facts enter a sentence, and none of the vocabulary. This step is skipped when the text is
   built from your own words.
6. **Sift.** Claude reads both versions as the reader and throws out one that is disjointed or reads as a list of
   finds. Between two decent versions it takes the second and stops; if the text matters, it shows you both.
7. **Checks.** `lint/form.py` flags the moulds a model pours any content into: a second contrast pair, a clipped
   paragraph opener, a quote cut into setup and payoff, a short aphoristic ending, the word limit. `lint/lint.py`
   is the surface pass, a selection from the humanizer and unslop lists.

A full run takes two to four minutes and one extra agent. Short texts, under about 80 words, skip the search and
the form pass.

## Versions

| Version | Idea | Where |
|---|---|---|
| v3 | Search, the job of the text, a chain of paragraphs, a rewrite from Chekhov's letters, two checks | `main`, tag `v3` |
| v2 | A loop against what three default models write, with a learned metric as a guard; 10 to 15 minutes a text | tag `v2` |
| v1 | Compare the draft with three defaults and fix only what it shares with all of them | tag `v1` |

Version 2 is still worth calling when a text is built from your own long material and every empty sentence
matters. Each tag has a page under Releases.

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

Version 3 began with the question of what to do when there is no material at all, only a request. Sonnet wrote
sixteen tasks in several ways, and Boris ranked them on shuffled sheets with the key hidden. The base was plain:
search first, then write within a word limit. On top of it went a heavy content stage, where a local model scored
every find for how expected it was, and a form stage, where the text was written again from an author's example.
The content stage cost five to eight minutes a text and gave nothing on six new tasks. The form stage by Chekhov's
letters gave the best text in two tasks, on both readings; on three new tasks it came first once and last twice.
Other authors did worse: Doroshevich's clipped line produced LinkedIn rhythm and lost the facts.

Model judges had preferred the heavy method ten votes of twelve, and Boris did not. A judge fitted to 44 of his own
"better than" pairs stayed near chance on pairs it had not seen. When he ranked the same texts a second time in a
new order, he agreed with himself in 14 pairs of 21. So version 3 keeps what his remarks kept coming back to (a
lost thread, an abrupt opener, huge quotes, a sagging ending) and does not choose between decent variants.

One reader, a handful of tasks, mostly in Russian. Treat the numbers as a direction. The rounds, including what
failed, are in `docs/evidence.md` for versions 1 and 2 and in `docs/evidence-v3.md` for version 3.

## Install

```bash
git clone https://github.com/boris-timofeenko/ne-slop-text ~/.claude/skills/ne-slop-text
```

That gives version 3. For an older one, name its tag:

```bash
git clone --branch v2 https://github.com/boris-timofeenko/ne-slop-text ~/.claude/skills/ne-slop-text-v2
```

To keep two versions side by side, change `name:` at the top of the older `SKILL.md` to the folder's name, so that
the two do not answer to the same command.

Then ask Claude Code to write or fix a text "ne-slop" (or "не слоп"), or run `/ne-slop-text`. The scripts need
Python 3 and nothing else. The form pass needs Claude Code's subagents, and the search needs web access.

## Usage

Give it the task or the text, and whatever material you have. Your own speech is the best material: answer a couple
of questions by voice and paste the transcript, in any language.

```
/ne-slop-text write a message to the hiring team for this job: <link>. My CV is cv.pdf. What I said about the project: <transcript>
/ne-slop-text fix this paragraph: <text>. What actually happened: <notes>
/ne-slop-text напиши пост в телеграм-канал для бегунов-любителей: стоит ли бежать первый марафон без тренера
```

You get the text back, the questions the material could not answer, and one line on what was done: searched or
built from your material, form pass used or skipped. The skill does not touch your files; the task, the facts with
their URLs, the plan and both drafts lie next to them, so you can see where every sentence came from.

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
form/form.md             the brief for the form pass
form/writers/            four pieces each by Chekhov and Twain, with sources
lint/form.py             the form check
lint/lint.py             surface checks, en and ru
tools/blind.py           blind test page
docs/evidence-v3.md      what version 3 rests on

version 2, kept as history:
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
learn/                   v1 marks, kept as history
docs/evidence.md         how the pipeline was found
```

## This README

The first version of this README went through version 1 of the skill. Three fresh agents (Opus, Sonnet, Haiku) wrote
their own READMEs from the same context, and all three opened like the first draft did: "A Claude Code skill for...".
One revision moved the game to the top and told the mechanism through the tests. That run is in `docs/readme-loop/`.
The version 2 sections were checked with the lint only. The version 3 sections were written by its rules and
checked with both scripts, without the form pass.

## Credits

- Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. "StoryScope: Investigating
  idiosyncrasies in AI fiction". COLM 2026. arXiv:2604.03136.
- The humanizer and unslop skills: their pattern and word lists feed the lint.
- `ne-slop`, Boris's skill for creative work in general; this is its part for text.
