"""Number sentences for the annotator and build ablation files.

usage:
  batch.py texts OUT.txt SENTENCES.json ID=PATH [ID=PATH ...]
      one file with every text, sentences numbered [1], [2], ... (what the annotator reads),
      and SENTENCES.json = {"ID": ["sentence 1", ...]} (what gate.py --sentences reads for the counts)
  batch.py words PATH
      words of the body (no greeting, sign-off or gaps): what the target length in task.md counts
  batch.py ablate OUT.txt PATH N[,N,...]
      the full text with numbered sentences, then for each N the same text without sentence N
      (what the ablation agent reads)
"""
import json
import re
import sys


GREETING = re.compile(r"^(hello|hi|hey|dear|good (morning|afternoon)|здравствуйте|добрый день|привет)\b", re.I)
SIGNOFF = re.compile(r"^(best|regards|kind regards|best regards|thanks|thank you|cheers|sincerely|"
                     r"с уважением|спасибо|всего доброго)\b", re.I)


def _sentences(para):
    # keep "(GAP 1: ...)" and other parentheses whole: no split inside brackets
    protected = re.sub(r"\([^()]*\)", lambda m: m.group(0).replace(". ", ".\x00"), para)
    parts = re.split(r"(?<=[.!?…])[\"”»)]?\s+(?=[\"“«(]?[A-ZА-ЯЁ0-9])", protected)
    return [p.replace(".\x00", ". ").strip() for p in parts if p.strip()]


def split(text):
    """Sentences of the body. A greeting line and a sign-off or signature are not counted: they are the container,
    and counting them would dilute every per-sentence rate. Bullets are split into sentences too."""
    paras = [" ".join(p.split()) for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    if paras and len(paras[0].split()) <= 5 and (paras[0].endswith(",") or GREETING.match(paras[0])):
        paras = paras[1:]
    while paras and (SIGNOFF.match(paras[-1]) or (len(paras[-1].split()) <= 4 and not re.search(r"[.!?]$", paras[-1]))):
        paras = paras[:-1]
    out = []
    for para in paras:
        if para.startswith("- "):
            for item in re.split(r"\s(?=- )", para):
                out.extend(_sentences(item))
            continue
        out.extend(_sentences(para))
    return [s for s in out if not re.fullmatch(r"\(GAP[^()]*\)\.?", s)]  # a gap is not a sentence of the text


def body_words(text):
    """Words of the body: no greeting, no sign-off, no gaps. This is what the target length counts."""
    return sum(len(re.sub(r"\(GAP[^()]*\)", " ", s).split()) for s in split(text))


def numbered(sents, skip=None):
    return " ".join(f"[{i}] {s}" for i, s in enumerate(sents, 1) if i != skip)


def main():
    cmd = sys.argv[1]
    if cmd == "texts":
        out, side, items = sys.argv[2], sys.argv[3], sys.argv[4:]
        sents = {}
        with open(out, "w", encoding="utf-8") as f:
            for it in items:
                tid, path = it.split("=", 1)
                sents[tid] = split(open(path, encoding="utf-8").read())
                f.write(f"=== {tid} ({len(sents[tid])} sentences)\n{numbered(sents[tid])}\n\n")
        json.dump(sents, open(side, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print({k: len(v) for k, v in sents.items()})
    elif cmd == "words":
        print(body_words(open(sys.argv[2], encoding="utf-8").read()))
    elif cmd == "ablate":
        out, path, nums = sys.argv[2], sys.argv[3], [int(n) for n in sys.argv[4].split(",") if n]
        sents = split(open(path, encoding="utf-8").read())
        with open(out, "w", encoding="utf-8") as f:
            f.write(f"=== FULL TEXT\n{numbered(sents)}\n\n")
            for n in nums:
                f.write(f"=== WITHOUT SENTENCE [{n}]: \"{sents[n - 1]}\"\n{numbered(sents, skip=n)}\n\n")
        print(f"{len(nums)} ablations of {len(sents)} sentences -> {out}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
