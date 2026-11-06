"""Turn the user's marks into questionnaire weights.

Reads learn/marks.jsonl, counts slop/live per pattern tag and compares settled patterns with the `lean` of the
mapped feature in loop/questionnaire.json. Prints what agrees, what conflicts and which patterns have no feature yet.
It does not edit the questionnaire: weights change by hand, after a look at the examples.

usage: update_weights.py [marks.jsonl] [questionnaire.json]
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MARKS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "marks.jsonl")
QUEST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "loop", "questionnaire.json")

# pattern -> (feature, value that the pattern corresponds to); None = no feature, handled by a reviser rule
MAP = {
    "inventory": ("inventory_sentences", "count"),
    "clever_turn": ("clever_turns", "count"),
    "performed_joke": ("clever_turns", "count"),
    "resume_speak": ("resume_speak", "count"),
    "process_description": ("process_description", "count"),
    "significance_connective": ("significance_clauses", "count"),
    "colon_reveal": ("colon_reveals", "count"),
    "meta_about_text": ("meta_about_text", "count"),
    "stance": ("stance", True),
    "external_force": ("agency", "external_forces_present"),
    "reader_address": ("reader_address", True),
    "plays_reader_code": ("brief_words_to_answer", True),
    "answers_reader": ("opening_move", "answers_brief"),
    "specific_episode": ("episode_specificity", "specific"),
    "plain_first_person": None,
    "idiomatic_paraphrase": None,
}


def main():
    rows = [json.loads(l) for l in open(MARKS) if l.strip()]
    spec = {f["id"]: f for f in json.load(open(QUEST))["features"]}
    tally = collections.defaultdict(collections.Counter)
    for r in rows:
        tally[r["pattern"]][r["label"]] += 1
    print(f"{len(rows)} marks, {len(tally)} patterns\n")
    print(f"{'pattern':24}{'slop':>5}{'live':>5}  verdict      feature check")
    for p, c in sorted(tally.items(), key=lambda x: (-x[1]["slop"], -x[1]["live"])):
        s, l = c["slop"], c["live"]
        verdict = "slop" if s >= 2 and l == 0 else "live" if l >= 2 and s == 0 else "mixed" if s and l else "thin"
        m = MAP.get(p, "unmapped")
        if m == "unmapped":
            check = "no tag mapping: add it to MAP and learn/patterns.md" + (", propose a new feature" if verdict in ("slop", "live") else "")
        elif m is None:
            check = "reviser rule, no feature"
        else:
            fid, val = m
            lean = spec.get(fid, {}).get("lean")
            if fid not in spec:
                check = f"feature {fid} missing from the questionnaire"
            elif not lean:
                check = f"{fid}: no lean yet" + (f", set it to {verdict}" if verdict in ("slop", "live") else "")
            elif val == "count":
                ok = verdict != "live"
                check = f"{fid}: counts lean ai" + ("" if ok else " BUT marks say live: revisit")
            else:
                side = "ai" if val in lean.get("ai", []) else "human" if val in lean.get("human", []) else "none"
                want = {"slop": "ai", "live": "human"}.get(verdict)
                if want and side != want:
                    check = f"{fid}={val}: lean is {side}, marks say {verdict}: CHANGE"
                else:
                    check = f"{fid}={val}: lean {side}, ok"
        print(f"{p:24}{s:>5}{l:>5}  {verdict:12} {check}")


if __name__ == "__main__":
    main()
