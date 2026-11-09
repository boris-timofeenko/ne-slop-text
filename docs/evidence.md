# How the pipeline was found

Three rounds of blind tests, November 2026. The judge was Boris, the person whose texts these were. He did not know
which variant came from which method until he had ranked them. The raw material stays private; the marks are in
`learn/marks.jsonl`.

## Before the tests

Boris had a CV that was partly his and partly written with Claude. He said text run through the humanizer skill was
recognisable "from a mile away", while his own `ne-slop` skill (written after a quest game where code-drawn graphics
came out alive) had a visible effect.

Three observations came before any judging:

- The unslop skill audited the CV and found nothing serious: no P0, no P1. Yet the CV read as partly machine-made.
  Rules catch what is in a text; they do not see what is missing.
- Opus, given a rich list of facts, wrote a clean, dry CV on its own. Slop does not need bad words.
- Lexical overlap with default generations did not separate the rewrites (12 to 20% of shared 3-grams, against 36 to
  39% between the defaults themselves). A collage of Boris's own phrases was the most lexically ordinary of all.

## Round 1: seven CV summaries

Current CV, humanizer, unslop, Opus from facts, a collage of Boris's phrases, an "engineer's log", a "voice" version.
Scores went 3 to 4 out of 5 across the board; Boris: "hard to say which one is not slop". At about 100 words, methods
do not separate. What he marked: sentences that list things, and sentences made for their sound, including his own old
line "can talk to engineers like an engineer". The eye judges form, not authorship.

## Round 2: one voice interview, five ways to turn it into text

Five open questions, answered by voice, unprepared. The answers had what no written source had given: an outside push
("management told us to go faster"), work inherited from the previous team, hedges ("on the whole it works"), one
specific bug (an AI agent that did not know today's date and turned away people who had just turned 18), and an
opinion about where QA is going.

| Place | Method |
|---|---|
| 1 | translation close to the speech |
| 2 | humanizer on top of 1 (almost unchanged) |
| 3 | "make it more professional" on top of 1 |
| 4 | raw: as much speech as possible, the joke kept |
| 5 | Opus writing from the same transcript in one pass |

The same fact, three forms: "I lead 3 QA engineers and sign off releases" was alive three times; "Lead a team of 3 QA
engineers and own release sign-off" and "Lead 3 QA engineers: 1-on-1s, performance reviews, sprint planning..." were
slop. Opus in one pass dropped the opinion and the push entirely. The joke, written as "The joke answer is...; the real
answer is...", became a device and was marked slop.

## Round 3: a letter with no text to start from

Task: "Message to the Hiring Team" for a QA role whose ad asks for stoic virtues and "an event where your stoicism was
proved". Every variant got the same context: the ad, the CV, the interview transcript.

- Four default writers (Opus twice, Sonnet, Haiku). The two Opus letters had the same skeleton down to the closing line,
  "I'd be glad to have that coffee". Haiku moved a bug to the wrong employer.
- A questionnaire of 21 discourse features, seeded from the StoryScope core features, each with a lean (machine-like or
  human-like).
- `consensus.py` flagged what the draft did together with every default and what leaned machine-like; a reviser fixed
  only that, under a list of allowed and forbidden moves.

| Place | Method |
|---|---|
| 1 | ne-slop draft plus one round of the loop |
| 2 | humanizer on top of the default (close to noise: nearly the same text as 5) |
| 3 | ne-slop draft without the loop |
| 4 | Claude by hand, with everything learned in rounds 1 and 2 |
| 5 | Opus default (Boris guessed it) |

The loop moved the ne-slop draft from third place to first. It cut three clever turns and three of four phrases quoted
from the ad, and kept the push, the bug and the opinion. It also cut one thing Boris liked: "Your ad asks for justice,
so I won't claim to be the best: I haven't met the other candidates". Hence the split between the brief's words used as
labels (machine-like) and used to answer it (human-like). The hand-written letter lost to the procedure; two of its
sentences were marked slop: one talked about the letter itself, one ended on an elliptical "...to one", a tic of mine
marked for the second time.

## The marks so far

39 sentences. No pattern got mixed labels.

- Slop: inventory (8), clever turn (4), resume-speak (2), process description (2), significance connective, colon reveal,
  staged joke, idiomatic paraphrase, text about itself.
- Alive: stance (6), plain first person (4), outside force (3), reader address (2), answering the reader in their own
  words, a specific episode.

## Limits

One judge, three tasks, one domain (job search). Ranks between near-identical texts are noisy. The questionnaire is
annotated by a model, which shares blind spots with the writers; the human stays the final judge.

## The night: a metric (version 2)

Three agents collected texts by talented authors written before 2022: 44 business letters and posts (12 authors),
48 engineering posts and README introductions (12), 47 pieces of Russian business and technical prose (13). Talent
was checked twice: by the author's standing and by two blind ratings without names, keeping the top 60 to 70%. For
each text an agent rebuilt the task as a list of facts, and Opus, Sonnet and Haiku wrote it: 417 defaults. Two pitfalls
found on the way: Sonnet sometimes reproduced a famous original almost word for word, and an author's name in the file
path doubled that copying, so the paths were made neutral.

Six agents compared human and default texts for the same task and listed where they part: 25 sentence moves and 5
text decisions (`gate/codebook.json`). 49 annotators labelled all 554 texts, sentence by sentence, without knowing
which was which. A logistic model on the move rates gives 0 for the mean talented human and 100 for the mean default.
On held-out authors it orders 92 of 100 human-model pairs correctly in letters, 95 in Russian, 78 in engineering
posts. In English a crude measure (sentence length, commas) does about as well; in Russian the moves do much better
(95 against 69). What separates the sides is mostly voice: asides, exclamations, slang, irony, questions and quoted
speech for people; recap endings, softeners, plain openings and slogans for models. Lists, resume-speak and self-praise
are as frequent in talented human texts as in defaults. Two annotators of the same text differ by about 13 points.

## Rounds 4 to 6: the metric against the reader

| Round | Task | Boris's top | The metric's top | Where the metric's top landed for Boris |
|---|---|---|---|---|
| v2 pages | letter, LinkedIn paragraph | loop "to authors" (letter), loop "to the mean" (paragraph) | "to authors" in both | 1st (letter), 4th of 5 (paragraph) |
| 4 | blog opening on Git scraping, from a fact list, the human original included | v2 "to the mean" | the human original | last |
| 5 | paragraph on flaky tests, no material at all | v1 | v2 "to authors" | last |
| 6 | the same two tasks, v2.1 added | default (flaky), v2 "to the mean" (git) | v1 (flaky); all within noise (git) | last (flaky) |

- Texts pushed down the metric lost their links and framing. In the letter the loop dropped the job title; in the
  paragraph on flaky tests the "to authors" text became a run of numbers and product names.
- The human original came last in round 4. It was the only text with an em dash; with typography evened out in round 6
  it came fourth of five. The dash was part of it, not all of it.
- Version 2.1 kept the story: beats that every edit must keep, edits instead of deletions, a reader's clarity floor,
  a truth check, and a band (only moves above the talented-human range count, and only in sentences an ablation check
  finds empty). It came second on both round 6 pages. Its band metric scored almost every text 0, so the gains came
  from the structure, not from the number.
- The same texts changed places between rounds 5 and 6 (v1 from 1st to 4th; the default from 2nd to 1st on one task and
  from 2nd to 5th on the other). One judge separates large differences, not close ones.
- Without the person's material, the default is not far behind: 2nd in rounds 4 and 5. Slop hurts most where the
  person is lost.

## Version 2

The guard (`gate/gate.py`) keeps the metric from round 1 of the night and asks it one question: is the draft within
annotator noise of the defaults' mean for this task? The loop takes the structure of v2.1, the writing rules of v1, and
`loop/overlap.py` for what the draft takes from every default at once (round 5: all three defaults opened with the
same Google figure).

Not established yet: whether v2 beats v1 for more than one judge; whether it works in other genres and in Russian
under blind judgement; whether outside readers or detectors take these texts for AI; how it does with nothing but a CV.

## Two test runs of version 2 (a letter from a CV only)

Two fresh agents ran the whole of SKILL.md on one task: "Why are you valuable to the company?" for a QA role, with
nothing but a CV and the job ad. Each logged every step and what was unclear or broken.

- First run: the reviser rewrote an opening it was not allowed to touch, and that edit alone flipped the guard's
  verdict. One annotator put the draft in the cloud and the other did not, and the whole difference was one label
  (a plain opening, about 12 points). Fixes: two annotators always, an UNCLEAR verdict instead of a tie-break, a scope
  check (`loop/scope.py`) that throws away a revision touching protected sentences, re-annotation of the draft
  together with the defaults, a task file with the target length and the gap format.
- Second run: the scope check passed, and the checker put back a fact the reviser had blurred. The draft had no
  model-like sentence left, yet both annotators kept it "in the cloud": the defaults of this task were themselves
  almost free of model moves, so no draft could get far enough below them. On letters written from a fact sheet the
  metric cannot separate anything. The guard now says so (NOT MEASURABLE) instead of sending the loop after a number.
- All three default writers saw that the ad requires "an event where your stoicism was proved" and left it out
  without a word. The draft showed it as a visible gap; the checker now reports every required element as present or
  as a gap.
