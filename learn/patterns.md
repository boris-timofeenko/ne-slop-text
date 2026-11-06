# Pattern tags for marks

Every mark in `marks.jsonl` is one sentence the user labelled `slop` or `live` in a blind test (or cut from a draft),
with a tag that names the decision behind it. Tag the decision, not the topic. Add a new tag when none fits; if it is
marked twice the same way and never the other, `update_weights.py` will propose a questionnaire feature for it.

| Tag | Feature in `loop/questionnaire.json` | Expected | Example |
|---|---|---|---|
| inventory | inventory_sentences | slop | "Tests LLM agents for spec conformance, tool-call correctness, prompt injection and data leakage, and..." |
| clever_turn | clever_turns | slop | "I came to QA from frontend development and can talk to engineers like an engineer." |
| resume_speak | resume_speak | slop | "Lead a team of 3 QA engineers and own release sign-off." |
| process_description | process_description | slop | "Test plans live in a self-hosted Kiwi TCMS, each case is mapped to its automated test, and CI runs export..." |
| significance_connective | significance_clauses | slop | "That means ~5–10 fewer manual checks per release." |
| colon_reveal | colon_reveals | slop | "We brought it down by fixing what caused it: test isolation, test accounts and race conditions." |
| meta_about_text | meta_about_text | slop | "The stoicism event first, since you asked for it explicitly." |
| performed_joke | clever_turns | slop | "The joke answer is that I asked the AI to fix them a thousand times; the real answer is..." |
| idiomatic_paraphrase | (reviser rule: translate literally) | slop | "I set up how QA works in our team" for "выстраиваю процессы в нашей команде" |
| stance | stance | live | "Junior manual QA will probably disappear, and the people who stay will be..." |
| plain_first_person | (inverse of resume_speak) | live | "I lead 3 QA engineers and sign off releases." |
| external_force | agency = external_forces_present | live | "We had been automating slowly, until we got a sharp talking-to: go faster." |
| reader_address | reader_address | live | "Here is what I've done; judge for yourselves." |
| plays_reader_code | brief_words_to_answer | live | "Your ad asks for justice, enough to be unbiased in judgment, so I won't claim to be the best..." |
| answers_reader | opening_move = answers_brief | live | "Most of the duties on your list are things I already do as QA Tech Lead at..." |
| specific_episode | episode_specificity = specific | live | "...the model didn't know today's date and refused people who had turned 18 a month earlier" |
