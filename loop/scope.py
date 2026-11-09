"""Did the reviser stay inside its scope?

Every sentence of the old draft that the reviser was not allowed to edit must still be in the new draft, word for word.
In a test run the reviser split an opening sentence it had no licence to touch, and that edit alone flipped the
guard's verdict: the loop had started editing to move the number. This check catches that.

usage: scope.py OLD.txt NEW.txt ALLOWED
ALLOWED = comma-separated sentence numbers of OLD that may change (the EMPTY ones, the opening if overlap.py flagged
it, and sentences carrying a specific overlap.py flagged), e.g. "1,6", or "" for none.
Exit code 1 and a list of violations if a protected sentence changed; the orchestrator then keeps the old draft (or
asks the reviser again with the list).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch import split  # noqa: E402


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    old = split(open(sys.argv[1], encoding="utf-8").read())
    new_text = norm(open(sys.argv[2], encoding="utf-8").read())
    allowed = {int(n) for n in sys.argv[3].split(",") if n.strip()}
    violations = []
    for i, s in enumerate(old, 1):
        if i in allowed:
            continue
        if norm(s) not in new_text:
            violations.append((i, s))
    if violations:
        print(f"OUT OF SCOPE: {len(violations)} protected sentence(s) changed or removed:")
        for i, s in violations:
            print(f"  [{i}] {s[:140]}")
        print("Keep the old draft, or send the reviser back with this list.")
        sys.exit(1)
    print(f"in scope: every protected sentence ({len(old) - len(allowed)}) is unchanged")


if __name__ == "__main__":
    main()
