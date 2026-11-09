# learn/

History from v1, kept for reference.

- `marks.jsonl`: 39 sentences Boris marked "slop" or "alive" in three blind tests, with a tag for the decision behind
  each (`patterns.md` explains the tags).
- In v1 these marks were meant to tune the questionnaire's weights. Later tests showed the marks are not stable: the
  same sentence was "alive" in one test and "slop" in another, depending on what stood next to it. v2 does not learn
  from them. Its guard (`gate/`) is trained on 139 talented human texts and 417 model defaults, and versions of the
  method are compared by blind ranking, trusting only large differences.
