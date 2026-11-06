# Lint, English

Run `python3 lint/lint.py FILE --lang en`, then check by eye what a regex cannot see:

- No em dashes. At most one antithesis in the whole text. No "not just X but Y".
- No colon used to stage a payoff ("We fixed it by fixing what caused it: X, Y and Z"). Colons introduce lists,
  quotes and labels only.
- No trailing clause that explains significance ("..., ensuring...", "That means...").
- No triads for rhythm; keep three only where the meaning has three parts.
- Actor and verb first, the everyday word ("use", not "leverage"; "I lead", not "Lead a team of").
- Headings name the content.
- Same sentence shape three times in a row: break one.
- The portability test (from unslop): would this sentence fit another person or company unchanged? Then it carries no
  information; replace it with what holds only here, or cut it.

Sources for longer lists: the unslop skill (`references/word-lists.md`) and the humanizer pattern list (sections 1 to
29). Use their lists only as a lint. Do not use humanizer's "personality and soul" rewriting.
