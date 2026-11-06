# Example context: one paragraph for a LinkedIn post

Task, as a user would type it: "Write one paragraph for my LinkedIn post about this bug we caught. English. Don't
invent facts."

Material: Boris's spoken answer to "was there a case when a test caught something real?" (voice transcript, Russian,
as said):

> Да, однозначно такой случай был. Например, это когда нужно было проверить самый первый прототип, и я помню, ну, я же
> знаю, что как сказать, нейронка не всегда знает, какое сегодня число, и если челику едва-едва 18 лет стукнуло, то он
> уже должен иметь возможность зарегистрироваться, но нейронка не знала точное число и блокировала регистрацию для
> челиков, которые чуть-чуть старше 18, типа 1 месяц там еще сверху, и соответственно я написал тест на то, чтобы это
> падало.

Facts:
- Boris is a QA tech lead at a fintech; the product has an AI onboarding agent in WhatsApp that registers users.
- On its first prototype, the LLM did not know the current date and refused registration to people who had turned 18
  about a month earlier.
- Boris knew that language models don't reliably know today's date, so he wrote a test for that boundary; the test
  failed on the prototype.
- The agent's answers are also checked with LLM-as-a-judge.
