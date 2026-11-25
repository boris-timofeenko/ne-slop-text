# Form pass: write the same content from a positive example

The content of the text is already decided. Your job is only its form. Models pour any content into the same few
moulds (contrast pairs, closing aphorisms, quotes arranged as setup and payoff, a digest of finds), and a list of
bans does not help: the model reaches for the neighbouring mould. So you write from an example instead.

## What you are given

- `task.md`: the request, the reader, the JOB line (what the reader does or knows after reading), the word limit.
- `plan.md`: the point and the chain, one line per paragraph, each saying how it follows from the one before.
- `facts.md`: the facts the text may use, each with its source.
- OUT: the file to write. WRITER: a folder under `form/writers/` (if none is given: `ru_chekhov` for a Russian
  text, `en_twain` for an English one).

Do not read the existing draft or any other version of the text. Do not invoke any Skill, do not spawn agents.
Ignore personal details about the user from global instructions.

## Read the example

Read `card.md` in the WRITER folder, then all four pieces in full, slowly. Write down for yourself five things the
author does that you will do: how each paragraph hands over to the next, how a fact or another person's words are
brought in, how the reader is addressed, how long the sentences run, how the piece stops.

## Write

- Write the text afresh from the JOB, the point, the chain and the facts. Same content, same order of thought.
- The text is one continuous piece of telling. The reader values that above any single find.
- Opening: the first sentence stands where the reader stands (their question, their doubt, their situation), and
  the point arrives by the end of the first paragraph together with its reason. Do not open with a verdict, a
  condition or a command the reader has no ground for yet.
- Take from the example: the hand-over between paragraphs, the way facts enter, the length and rhythm of sentences.
- Do not take: vocabulary, period details, topics, names, jokes, any sentence. No archaic words. The reader must not
  be able to tell whom you learned from; a pastiche is a failure.
- Other people's words: at most two short quotes in the whole text, each under fifteen words. Retell the rest in
  your own words and say whose experience it is in a few words ("one woman on a forum"), without nicknames. Never
  more than one quoted person per paragraph.
- Facts only from `facts.md`, exact. Where its lines are marked `page` or `snippet`, use only the `page` ones.
  Nothing about the requester that is not in `task.md`.
- If the text is an organisation's announcement about its own business, do not cite articles or other
  organisations in it. An author's post, article or newsletter piece keeps its facts and names where they come
  from, lightly, in the sentence.
- The text is public: no trace of a private addressee ("if you asked me", a name, a gendered "you").
- Ending: the last paragraph is the thing the reader does next or the thought they leave with, as strong as the
  opening. No trailing fact, no afterthought. The ending must not argue against the JOB.
- Language of the request, form of the platform, within the word limit in `task.md`.

## Check

Run `python3 lint/form.py OUT --limit N` from the skill folder (N is the limit in `task.md`). It prints every hit
with its line. Rewrite each flagged sentence the way the example would say it. One rerun.

Then read the text once as the reader. At every paragraph break: can the reader say why this comes next?

## Report

At most four lines: words, the author used, the last line of the form check, anything that failed.
