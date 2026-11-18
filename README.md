# One Shot

**A whole music video from one story, made by Claude Code.**

You write the story you want the song to tell. Claude Code writes the lyric, makes the song in Suno, plans the film,
builds and animates it in Blender, and edits it to the music. You listen to the song takes and, if you want, leave notes
along the way. Otherwise it makes every decision itself and keeps going until the film is finished.

From [Imaginative Prompting](https://www.youtube.com/channel/UCzAPMzBbq7w5d7rsSdb0fTw), where every music video is made with
Claude Code.

## What you need

- **Claude Code**, with **Claude in Chrome** connected (the run drives suno.com in your browser).
- **A Suno account** signed in in Chrome. A paid plan is needed for commercial use, WAV downloads and stems. Read
  Suno's terms for what you may do with the songs.
- **Blender** 4.2 or newer, with `blender` on your PATH.
- **ffmpeg**, **Python** 3.10 or newer, and **Node.js** 22 or newer if you use the WIP.
- **Whisper:** on Apple silicon, `uv tool install mlx-whisper`; elsewhere `pip install faster-whisper` into the tools'
  environment.
- **Optional:** [WIP](https://github.com/Imaginative-Prompting/wip), to watch every step as it happens and write notes
  on it.

```sh
git clone https://github.com/Imaginative-Prompting/one-shot.git
cd one-shot
python3 tools/check_setup.py --install     # makes .venv/ for the tools and says what else is missing
cp settings.example.json settings.local.json   # optional: your WIP, a GPU queue, the Whisper backend
```

## Making a film

Open Claude Code in this folder and give it your story:

> Make a music video. The story: a lighthouse keeper who has kept the light on every night for forty years learns the
> ships stopped coming a decade ago. Bittersweet, folk, about three minutes.

Say as much or as little as you like: the story, a genre, a length, a look, a camera style, a time limit in hours.
Whatever you leave open, it decides. Then:

1. **It asks once** for anything only you can give: Suno signed in, a sign-in for character motion (Mixamo) if the
   story has people who move a lot, anything else the story implies.
2. **You listen, about 20 minutes in.** It researches the story if it needs to, writes the lyric, and makes three takes in
   different directions (telling you before it spends anything) and posts them.
   Listen on Suno, then pick one, ask for another round, or say what's wrong ("line 12 never sings right"). Picking is
   yours: nothing is downloaded until you pick (Suno caps downloads), and meanwhile the run keeps building the film's
   look.
3. **Everything else is the run's.** Each step shows up as a WIP entry (or a Markdown file in the film's folder). Write
   a note on any of them, in the WIP or in chat, and it acts on it. Write nothing, and it carries on.

The film ends up in `films/<name>/renders/final/`, with a report of what it decided and why, what it spent, and the
credits for every asset it used.

## How it works

The run follows a pipeline, one stage at a time. Each stage's instructions are read only when it gets there.

| Stage | What it makes |
|---|---|
| [0 Intake](pipeline/0-intake.md) | the brief: your words, read literally, and everything left open |
| [1 Lyric](pipeline/1-lyric.md) | several song concepts, the strongest chosen; the lyric in its genre's voice, checked line by line |
| [2 Song](pipeline/2-song.md) | three Suno directions, your pick, then the master, every sung word timed, the song's map |
| [3 Treatment](pipeline/3-treatment.md) | the film's one idea, its arc, its look proven in frames, its cast |
| [4 Scenes and shots](pipeline/4-shots.md) | the scenes the film moves through, a written shot for every line in them, and how the film moves with the music |
| [5 Blocking](pipeline/5-blocking.md) | the whole film roughed out on the song's clock |
| [6 Build](pipeline/6-build.md) | each shot made as good as it can be, one at a time |
| [7 Edit](pipeline/7-edit.md) | the finished film, checked, and the report |

Three things carry the quality:

- **A craft library** ([craft/](craft/)): story, lyric, song structure, music to picture, camera, composition,
  transitions, light and colour, look, animation, people, sets, words on screen, editing. Each concept says what it does
  for the viewer and when breaking it is the better choice. **None of it is a hard rule.**
- **[Where a model's first attempts go wrong](tendencies.md)**: the bland camera, one technique everywhere, filler
  motion, the clever chorus nobody understands. Distilled from thousands of review notes on model-made music videos.
- **A critic** ([.claude/agents/critic.md](.claude/agents/critic.md)): a fresh Claude that sees only the files and judges
  every concept, the lyric, the look, the plan and every finished shot. It never hears the builder's opinion of its own
  work.

The [tools](tools/) are the mechanical parts: rhyme maps, Whisper word checks, word timing measured on the vocal stem,
the song's beats and sections, mastering, frame and render checks (exposure, flicker, pops, image speed, colour
blindness), Blender probes for framing and things passing through things, and the edit. Each reports numbers, never a
verdict.

## Time and cost

Two goals shape the pipeline: getting you to something good quickly, and letting you step in at any point. The first song
takes come about 20 minutes after your prompt; deeper research, reviews and fact checks run alongside and feed the next
round. A note on any WIP entry reaches the run within seconds. For speed, start Claude Code at `high` effort; `xhigh`
and `max` think longer on every step.

There is no limit by default: the run keeps working on each shot until it can't find anything worth improving. Give it a
number of hours and it plans around them from the start, sharing the time equally among the shots (pauses don't count,
and you can put the final render outside the limit, say for a 4K delivery). A whole film can take
many hours and a lot of usage. Suno Creates and downloads use your plan's credits; the run tells you before each one.

## License

MIT. The films you make are yours; the songs are subject to Suno's terms, and downloaded assets to their own licenses
(listed in each film's report).
