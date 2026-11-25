---
name: ne-slop-text
description: Write or fix text for people so that it reads as written by a person, not by the average of the internet. v3 pipeline - the person's material or mandatory web research, the job of the text in one line, a draft held together by a chain of paragraphs, one rewrite from a positive example (Chekhov's letters for Russian), a sift by the author, then a form check and a surface lint. Works from a bare request with no context. Any language (examples and lint for Russian and English). Use for posts, announcements, newsletter pieces, letters, messages to hiring teams, bios, READMEs. Triggers - "не слоп", "ne-slop", "по-человечески", "живее", "звучит как ChatGPT", "sounds like AI", "unslop", "humanize", "fix this text", "write a post about".
---

# ne-slop-text v3

Slop is the text the reader could have got by giving the same request to any model. A model with no search writes
the template. A model that searches first writes better, but different agents bring back the same finds and arrive
at the same point. What a human reader then notices first is not the content at all: it is whether the text is one
continuous piece of telling or a list of finds, whether the opening is abrupt, whether the ending sags.

What the tests showed (details in `docs/evidence-v3.md`):
- Mandatory search plus a length limit plus a coherent telling is already most of the result. Nothing built on top
  of it beat it reliably in blind reading by a person.
- New content poured into a model's habitual moulds still reads as machine-written, and bans on constructions do
  not hold: the model takes the neighbouring one. A positive example works better. The author of the example
  decides: Chekhov's letters gave the best texts, a feuilletonist with a clipped line gave LinkedIn rhythm.
- Model judges do not predict a human reader, and a judge fitted to one reader's rankings did not transfer. The
  reader himself agreed with his own earlier ranking in two pairs out of three. Fine differences between decent
  variants are noise; only coarse ones are real.
- Scoring "expectedness" with a local model, default texts and a canon step cost most of the time and showed no
  gain. They are not in this version. Neither is the v2 loop (`loop/`, `gate/` stay in the folder as history; v2
  itself is installed as `ne-slop-text-v2`).

Scripts and briefs below are in this skill's folder; data files (task.md, facts.md, drafts) live next to the task.

## Inputs

- A task (what to write, for whom, where it will be published) or a source text to fix.
- Material, optional: documents, facts, the person's own words (voice transcripts, chats, notes).

## Mode

- Short (under ~80 words: chat replies, short messages, titles): Steps 0, 1, 3, 6.
- Full: all steps. One fresh agent, two to four minutes.

You (the session the user talks to) write the task file, search, plan and draft. One fresh agent does the form pass
and sees only the files named for it. Tell it not to use skills.

## Step 0. The task file

Write `task.md`: the request as given; who the reader is and what they already know about the subject; the JOB in
one line (what the reader does or knows after reading: an announcement makes people respond, an advice post helps
them decide, a greeting pleases one person); the word limit (250 for a social post or announcement, 350 for a blog
or newsletter piece, unless the task gives another); required elements; where the material is.

Everything below serves the JOB. A find that works against it is left out, however good.

## Step 1. Whose knowledge this is

1. **The person's material first.** What only this person has: an episode, an opinion, a number, their own wording.
   If it is there, the text is built from it and stays close to it.
2. **Requester-only knowledge is never guessed.** If the text speaks for an organisation or about a particular
   person (an announcement, a company post, a greeting) and their practice, rules, contacts, prices, dates or people
   are not in the material, write up to five questions to `questions.md`, ordered by how much the answer would
   change the text, and write a short text that holds whatever the answers are. General practice found on the web is
   not a fact about this requester: do not state it as "we do X".
3. If you can ask the user, ask one to three open questions that do not suggest the answer.

## Step 2. Facts

If the material does not cover the subject, searching is mandatory: 4 to 8 queries or page fetches. A model that is
merely allowed to search does not search. Prefer people's own words (forums, comments, postmortems), primary
records (documentation, statistics, price lists, timetables), dated events, and anything you can count or measure
yourself right now.

Write `facts.md`, one per line: `- <precise fact or verbatim words> | <URL> | page` or `| snippet`. `page` means you
opened the page and saw it there. Only `page` facts may appear in the text.

## Step 3. Plan and draft

Write `plan.md`: the point (one sentence you would say to this reader; it moves them toward the JOB) and the chain,
three to six lines, one per paragraph, each after the first starting with how it follows from the one before (`so`,
`but`, `because`, `for example`, `then`). A fact that does not fit the chain stays out.

Then write `draft.txt` along the chain:

- The first sentence stands where the reader stands (their question, doubt or situation); the point arrives by the
  end of the first paragraph together with its reason. No verdict, condition or command before the reader has
  ground for it, and no general introduction to the topic.
- One continuous piece of telling. At every paragraph break the reader can say why this comes next.
- At most two short quotes, each under fifteen words; the rest retold in your own words, without nicknames.
- The last paragraph is what the reader does next, as strong as the opening.
- Facts exact. An author's post names where a fact comes from, lightly, in the sentence. An organisation's own
  announcement does not cite articles or other organisations.
- Within the word limit. For a source text (fix mode): extract its JOB and chain into `plan.md`, keep every
  sentence that renders the person's material, and fix only what breaks the rules above.

## Step 4. Form pass (full mode)

Skip this step when the draft is built from the person's own words: rendering them close to the source beat every
rewrite in earlier tests, and a borrowed form would dissolve the voice.

Otherwise spawn one fresh agent (sonnet) with `form/form.md`, `task.md`, `plan.md`, `facts.md` and the output path
`form.txt`. It must not see `draft.txt`. It rewrites the same content from four pieces by one author in
`form/writers/`: `ru_chekhov` (his letters) for Russian, `en_twain` for English. It takes the way paragraphs hand
over and facts enter, never the vocabulary or the period. Do not let it choose a writer at random, and do not use
its text without Step 5.

In English the form pass changed little in tests; it may be skipped there.

## Step 5. Sift

Read `draft.txt` and `form.txt` yourself as the reader in `task.md`.

1. Throw out a version that is disjointed, reads as a list of finds, opens abruptly, or ends against the JOB.
2. Check every fact and quote in what remains against `facts.md` and the material; the form pass sometimes lets a
   `snippet` fact through. Cut or fix.
3. If both versions are decent, take `form.txt` and stop comparing. Do not spawn judges and do not run rounds: model
   judges do not predict a human reader, and fine differences between decent variants are below what a reader
   reproduces on a second reading.
4. If the text matters to the user, show both and let them choose.

## Step 6. Form check and lint

```bash
python3 lint/form.py FILE --limit 250
python3 lint/lint.py FILE --lang ru
```

`form.py` flags, with the offending line: more than one contrast pair, a clipped one-line opener of a paragraph, a
quote cut into pieces, more than two quotes or a long one, a trace of a private addressee, a short closing line,
the word limit. `lint.py` is the surface pass (stock phrases, inflated significance, explaining tails, em dash in
English); then read the lines it lists for checking by eye with `lint/ru.md` or `lint/en.md`. Fix a flagged
sentence by saying the thing straight, not by swapping in the neighbouring construction. The lint is a selection
from the humanizer and unslop lists; rewriting "with personality" is excluded on purpose.

Give the user: the text; the questions from `questions.md`, if any; one line on what was done (searched or built
from material, form pass used or skipped). Never edit the user's original files; write drafts next to them.

## Checking a version of the method

- Only blind reading by a person counts. `python3 tools/blind.py out.html key.json "Title" "Subtitle"
  name=path=label ...` builds a sheet; a sheet of about 2500 words is a comfortable sitting.
- Before trusting a difference, have the same person re-rank the same texts in a new order. In our test he matched
  himself in 14 pairs of 21. A difference he calls small is noise.
- Even the length limit across variants; a text twice as long wins on completeness alone.
- Do not report model-judge wins as quality. Use model readers only to screen out obvious failures.

## What not to do (each was tested)

- Opening with the most unexpected find. An announcement that recruits opened with "we ask you not to come".
- Cutting everything without a source. The author's own conclusion needs no source; only facts do.
- Banning constructions by list. A text with "no contrast pairs" opened with one.
- A random or "fitting" writer as the example. Short-line feuilletonists give broetry and lose the facts.
- "Write it as a private letter" with no example: unstable, and the private addressee leaks into a public post.
- Stating general practice as the requester's own. Ask instead.
- Chains of forum quotes with nicknames; quotes cut into a setup and a payoff.
- Scoring sentences for "expectedness" with a local model and optimising it; its maximum is copying the source.
- Optimising against model judges, or fitting a judge to a handful of human rankings.
- Everything in the v2 list still holds: chasing a metric, polishing toward the genre, performing voice, text about
  itself, a typographic tell.

## Where other approaches fit

- `ne-slop` (the parent skill, any creative work): Step 1 is its text part.
- `ne-slop-text-v2`: the loop against default texts with a guard metric. Use it by name when the text is built from
  the person's own long material and every empty sentence matters.
- unslop and humanizer: their pattern lists feed `lint/lint.py`; humanizer's rewriting with "personality and soul"
  is excluded.
