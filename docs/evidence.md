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
