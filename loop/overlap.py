"""What the draft takes from every default at once.

Models writing the same task converge: in one test all three opened a paragraph about flaky tests with the same
sentence shape and the same Google statistic. This script finds, without any model:
- the opening: how close the draft's first sentence is to each default's first sentence;
- shared specifics: numbers and capitalised names that EVERY default uses and the draft uses too
  (the facts everyone reaches for first);
- shared phrasing: 4-word sequences the draft shares with the defaults.
A hit is not an error by itself (a required fact may be shared). It is a place to look: is it there because the
story needs it, or because it came first?

Specifics that are in the material (--material FILE, repeatable) are the person's facts: the defaults use them because
they were given, so they are listed apart and never flagged. Numbers written in words count as numbers.

usage: overlap.py DRAFT.txt DEFAULT1.txt DEFAULT2.txt [DEFAULT3.txt ...] [--material FILE ...]
"""
import difflib
import re
import sys

STOP = set("""a an the and or but if of to in on at by for with from as is are was were be been it its this that these
those i we you he she they them our your their my me us not no so than then there here into out up about over after
before when what which who how why do does did have has had can could will would should may might just also only very
и в во не что он на я с со как а то все она так его но да ты к у же вы за бы по только ее мне было вот от меня еще
нет о из ему теперь когда даже ну вдруг ли если уже или ни быть был него до вас нибудь опять уж вам ведь там потом
себя ничего ей может они тут где есть надо ней для мы тебя их чем была сам чтоб без будто чего раз тоже себе под
будет ж тогда кто этот того потому этого какой совсем ним здесь этом один почти мой тем чтобы нее сейчас были куда
зачем всех никогда можно при наконец два об другой хоть после над больше тот через эти нас про всего них какая много
разве три эту моя впрочем хорошо свою этой перед иногда лучше чуть том нельзя такой им более всегда конечно всю между""".split())


def first_sentence(t):
    lines = [l for l in t.strip().splitlines() if l.strip()]
    if lines and len(lines[0].split()) <= 4 and lines[0].rstrip().endswith(","):
        lines = lines[1:]  # "Hello team,"
    return re.split(r"(?<=[.!?])\s", " ".join(lines), maxsplit=1)[0]


def words(t):
    return re.findall(r"[\w'’]+", t.lower())


def grams(t, n=4):
    w = words(t)
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)} - {g for g in [()] }


NUMBER_WORDS = {"two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
                "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "twenty": "20", "hundred": "100",
                "thousand": "1000", "два": "2", "две": "2", "три": "3",
                "четыре": "4", "пять": "5", "шесть": "6", "семь": "7", "восемь": "8", "девять": "9", "десять": "10",
                "полтора": "1.5", "полторы": "1.5"}


def specifics(t):
    low = t.lower()
    for w, d in NUMBER_WORDS.items():
        low = re.sub(rf"\b{w}\b", d, low)
    nums = {n.strip().rstrip(".,") for n in re.findall(r"\d[\d,.]*\s?%?", low) if n.strip().rstrip(".,")}
    names = set()
    for s in re.split(r"(?<=[.!?])\s+", t):
        toks = re.findall(r"[A-ZА-ЯЁ][\w'’.-]*", s)
        first = re.match(r"\W*([\w'’.-]+)", s)
        for tok in toks:
            tok = tok.strip(".")
            if first and tok == first.group(1).strip("."):
                continue  # sentence-initial capital
            if tok.isupper() and len(tok) <= 3:
                continue  # AI, CI, QA, API: domain words, not specifics
            if tok.lower() not in STOP:
                names.add(tok)
    return nums | names


def main():
    args = sys.argv[1:]
    material = []
    while "--material" in args:
        i = args.index("--material")
        material.append(open(args[i + 1], encoding="utf-8").read())
        del args[i:i + 2]
    if len(args) < 2:
        sys.exit(__doc__)
    draft = open(args[0], encoding="utf-8").read()
    defaults = [open(p, encoding="utf-8").read() for p in args[1:]]
    names = args[1:]

    def opening_sim(a, b):  # by words, not characters
        return difflib.SequenceMatcher(None, words(a), words(b)).ratio()

    op = first_sentence(draft)
    print(f"draft opening: \"{op}\"")
    flag = False
    for n, d in zip(names, defaults):
        r = opening_sim(op, first_sentence(d))
        mark = "  <- close" if r >= 0.45 else ""
        flag |= r >= 0.45
        print(f"  {r:.2f} {n}: \"{first_sentence(d)[:110]}\"{mark}")
    pair = [opening_sim(first_sentence(a), first_sentence(b)) for i, a in enumerate(defaults) for b in defaults[i + 1:]]
    if pair:
        print(f"  the defaults' openings among themselves: {sum(pair) / len(pair):.2f} on average"
              + ("  <- they open the same way" if sum(pair) / len(pair) >= 0.45 else ""))

    given = {g.lower() for g in set().union(*[specifics(m) for m in material])} if material else set()
    common = set.intersection(*[specifics(d) for d in defaults])
    from_material = sorted(c for c in common if c.lower() in given)
    shared = sorted(c for c in common & specifics(draft) if c.lower() not in given)
    print(f"\nspecifics every default uses: {sorted(c for c in common if c.lower() not in given) or 'none'}"
          + (f" (from the material, not flagged: {from_material})" if from_material else ""))
    print(f"of them in the draft: {shared or 'none'}")

    dg = set().union(*[grams(d) for d in defaults])
    mine = {g for g in grams(draft) if not all(w in STOP for w in g)}
    sh = sorted(" ".join(g) for g in mine & dg)
    print(f"\nshared 4-word sequences (information only, not an edit target): {len(sh)}/{len(mine)} = {len(sh) / max(1, len(mine)):.2f}")
    if sh:
        print("  " + "; ".join(sh[:40]))

    print("\nFOR THE REVISER:")
    if flag:
        print("- The opening is close to a default's opening: start from what only this text has, if the story allows.")
    if shared:
        print(f"- The draft leans on the specifics every default uses ({', '.join(shared)}). Keep one only if the story"
              " needs it; otherwise use a specific the defaults did not reach for.")
    if not flag and not shared:
        print("- Nothing shared with all defaults at once.")


if __name__ == "__main__":
    main()
