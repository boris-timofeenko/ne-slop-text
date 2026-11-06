"""Surface lint: the last and weakest pass. Flags, never rewrites.

usage: lint.py FILE [--lang en|ru]
Exit code 1 if anything is flagged.
"""
import re
import sys

COMMON = [
    (r"\b(?:to|for|with) one\.\s*$", "elliptical clever ending ('...hands tickets to one.')"),
]

EN = [
    (r"—", "em dash"),
    (r"\s--\s", "double hyphen used as a dash"),
    (r"\bnot (?:just|only|merely)\b[^.]{0,80}\bbut\b", "'not just X but Y'"),
    (r"\b(?:it's|it is|this is|that's) not\b[^.]{0,60}[,;] (?:it's|it is|but)\b", "negative parallelism"),
    (r",\s+(?:ensuring|enabling|highlighting|underscoring|showcasing|reflecting|fostering|demonstrating|emphasizing)\b",
     "trailing -ing clause that explains significance"),
    (r"\b(?:that|this) (?:means|shows|proves|demonstrates)\b", "connective that explains meaning"),
    (r"\b(?:delve|tapestry|testament|leverag\w*|seamless\w*|robust|passionate|thrilled|vibrant|pivotal|crucial|"
     r"elevate|unlock|game[- ]changer|cutting[- ]edge|synerg\w*|spearhead\w*|meticulous\w*|landscape)\b",
     "AI vocabulary"),
    (r"\b(?:excited to|eager to|love to|drawn to)\b", "performed enthusiasm"),
    (r"\b(?:in today's|in the world of|in an era of|let's dive|here's the thing|the best part|at the end of the day)\b",
     "stock phrase"),
    (r"\b(?:the (?:joke|honest|short|real) answer is)\b", "staged answer"),
    (r"\b(?:since you asked|as you asked|first, since)\b", "text about itself"),
    (r"\b(?:own(?:ed)?|drove|spearheaded) (?:the )?(?:release|process|quality|roadmap|strategy)", "resume-speak"),
    (r"^\s*(?:led|lead|owned|drove|spearheaded|managed) (?:a team of|the)\b", "subject-less resume fragment"),
    (r"\b(?:I'd be (?:glad|happy) to|looking forward to)\b[^.]*\b(?:discuss|chat|talk|coffee|hearing)\b",
     "closing call to action"),
]

RU = [
    (r"\bне просто\b[^.]{0,80}\bа\b", "«не просто X, а Y»"),
    (r"\bэто не\b[^.]{0,60}[,—–-]\s*это\b", "«это не X, это Y»"),
    (r"\b(?:погрузитесь|откройте для себя|давайте разберёмся|давайте разберемся|в мире, где|в эпоху)\b", "штамп"),
    (r"\b(?:стоит отметить|важно понимать|следует подчеркнуть|не секрет, что|как известно)\b", "вводная-пустышка"),
    (r"\b(?:играет (?:важную|ключевую) роль|является (?:ключевым|важным)|настоящий прорыв|уникальн\w+)\b", "раздувание значимости"),
    (r",\s+(?:обеспечивая|подчёркивая|подчеркивая|демонстрируя|позволяя|отражая)\b", "деепричастный хвост-объяснение"),
    (r"\b(?:это значит|это показывает|это доказывает)\b", "связка-объяснение"),
    (r"\b(?:с радостью|с огромным удовольствием|вдохновляет)\b", "сыгранная эмоция"),
]


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+|\n\s*\n", text) if s.strip()]


def unquoted(s):
    """Quoted examples are data, not the author's prose: a text about slop may quote slop."""
    s = re.sub(r"`[^`]*`", " ", s)
    s = re.sub(r"\"[^\"]*\"|“[^”]*”|«[^»]*»", " ", s)
    return s


def main():
    path = sys.argv[1]
    lang = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else "en"
    rules = COMMON + (RU if lang == "ru" else EN)
    text = open(path).read()
    hits = 0
    prose = [s for s in sentences(text) if not s.lstrip().startswith(("|", "#", "```"))]
    for s in prose:
        for pattern, why in rules:
            if re.search(pattern, unquoted(s), flags=re.IGNORECASE | re.MULTILINE):
                hits += 1
                print(f"[{why}] {s.strip()[:160]}")
    antitheses = len(re.findall(r"\bnot\b[^.]{0,40}, but\b|\bне\b[^.]{0,40}, а\b", unquoted(text), flags=re.IGNORECASE))
    if antitheses > 1:
        hits += 1
        print(f"[more than one antithesis in the text: {antitheses}]")
    colon_lines = [s for s in prose if re.search(r"\w: [a-zа-я]", unquoted(s)) and unquoted(s).count(",") >= 2]
    for s in colon_lines:
        print(f"[check: colon reveal?] {s.strip()[:160]}")
    print(f"\n{hits} flag(s)" + (f", {len(colon_lines)} colon(s) to check by eye" if colon_lines else ""))
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
