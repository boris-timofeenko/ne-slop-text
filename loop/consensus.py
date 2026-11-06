"""Where the draft sits in the machine cluster of this particular task.

A feature is flagged only when the draft's value leans machine-like (`lean` in the questionnaire).
P1: the defaults agree on it too (the local pull of the average). P2: by weight only.
Keep: the draft's value leans human; the reviser must not lose it.
Also prints the 4-grams the draft shares with the defaults and how close its opening sentence is to theirs.

usage: consensus.py questionnaire.json features.json[,more.json] D1,D2,D3 DRAFT [TEXTS_DIR]
features.json: {"<text_id>": {"<feature>": {"value": ..., "evidence": "..."}}}
TEXTS_DIR holds <text_id>.txt for the lexical checks.
"""
import collections
import difflib
import json
import re
import sys


def main():
    spec = {f["id"]: f for f in json.load(open(sys.argv[1]))["features"]}
    feats = {}
    for path in sys.argv[2].split(","):
        feats.update(json.load(open(path)))
    defaults = sys.argv[3].split(",")
    draft = sys.argv[4]
    texts_dir = sys.argv[5] if len(sys.argv) > 5 else None

    def value(t, f):
        x = feats[t].get(f)
        return x.get("value") if isinstance(x, dict) else x

    def evidence(t, f):
        x = feats[t].get(f)
        return x.get("evidence", "") if isinstance(x, dict) else ""

    def leans_ai(f, v):
        lean = f.get("lean", {})
        if "ai_if_over" in lean:
            return (v or 0) > lean["ai_if_over"]
        return v in lean.get("ai", [])

    groups = {"P1": [], "P2": [], "Keep": []}
    print(f"{'':6}{'feature':24}{'defaults':44}draft")
    for fid, f in spec.items():
        if "lean" not in f or fid not in feats[draft]:
            continue
        vals = [value(d, fid) for d in defaults]
        dv = value(draft, fid)
        ai = leans_ai(f, dv)
        if "ai_if_over" in f["lean"]:
            agree = sum(1 for v in vals if leans_ai(f, v)) >= len(vals) - 1
        else:
            mode, n = collections.Counter(json.dumps(v) for v in vals).most_common(1)[0]
            agree = n >= len(vals) - 1 and json.dumps(dv) == mode
        if ai and agree:
            tag = "P1"
        elif ai:
            tag = "P2"
        elif dv in f["lean"].get("human", []):
            tag = "Keep"
        else:
            tag = ""
        print(f"{tag:6}{fid:24}{str(vals):44}{dv}")
        if tag:
            groups[tag].append((fid, f["q"], dv, evidence(draft, fid)))

    if texts_dir:
        def words(t):
            return re.findall(r"[\w']+", t.lower())

        def grams(t):
            w = words(t)
            return {tuple(w[i:i + 4]) for i in range(len(w) - 3)}

        def first_sentence(t):
            body = [l for l in t.strip().splitlines() if l.strip()]
            if body and len(body[0].split()) <= 4 and body[0].rstrip().endswith(","):
                body = body[1:]  # skip "Hello team,"
            return re.split(r"(?<=[.!?])\s", " ".join(body), maxsplit=1)[0]

        text = {t: open(f"{texts_dir}/{t}.txt").read() for t in defaults + [draft]}
        shared = sorted(" ".join(g) for g in grams(text[draft]) & set().union(*[grams(text[d]) for d in defaults]))
        mine = grams(text[draft])
        print(f"\nshared 4-grams with defaults: {len(shared)}/{len(mine)} = {len(shared) / max(1, len(mine)):.2f}")
        print("; ".join(shared))
        op = first_sentence(text[draft])
        best = max(defaults, key=lambda d: difflib.SequenceMatcher(None, op.lower(), first_sentence(text[d]).lower()).ratio())
        r = difflib.SequenceMatcher(None, op.lower(), first_sentence(text[best]).lower()).ratio()
        print(f"\nopening: \"{op}\"\nclosest default opening ({best}, similarity {r:.2f}): \"{first_sentence(text[best])}\"")
        if r >= 0.45:
            groups["P1"].append(("opening", "The opening sentence is close to a default's opening.", op, ""))

    titles = {
        "P1": "P1: the draft does what the defaults do, and it leans machine-like",
        "P2": "P2: leans machine-like by weight",
        "Keep": "Keep: human-leaning, do not lose",
    }
    for key, items in groups.items():
        print(f"\n## {titles[key]}")
        for fid, q, dv, ev in items:
            print(f"- {fid} = {dv}: {q}" + (f' Example: "{ev}"' if ev else ""))


if __name__ == "__main__":
    main()
