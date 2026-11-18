# Stage 0: Intake (about 6 minutes, research included)

The prompt is the whole brief. This stage reads it closely, finds the facts the song needs if the story is about the real
world, and asks the person, once, for anything only they can give. It's quick: the song is waiting.

## 1. The film folder (now)

```sh
python3 tools/new_film.py <slug> [--hours N] [--length m:ss]   # a short name from the story; hours and length if the prompt gives them
```

Copy the opening prompt into `films/<slug>/prompt.md` exactly as written, with the date and time (`date`). Every later
note from the person goes into the same file, verbatim, with its time. Nothing in it is ever paraphrased. Start the note
watcher (AGENTS.md, "The two goals").

## 2. Research, when the story needs it (start it first: about 5 minutes)

If the story is about the real world (current events, real people, a real scene or history), start the research before
writing anything else, so it runs while you write the brief. Run `date` first: it's later than your knowledge.

The song needs the story's few big moments and what people say about them, not a dossier. Start one or two `scout`
helpers at once (`.claude/agents/scout.md`), one per thread (for example: what happened and where things stand; what
people are joking about). Each comes back within about five minutes. You merge them into a short `research/facts.md`:
the five to eight moments everyone knows, in plain words, and a handful of references worth singing
(`craft/research.md`). Anything the film will need later (how real things look, more references for the picture) is
researched in the background after the song request, not now.

## 3. The brief (about 3 minutes, while the scouts run)

Write `brief.md`. It's what every later stage and the critic check against.

- **The story, in their words.** Quote the prompt's story. Prompts are often thought out loud: a "maybe", an aside, a
  correction ("X, although Y is closer") is them steering, not content to use. Write down where their thinking landed
  (here: Y), and build from that, not from the path that got there. Their words describe what the song should do; they
  aren't the lyric. A label they use ("good news, then bad news", "the chorus asks…") isn't sung: write lines that do
  what it describes.
- **What it asks for, item by item, read literally.** The story's beats, tone, who's in it, any lines that must be sung,
  genre, voice, length, look, camera style, engine, a time limit. For each descriptive word, write the measurable
  version you'll build to: "a close-up" is the head filling a third to half of the frame height; "huge" is bigger than
  anything around it.
- **What it leaves open.** Everything not asked for is yours to decide, in the stage it belongs to.
- **What it doesn't ask for.** The additions you'll be tempted to make (a narrator, a frame story, a mention of how the
  video was made, a mascot), so you notice if one creeps in.
- **Length** (from the prompt, or what the story needs and why: a story with one turn usually fits 2:30–3:30), **engine**
  (Blender unless the prompt asks for something else) and **time** (a number of hours if the prompt gives one; otherwise
  no limit beyond the 20 minutes to the first takes). If the person sets or changes a limit later, or pauses the run, or
  asks for the final render to sit outside the limit, record it in `run.json` (`pipeline/6-build.md`, "Time").

Start one critic on the brief in the background (`pipeline/review.md`); it checks only how the brief reads the person's
words. Don't wait for it: act on what it finds when it lands.

## 4. Settings and the one ask (a minute)

`python3 tools/check_setup.py` (in the background) reports what's installed and what's missing; install what you can.
`settings.local.json` is the person's; don't edit it unless they asked.

Make one message with everything only the person can unlock, then carry on with whatever doesn't need it:

- **Suno, signed in, in their Chrome**, with Claude in Chrome connected (a paid plan for commercial use, WAV and stems).
  Open https://suno.com/create in a new tab of your own to check, and read its form while you're there (stage 2, step 2),
  so stage 2 only has to fill it. Don't touch their tabs.
- **Mixamo** (an Adobe sign-in) if the story has people who need to move a lot.
- **Anything the story implies:** a paid asset, a font, a sign-in to a stock site.

Never type a password or create an account.

## 5. Show it

One WIP entry with the brief and the research: the facts, the deep cuts, what's still being checked. Check for notes, then
stage 1. The clock: stage 1 should start about 6 minutes in.
