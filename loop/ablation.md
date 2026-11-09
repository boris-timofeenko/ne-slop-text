# Ablation: does this sentence carry anything?

You get the task file (who the readers are and what they asked for) and a file made by `loop/batch.py ablate`: a full
text with numbered sentences and, for some sentences, the same text WITHOUT that sentence. For each such sentence,
compare the two versions and answer: does the version without it lose something these readers need, namely a fact, a
cause, a consequence, the turn of the story (the point where things stop being what they seemed), or the link between
the text and what the readers asked for? A sentence that only restates, announces, frames or sums up what is said
elsewhere loses nothing. A pronoun left without its referent ("these" with nothing before it) is not a loss: a
reviser fixes that with one word.

Write JSON to the path you are given:

```json
{"3": {"lost": true, "what": "turn: the flakiness may be in the product, not the test"},
 "7": {"lost": false, "what": "nothing: repeats sentence 6"}}
```

Read only the two given files; do not use skills. Reply with one line.

Then the orchestrator writes `{"DRAFT": [sentence numbers with lost = true]}` and passes it to `gate.py
--load-bearing`. Load-bearing sentences are not counted against the draft and the reviser may not touch them.
