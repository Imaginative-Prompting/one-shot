# Showing the work, and the person's notes

The person sees the run through WIP entries, one or more per stage, and can write a note on any entry. You never wait
for notes (except the take pick's window, `pipeline/2-song.md`), but you look for them often and act on them first.

## Posting

```sh
python3 tools/wip.py <film> post <entry.json>
```

`tools/wip.py` finds the person's WIP from `settings.local.json`, makes the film's project on first use, copies nothing
(media is referenced in place from the film folder), and refuses to overwrite an existing entry: each pass is a new
entry with a new id, so the newest is always on top. With no WIP set up, it writes the same entry as Markdown into
`films/<slug>/wip/` and the person can read it there.

An entry:

```json
{
  "id": "s3-look-frames-2",
  "title": "Look frames, round 2",
  "tags": ["treatment", "look"],
  "summary": "One line: what this is and what changed.",
  "body": "Markdown: what this step made; the options weighed, the pick and why; the critic's verdict in a few lines; what's next. Known issues only if they're outside this step.",
  "media": [{ "type": "image", "src": "treatment/look/frame-1.png", "title": "The diner at 2:14" }]
}
```

`src` paths are relative to the film folder. Images go up at full size; clips go up encoded (H.264) with their own audio.
Write for someone who hasn't followed the run: plain words, what they're looking at, what you decided.

When to post: every stage's end, every Suno round (with the spend), every look frame round, the animatic, every finished
shot with the current full film, every joined section, the final film. Never hold a post back because of a flaw you've
found: post it with the flaw named first, and post the fix when it lands.

## Notes

```sh
python3 tools/notes.py <film>                         # new notes from the person, oldest first
python3 tools/notes.py <film> --reply <note id> "…"   # your answer, shown under their note
```

Check at the end of every stage, between shots in stage 6, and while waiting on anything. Notes typed in chat count the
same. For each note:

1. Copy it verbatim, with its time and the entry it's on, into `prompt.md`.
2. Read it as one thought with any other new notes; they often explain each other.
3. Reply on the entry: what you understood and what you'll do. If it's ambiguous, say how you read it and go ahead; they
   can correct you.
4. Do it, and post the result as a new entry that names the note.

Their words are taken literally, like the prompt's. A note about one thing changes that thing; it doesn't license
redoing what they didn't mention. A vague quality note ("make it cleaner") means better framing, value, colour and
fewer, bigger things, not new kinds of things.

## What a note on an earlier stage redoes

| Note on | Redo | Then |
|---|---|---|
| the brief or story | the stage it changes | every later stage the change reaches |
| the lyric | the lines it names (stage 1) | a new Create (announced), timing and map; shots keep their cards and move to the new times |
| a take, or the sound | the request or the pick (stage 2) | timing and map; shots move to the new times |
| the treatment or look | the look frames | the shots the change touches |
| a shot | that shot | its neighbours' transitions |
| the edit | the edit | nothing else |

Shots are keyed to `timing.json` and `map.json`, never to typed frame numbers, so a new take moves every shot to its new
times without rebuilding it. Check each moved shot's landings anyway.
