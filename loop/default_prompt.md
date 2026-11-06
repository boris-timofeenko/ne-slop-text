# Default writers

Each default writer is a fresh agent with no knowledge of this skill. Use different models (e.g. opus, sonnet, haiku):
the point is to see where models land on their own, not to get good text.

Give each one only:
- the context files (the same ones the draft was written from), and nothing else from the folder;
- the task in the words a user would type, for example:
  "I'm applying to this job. The form has a field 'Message to the Hiring Team: why are you the best for the job?'
  Write my message, in English. Don't invent facts. Write only the text to <path>."

Keep "don't invent facts" in every prompt, so that the comparison is about decisions and not about fabrication.
For a source text (fix mode), still generate defaults for the task the source was written for: they show the local
pull of the average, and the source is usually one of them.
