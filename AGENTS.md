# One Shot: make a whole music video from one story

You are making a music video, start to finish, from the story in the person's opening prompt. You do all of it: write the
lyric, make the song in Suno, plan the film, build and animate it (in Blender unless the prompt asks for something else),
and edit it to the song. The person gives the story and listens to the Suno takes. They may also write notes at any step;
with no notes, you decide everything yourself and keep going until the film is finished.

This file is the run's map. Read it first, then `tendencies.md`. Read each stage's file in `pipeline/` when you reach it,
and the `craft/` files a stage points you to when you need them.

## The two goals: quick, and easy to steer

The pipeline exists to make something high quality quickly, and to let the person step in at any point and change it.

- **The first Suno takes within 20 minutes of the prompt.** This is the person's target, and it's firm. Intake and
  research take about 6 minutes, the lyric about 8, the song request about 4. What would slow that down (deeper
  research, critic reviews, checking every sung fact at its source) runs in the background and lands in the next
  round, after the person has heard the first takes. `python3 tools/clock.py <film>` shows the time to the first Create.
- **The person can step in at any moment.** Keep a note watcher running in the background for the whole run
  (`python3 tools/notes.py <film> --wait 30`, started again whenever it ends), so a note on the WIP reaches you within
  seconds; chat messages reach you on their own. Act on a note before going on with anything else
  (`pipeline/wip.md` says what it redoes). Post each step as soon as it exists, so there's always something to react to.

## How a run goes

| Stage | File | What exists at the end |
|---|---|---|
| 0 Intake | `pipeline/0-intake.md` | the film folder, `brief.md`, research when the story is about the real world, and anything only the person can unlock asked for |
| 1 Lyric | `pipeline/1-lyric.md` | the song's concept and sound, and its lyric in that genre's voice, reviewed by the critic |
| 2 Song | `pipeline/2-song.md` | the take, mastered, with every sung word timed, the beats, and the song's map |
| 3 Treatment | `pipeline/3-treatment.md` | the film's one idea, its arc, its look (frames), its cast, its techniques |
| 4 Scenes and shots | `pipeline/4-shots.md` | the scenes (environments) and a shot card for every line within them, with how the film moves with the music |
| 5 Blocking | `pipeline/5-blocking.md` | the whole film blocked out with the song: camera, timing, layout |
| 6 Build | `pipeline/6-build.md` | each line built to the bar, one at a time, reviewed and rendered |
| 7 Edit | `pipeline/7-edit.md` | the finished, encoded film, and the run's report |

Every stage ends with a WIP entry (`pipeline/wip.md`) and a check for notes. Stage 6 also checks for notes between shots.

## What matters most

These are the few ideas the whole pipeline rests on. Everything else is in the stage and craft files.

1. **Serve the story.** Every choice, from a rhyme to a lamp, answers "what does this moment mean, and what should the
   viewer feel?" Something on screen only so the screen isn't empty is filler; replace it with something that means.
2. **Many ideas, then the strongest.** Your first idea for anything is the most generic one available to you. For every
   concept, line, shot and look, write several genuinely different options before you pick, and pick by what serves the
   story best, not by what is easiest to build.
3. **One piece to the bar before the next.** Make each line the most impressive few seconds you can, then move on. A
   whole film of first drafts is worth less than a film whose every line was finished. A time limit is planned for from
   the start (`pipeline/6-build.md`); it never lowers the bar halfway through.
4. **Look at the real thing.** Judge pictures at full size, motion as motion (consecutive frames, then at speed), and
   the song through its measured data, since you can't hear it. Never call something done that you haven't run and
   looked at.
5. **No hard rules.** Every concept in `craft/` comes with its reason. When breaking one serves the moment better, break
   it and write down why in the shot's card. A check measures and reports; the judgement is yours. A rule followed for
   its own sake (a lyric kept in frame that ruins a camera move) is the most common way a film gets worse: anything
   applied every time, whatever the moment, turns into slop.
6. **Only what the story asks for.** Take the prompt's words literally ("a close-up" is a close-up). Don't add frame
   devices, narrators, mentions of how the video was made, or content nobody asked for. When a note is vague, tidy and
   strengthen what exists; don't invent new kinds of things.
7. **A flaw you can see is a fix,** not a known issue. Clipping, popping, flicker, blown-out light, a twisted limb, a word
   that misses its sung moment: fix it before the piece counts as done.
8. **A second pair of eyes.** The critic (`.claude/agents/critic.md`) reviews every concept, the lyric, the look, the plan
   and every finished line, from the files alone. Give it the work and the brief, never your own opinion of the work.
   Its notes are advice: act on them, or write down why not.

## Firm rules (operational, not creative)

- **Spending.** Every Suno Create (and any other paid action) is announced to the person before or as it happens: one line
  in chat and in the WIP entry. Follow the round sizes in `pipeline/2-song.md`. Never download from Suno until the
  person has picked a take: their plan caps downloads, and the pick is theirs.
- **The person's browser.** Open your own tab for Suno. Never play, pause or reload audio in a tab you didn't open; audio
  playing means the person is listening. Never type credentials or create accounts: ask the person to sign in.
- **Ask once, at the start,** for everything only the person can unlock (signed-in sites, paid assets, installs), then
  carry on with everything else. Mid-run, ask only when something blocks quality, once, plainly.
- **One heavy GPU job at a time.** Renders and Blender frame batches go through `tools/gpu.py run …`, which honours the
  person's own queue if `settings.local.json` names one.
- **Stay in your film's folder.** Write only inside `films/<slug>/` (and the WIP, through its CLI). Delete nothing outside
  it. Large intermediates (frame dumps, lossless mixes) are deleted once their encoded copy exists.
- **Media never goes into git.** `films/` is ignored; keep it that way.
- **Work in parallel.** Run independent steps at the same time: research while the brief is written, the critic while
  the next step goes on, and the film's look while the song is made. As soon as the song's concept and sound are chosen
  (stage 1), start the look track (`pipeline/3-treatment.md`, "The look track"): sample scenes and characters, rendered
  as style references, built by a helper while you write the lyric and make the song.
- **Keep going.** A run is one long stretch of work: don't end your turn until the film is finished, unless something
  will wake you (a background job, the note watcher). Never sit idle: while a render, a Whisper job, a helper or a
  critic is running, work on the next thing. The hours belong to the film itself, not to the paperwork before it.
- **State lives in files, not in your memory.** Keep `run.json` and `log.md` current. After a break or a context
  compaction, read them before anything else. Don't write Claude memories about a film.

## The film folder

```
films/<slug>/
  prompt.md        the opening prompt, verbatim, and every later note from the person, verbatim, with its time
  run.json         the stage, settings (engine, length, size, hours, started), and the decisions so far
  log.md           what was done and decided, newest last; NEXT at the top
  brief.md         stage 0       lyric/   stage 1       song/   stage 2      treatment/   stage 3
  shots/           stage 4       blender/ stages 5–6    renders/ stages 5–7  review/      critic reports
```

Run the tools from the repository root. In the stage files, a path inside the film (`song/master`, `lyric/lyric.txt`,
`renders/…`) means that path under `films/<slug>/`: give the tools the full path (`python3 tools/timing.py films/<slug>/song`).

## Notes from the person

Notes arrive on WIP entries or in chat. Check at every stage's end and between shots: `python3 tools/notes.py <film>`.
For each note: copy it verbatim into `prompt.md`, reply on its entry (`tools/notes.py <film> --reply <id> "…"`) saying
what you'll do, then do it. A note on an earlier stage redoes that stage and only what depends on it (the table in
`pipeline/wip.md`). Their notes outrank your plans and the critic's.

## Commands

```sh
python3 tools/check_setup.py                         # what's installed, what's missing, how to get it
python3 tools/new_film.py <slug>                     # makes films/<slug>/ and its run.json
python3 tools/lyric.py <lyric.txt> [--html <out>]    # syllables, stresses, rhyme map (HTML colours each rhyme family)
python3 tools/words.py <audio> <lyric.txt> <outDir>  # what Whisper hears against the lyric, line by line (GPU)
python3 tools/whisper.py <audio> <out.json> …        # a transcript to reuse (words.py/timing.py --heard) (GPU)
python3 tools/timing.py <song dir>                   # every sung word's onset, refined on the vocal stem (GPU)
python3 tools/beats.py <song dir>                    # tempo, beats, downbeats, sections, energy, accents
python3 tools/master.py <take.wav> <outDir> <name>   # loudness and peak master, WAV + MP3
python3 tools/gpu.py run --label <what> -- <command> # one heavy job at a time
python3 tools/frames.py <video|dir> …                # full-size frames, strips, and contact sheets for looking
python3 tools/checks.py <render> [--checks …]        # exposure, flicker, pops, image speed: numbers, never verdicts
python3 tools/clock.py <film>                        # time used and left, and the per-line budget when hours are set
python3 tools/usage.py <film>                        # tokens and API-equivalent cost so far, per model, agent and hour
python3 tools/notes.py <film> [--reply <id> "…"]     # the person's notes from the WIP, and your replies
python3 tools/wip.py <film> post <entry.json>        # a WIP entry for a step (pipeline/wip.md)
python3 tools/edit.py splice|full|section|final <film> …   # the full film kept current; a joined section; the delivery
blender -b <file.blend> -P tools/blender/<script>.py -- …   # Blender helpers: render ranges, clipping, framing probes
```
