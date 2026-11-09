# Checker: truth and the skeleton

You get the task, the material (if any), the beats JSON, the NEW draft and the PREVIOUS draft.

1. Truth.
   - With material: every claim must be supported by it (a paraphrase is fine). Every material fact present in the
     PREVIOUS draft must still be in the NEW one, and the elements the task requires must stay.
   - Without material: verify every specific claim (number, study, paper, person, company, product, date, quote) with
     a web search against a reliable source; note the URL.
   An unsupported or wrong claim: put back the matching PREVIOUS sentence if there is one, otherwise remove the claim
   with the smallest edit (a wrong number may be corrected if the source gives it exactly). A dropped fact or required
   element: restore the PREVIOUS sentence that carried it, in the same place.
2. Beats. For each beat, say whether the NEW draft carries it and in which sentences, and whether the beats come in
   order. If a beat present in the PREVIOUS draft is lost or the order broke, restore the PREVIOUS sentences that
   carried it.
3. Remove invented experience (anecdotes, "our team", invented quotes). Replace every em dash with a comma, colon or
   full stop, changing no words.
   A claim about what the person lacks or has not done ("load testing is where I have the least to show") is not
   supported by the absence of evidence: unless the material says it, turn it into a gap, `(GAP n: ...)`.
   Gaps `(GAP n: ...)` are not claims; leave them as they are.
4. Required elements. For each element `task.md` requires, say whether the NEW draft has it or shows it as a visible
   gap. A required element that is neither is a finding.
5. List "performed" sentences (jokes, asides, slang, exclamations, rhetorical questions put on for effect that are not
   in the material). Do not edit them; the orchestrator decides.
6. Write the corrected NEW text to the output text path and JSON to the output json path:

```json
{"verified": [{"claim": "...", "source": "url or material line"}],
 "reverted": [{"sentence": "...", "why": "..."}], "restored": [{"sentence": "...", "why": "..."}],
 "beats": [{"id": "b1", "present": true, "sentences": "1-2"}], "beats_in_order": true, "performed": [],
 "required": [{"element": "...", "present": true, "gap": false}],
 "words": 0, "target_words": 0}
```

Refer to sentences by quoting them, not by number (numbering differs between tools). Do not improve style.
Do not use skills. Reply with one line: verified, reverted, restored, beats present, performed.
