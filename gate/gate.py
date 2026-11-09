"""Machine-cloud check: the metric as a guard, not a target.

The metric (M1) was fitted on 139 talented human texts and 417 model defaults written for the same tasks: it
weighs sentence "moves" (gloss, moral, signpost, aside, question...) and a few text-level decisions. 0 = mean talented
human, 100 = mean model default. It tells a default from a non-default well (held-out authors: 92 of 100 pairs right
in letters, 95 in Russian, 78 in engineering posts). It does NOT rank good texts the way a reader does: texts pushed
down its scale got worse in blind tests. So it is only asked one question here: is the draft still in the machine
cloud of this task?

Input: one JSON with annotations of the draft and the task's defaults, all made by the same annotator in one batch:
  {"DRAFT": {"n": 9, "s": {"1": ["gloss"], "4": ["signpost"]}, "t": {"opening": "plain_setup", ...}},
   "D1": {...}, "D2": {...}, "D3": {...}}
n = number of sentences; s = moves per sentence (1-based); t = text-level decisions (see codebook.json).
Optional --load-bearing FILE: {"DRAFT": [3, 5]} = sentences an ablation check found load-bearing (removing them
loses a fact, a cause, a consequence or a turn); they are not counted against the draft.

--sentences FILE (from loop/batch.py) sets n for every text, so the annotator does not have to count.

Pass one annotations file per annotator (two for a text that matters). The verdict is "in the cloud" only if every
annotator puts the draft there; if they disagree it is UNCLEAR, and the loop must not edit to settle it: one
text-level label (a plain opening is worth about 12 points) can flip a verdict, which is the size of the noise.

usage: gate.py ANN_A.json [ANN_B.json ...] [--lang en|ru] [--draft DRAFT] [--load-bearing FILE] [--sentences FILE]
Exit code: 0 out of the cloud, 1 in the cloud, 2 unclear.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CODEBOOK = json.load(open(os.path.join(HERE, "codebook.json"), encoding="utf-8"))
SMOVES = [m["id"] for m in CODEBOOK["sentence_moves"]]
ALIAS = {"drumbeat": "drumbeat_list", "claim_or_verdict": "other", "voice_or_quote": "other"}
REGISTER = {"neutral_written": 0.0, "neutral_with_drops": 1.0, "marked_voice_held": 2.0}
NOISE = 13.0  # mean disagreement between two annotators of the same text, in points


def clean(a, skip=()):
    s = {}
    for k, moves in (a.get("s") or {}).items():
        if int(k) in skip:
            continue
        ms = sorted({ALIAS.get(m, m) for m in moves} & set(SMOVES))
        if ms:
            s[int(k)] = ms
    t = {k: ALIAS.get(v, v) if isinstance(v, str) else v for k, v in (a.get("t") or {}).items()}
    return s, t


def features(a, skip=()):
    s, t = clean(a, skip)
    n = max(int(a.get("n") or 1), 1)
    x = {m: 0.0 for m in SMOVES}
    for moves in s.values():
        for m in moves:
            x[m] += 1.0 / n
    for k, v in t.items():
        if k == "register":
            x["register_marked"] = REGISTER.get(v, 0.0)
        else:
            x[f"{k}={v}"] = 1.0
    return x, s, t, n


def m1(model, x):
    d = model["intercept"] + sum(f["coef"] * (x.get(f["feature"], 0.0) - f["mean"]) / f["scale"]
                                 for f in model["features"])
    return 100.0 * (d - model["zh"]) / (model["zd"] - model["zh"])


def points(model, feature, n=1):
    unit = 100.0 / (model["zd"] - model["zh"])
    for f in model["features"]:
        if f["feature"] == feature:
            return unit * f["coef"] / f["scale"] / (n if f["sentence_level"] else 1)
    return 0.0


def band_excess(model, x):
    b = model.get("band")
    if not b:
        return None, {}
    over = {}
    raw = 0.0
    for name, m in b["moves"].items():
        e = max(0.0, x.get(name, 0.0) - m["q75"])
        if e > 0:
            over[name] = round(100.0 * m["weight"] * e / b["norm"], 1)
            raw += m["weight"] * e
    return round(100.0 * raw / b["norm"], 1), over


def main():
    args = sys.argv[1:]
    opt = {}
    for key in ("--lang", "--draft", "--load-bearing", "--sentences"):
        if key in args:
            i = args.index(key)
            opt[key] = args[i + 1]
            del args[i:i + 2]
    model = json.load(open(os.path.join(HERE, "models", f"{opt.get('--lang', 'en')}.json"), encoding="utf-8"))
    draft = opt.get("--draft", "DRAFT")
    sents = json.load(open(opt["--sentences"], encoding="utf-8")) if "--sentences" in opt else {}
    lb = set()
    if "--load-bearing" in opt:
        lb = set(json.load(open(opt["--load-bearing"], encoding="utf-8")).get(draft, []))

    print(f"metric (0 = talented human, 100 = model default), lang {model['model']}, annotator noise ±{NOISE:.0f}")

    def sentences_only(x):  # the part the loop may act on: sentence moves, without opening/closing/register labels
        return {k: v for k, v in x.items() if k in SMOVES}

    floor = m1(model, {})  # a text with no sentence moves at all
    verdicts, full_verdicts, flat, leaning, text_level = [], [], [], {}, {}
    for path in args:  # one file per annotator; each must hold the draft and the defaults from one batch
        ann = json.load(open(path, encoding="utf-8"))
        for tid, ss in sents.items():
            if tid in ann:
                ann[tid]["n"] = len(ss)
        defaults = [k for k in ann if k != draft]
        x, s, t, n = features(ann[draft], skip=lb)
        line = f"\n[{os.path.basename(path)}]"
        for label, f, store in (("by sentences", sentences_only, verdicts), ("with text-level labels", lambda v: v,
                                                                              full_verdicts)):
            scores = {k: m1(model, f(features(ann[k])[0])) for k in defaults}
            mean_d = sum(scores.values()) / max(len(scores), 1)
            ds = m1(model, f(x))
            store.append(ds > mean_d - NOISE)
            if store is verdicts and mean_d - NOISE <= floor + 0.5:
                flat.append(True)  # the defaults sit within noise of a text with no moves: nothing to separate
            line += (f"\n  {label:24} defaults " + ", ".join(f"{k} {v:.1f}" for k, v in sorted(scores.items()))
                     + f"; mean {mean_d:.1f}; draft {ds:.1f} (needs < {mean_d - NOISE:.1f}): "
                     + ("IN" if store[-1] else "out"))
        print(line)
        for i, moves in clean(ann[draft])[0].items():  # all model-leaning sentences, load-bearing included
            p = sum(points(model, m, n) for m in moves)
            if p > 0:
                leaning.setdefault(i, set()).update(m for m in moves if points(model, m, n) > 0)
        for k, v in t.items():
            pts = points(model, f"{k}={v}") if k != "register" else 0
            if pts:
                text_level.setdefault(f"{k}={v}", []).append(round(pts, 1))
        total, over = band_excess(model, x)
        if total is not None:
            print(f"  above the talented-human range: {total} {over or ''}")

    if flat and len(flat) == len(verdicts):
        verdict, code = (f"NOT MEASURABLE on this task: the defaults' sentences are within noise of a text with no moves"
                         f" ({floor:.1f}), so the metric cannot tell the draft from them. Rely on overlap.py and the"
                         " reader; do not edit for the metric."), 3
    elif all(verdicts):
        verdict, code = "STILL IN THE MACHINE CLOUD by its sentences (every annotator agrees)", 1
    elif not any(verdicts):
        verdict, code = "out of the machine cloud by its sentences (every annotator agrees)", 0
    else:
        verdict, code = "UNCLEAR: the annotators disagree. Do not edit to settle it; report it to the user.", 2
    print(f"\nVERDICT: {verdict}")
    if all(full_verdicts) and not all(verdicts):
        print("NOTE: with the opening/closing labels counted, every annotator puts the draft IN the cloud. The labels"
              " alone do it (a plain opening is worth about 12 points). Tell the user; the opening may be rewritten"
              " once only if overlap.py flagged it as close to the defaults' opening.")

    draft_sents = sents.get(draft, [])
    print("\nsentences with model-leaning moves (from any annotator):")
    if not leaning:
        print("  none")
    for i in sorted(leaning):
        state = "LOAD-BEARING (do not touch)" if i in lb else ("EMPTY (may be edited)" if "--load-bearing" in opt
                                                                else "not checked yet")
        text = draft_sents[i - 1][:100] if 0 < i <= len(draft_sents) else ""
        print(f"  [{i}] {state:28} {', '.join(sorted(leaning[i])):28} {text}")
    unchecked = sorted(i for i in leaning if "--load-bearing" not in opt)
    if unchecked:
        print(f"\nto ablate: {','.join(map(str, unchecked))}")
    if text_level:
        print(f"text-level decisions that pull toward the defaults (information only, not an edit target): {text_level}")
    print("\nThis is a check, not a target: do not chase the number. Only EMPTY sentences may be edited, never by adding"
          " voice the material does not have.")
    sys.exit(code)


if __name__ == "__main__":
    main()
