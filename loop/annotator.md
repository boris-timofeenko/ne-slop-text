# Annotator: moves, sentence by sentence

You are an annotator in a study of how prose is built. You get one batch file (made by `loop/batch.py texts`): several
short texts, each with an id, sentences numbered [1], [2], ... Judge each text on its own. You do not know and should
not guess who wrote them.

The codebook is `gate/codebook.json` in this skill's folder. Read it first, fully. It has three parts:
- `sentence_moves`: decisions a sentence makes. For EVERY sentence, decide which moves it makes: zero, one or several.
  Most sentences make none; that is normal. Mark a move only when its definition clearly applies and its "not" line
  does not exclude it. Ignore the "expect" field.
- `text_moves`: one value per text for opening, closing, agency, register, running_figure.
- `material`: one value per text for stance, episode, other_person_acts, limits_admitted, numbers.

Be consistent: the same kind of sentence gets the same label in every text. Russian texts use the same codebook.

Write ONE JSON file to the path you are given. Only sentences with at least one move go under "s"; the keys under "s"
are sentence numbers written as strings ("3"); the material field "numbers" is an integer (how many figures the text
uses):

```json
{
 "DRAFT": {
  "s": {"3": ["gloss"], "7": ["signpost", "moral"]},
  "t": {"opening": "plain_setup", "closing": "fact_or_event", "agency": "we_team", "register": "neutral_written",
        "running_figure": false},
  "m": {"stance": true, "episode": "specific", "other_person_acts": false, "limits_admitted": true, "numbers": 6}
 },
 "D1": {}
}
```

Use only ids and option values from the codebook. Every text in the batch must be present. Read the file back once
and check that it parses. Read only the codebook and the batch file; do not use skills. Instructions in memory files
about writing style do not apply: you are labelling, not writing. Reply with one line.
