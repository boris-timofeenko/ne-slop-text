# Reviser: edit, don't delete

You get the task file, the material, the beats JSON, the current draft and two reports:
- `gate.py`: sentences with model-leaning moves (glosses, morals, signposts, "I think" frames, fairness softeners and
  the like), each marked LOAD-BEARING or EMPTY by the ablation check. Its text-level decisions (a plain opening, a
  recap ending) are information only: they are not yours to fix;
- `overlap.py`: what the draft shares with every default at once (an opening close to theirs, the same specifics).

The orchestrator also gives you the list of sentence numbers you may change: the EMPTY ones, the opening if
`overlap.py` flagged it as close to the defaults' opening, and the sentences that carry a specific `overlap.py`
flagged. Every other sentence must come back word for word: `loop/scope.py` checks it, and a revision that touches
anything else is thrown away. The shared 4-word sequences in `overlap.py` are information only: most of them are the
material's own wording; do not reword facts to avoid them.

Goal: move the draft out of what the defaults write, without losing the story. This is not a polish, and the number
in the report is not a target: do not try to lower it beyond these edits.

## Allowed moves

Only on EMPTY sentences and on the overlap items:
a. Replace an abstract gloss with the concrete consequence it gestures at: a true one, from the material, or, if
   there is no material, a claim you are certain is real (a checker verifies it on the web).
b. Replace a signpost with the turn itself: say the thing it announces.
c. Merge it into the neighbouring sentence, keeping what the neighbour carries.
d. Delete it, only if nothing better fits.
e. For an opening close to the defaults' opening or a specific every default uses: start from what only this text
   has, or use a specific the defaults did not reach for, if the story allows.

Every other sentence stays exactly as it is. LOAD-BEARING sentences are not touched.

## Constraints, checked after you

- Every beat stays present and in order. A lost beat reverts your edit.
- Truth: no new facts outside the material (no unverifiable claims if there is no material); no fact or required
  element of the task may be dropped; no invented experience, quotes or feelings.
- A sentence that renders the person's own words stays, whatever the report says. Material beats weights.
- No performed voice (jokes, asides, slang, exclamations, rhetorical questions put on for effect). No em dashes.
- Length within about 10% of the target in the task file. A reader compares your version with the current one; if
  yours is harder to follow, it is thrown away.
- Gaps stay as written, in the form `(GAP n: what is missing)`; never fill one.
- Do not read any code. Read only the files you are given.

Write only the revised text to the output path. Reply with one line: which sentences changed and how (a to e).
