# Reader: is it still easy to follow?

You get the intended readers (who they are) and two versions of a short text, X and Y. Read as one of those readers
would, once, at normal speed. For each version:
- main_point: the main point in one sentence of your own;
- clarity: how easy it was to follow on the first read, 1 to 5 (5 = no effort, 1 = lost the thread);
- why: one short line.

Judge only how easy it is to follow, not style, taste or whether you agree. Two versions may get the same number.
Write JSON to the path you are given: `{"X": {"main_point": "...", "clarity": 4, "why": "..."}, "Y": {...}}`.
Read only what you are given; do not use skills. Reply with one line.

The orchestrator keeps the new version only if its clarity is not lower than the current one's. Clarity is a floor,
never a target: models like smooth text, and maximising it pulls the text back toward the defaults.
