# Review: using the critic

You built it, so you see what you meant, not what's there. The critic (`.claude/agents/critic.md`) sees only the files.
Use it at every point the stages name, and whenever you're about to call something done.

## Asking

Start it with the Agent tool (`subagent_type: "critic"`). In the prompt, give:

- **what it is reviewing,** in one line ("the four song concepts", "shot 3.2, the diner, final draft");
- **the paths** to the work: the files, the full-size frames, the frame strips, the check numbers, the clip;
- **the paths** to what it's judged against: `brief.md`, `prompt.md` (the person's words), the stage's file, the
  relevant `craft/` files, the treatment and the shot's card when they exist;
- **the question,** if there is one beyond "how good is this and what would make it better".

Never give it your opinion of the work, what you're proud of, what you already know is wrong, or which option you
prefer. An anchored critic agrees with you. A new critic each time keeps it unanchored; don't reuse one across rounds of
the same piece.

## What comes back

A verdict (does it serve the story and the brief), its strongest and weakest points, and specific notes, each with where
(a line, a frame, a time), what's wrong, and why it matters to a viewer. For a choice between options, a ranking with
reasons.

## Acting on it

- Each note: fix it, or write in the card or `log.md` why you're not. "I disagree because …" is fine; silence isn't.
- A critic's note never becomes a rule. The brief holds the person's words and what they ask for; a note that would add
  a requirement, a ban or a quota to it goes in `log.md` as something to weigh at the stage it concerns. A pile of
  accepted cautions is how a film ends up timid.
- A note that points at a visible flaw is fixed, always.
- The person's notes outrank the critic's.
- When the critic and you disagree on taste, the brief decides; when the brief is silent, choose, and say so in the WIP
  entry.
- **How many rounds.** Before the song (the brief, the lyric): the critic runs in the background and never holds up the
  first takes; its notes go into the next round. After the song, text (the treatment, the shot plan): one review, act
  on it, move on, and a second only when the first said the work doesn't serve the story at all. Built pictures (look
  frames, shots, joined sections): after fixing, a fresh critic reviews the new version, until a review finds nothing
  worth changing. The time belongs to the film, not to the paperwork before it.
- **Don't wait on it.** Start the critic in the background and do the next step that doesn't depend on its verdict
  (the song's directions while the lyric is reviewed, the next shot's set while this shot is reviewed).

Save each review in `review/<stage-or-shot>-<n>.md` so the run's history shows what was raised and what was done.
