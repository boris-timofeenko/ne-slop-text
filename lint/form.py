"""Form check for v3: the moulds a model pours any content into. Flags with the offending line, never rewrites.

usage: form.py FILE [--limit WORDS]
Exit code 1 if anything is flagged. No model, instant. Run before lint.py.
"""
import re
import sys

QUOTE = r"«[^»]+»|“[^”]+”|\"[^\"]+\""
CONTRAST = [
    r"\bне\b[^.!?\n]{1,70}?,\s+а\s", r"\bне\s+(?:просто|только)\b", r"\bа\s+не\b", r"\bвместо\b",
    r"\bэто\s+не\b[^.!?\n]{1,60}[,.—-]\s*(?:это|а)\b",
    r"\bnot\b[^.!?\n]{1,70}?,\s+but\b", r"\bnot (?:just|only)\b", r"\brather than\b", r"\binstead of\b",
    r"\b(?:isn['’]t|aren['’]t|wasn['’]t|not)\b[^.!?\n]{1,60}[.;—-]\s*(?:it|that|they)(?:['’]s|['’]re| is| are| was)\b",
]
ADDRESSEE = r"\bесли бы (?:ты|вы) спросил\w*|\bты (?:спрашивал\w*|просил\w*)\b|\byou asked\b|\bif you asked me\b"


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?…])\s+", text.replace("\n", " ")) if s.strip()]


def main():
    text = open(sys.argv[1]).read()
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    flags = []
    sents, paras = sentences(text), paragraphs(text)

    contrasts = [s for s in sents if any(re.search(p, re.sub(QUOTE, " ", s), flags=re.I) for p in CONTRAST)]
    if len(contrasts) > 1:
        flags += [("contrast pair (more than one in the text)", s) for s in contrasts]
    for p in paras:
        first = sentences(p)[0]
        if len(first.split()) <= 3 and first[-1] in ".!" and len(sentences(p)) > 1:
            flags.append(("clipped opener of a paragraph", first))
    for s in sents:
        if len(re.findall(QUOTE, s)) >= 2:
            flags.append(("quote cut into pieces inside one sentence", s))
        if re.search(ADDRESSEE, s, flags=re.I):
            flags.append(("trace of a private addressee", s))
    quotes = re.findall(QUOTE, text)
    for q in quotes:
        if len(q.split()) > 15:
            flags.append(("quote longer than fifteen words: retell it", q))
    if len(quotes) > 2:
        flags.append((f"{len(quotes)} quotes in the text, at most two: retell the rest", ""))
    for p in paras:
        if len(re.findall(QUOTE, p)) > 1:
            flags.append(("more than one quote in a paragraph", p[:160]))
    last = sents[-1] if sents else ""
    if len(last.split()) <= 6 and not re.search(r"\d|@|http", last):
        flags.append(("short closing line: an aphorism or an afterthought?", last))
    words = len(text.split())
    if limit and words > limit:
        flags.append((f"{words} words, limit {limit}", ""))

    for why, line in flags:
        print(f"[{why}] {line[:200]}".rstrip())
    print(f"\n{words} words, {len(flags)} flag(s)")
    sys.exit(1 if flags else 0)


if __name__ == "__main__":
    main()
