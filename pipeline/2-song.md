# Stage 2: Song (the first Create about 20 minutes after the prompt)

You can't hear. The person listens on Suno and picks the take; you write the request, drive Suno, and turn the chosen
take into data the whole film keys to. Nothing is downloaded until they pick: their plan caps downloads. Read `craft/song.md` first.

## 1. Three directions

The lyric was written for the sound chosen with its concept (stage 1). Write three genuinely different directions within
that sound in `song/directions.md`: different grooves, tempos, instrumentation, voices and deliveries, arrangements, all
of which the lyric suits. A direction in another genre only if the lyric would sing well there too; otherwise adapt the
lyric to it first (stage 1). Each direction also says what the music does at the turning point (a key change, a tempo
or groove change, a drop, a new instrument), how it starts (short, or straight in on the first line) and how it ends (a
real ending, not a fade mid-line).

Turn each into a Suno style prompt: a few compatible, prioritised instructions beat a pile of adjectives. Name musical
traits, never artists. Use exclusions sparingly, for real risks (a long instrumental intro, a fade-out, a mumbled vocal).
This takes a few minutes, with no critic gate: the person's ears are the judge of the sound.

If the person points at a song whose style they like (a Suno link), open it in your own tab and read its style
description from the page; it's the starting point for all three directions, which stay close to it and differ in
smaller ways (tempo, voice, arrangement). Never play it: you can't hear it, and audio in their browser is theirs.

## 2. Read Suno's form from the page

If you read the form in stage 0, just check nothing has changed. Otherwise open https://suno.com/create in a new tab of
your own. Read, never assume: the model picker (choose the best available,
write its exact name), every field and its character limit, the vocal gender, the duration setting, sliders, what a
Create costs and what the plan allows for downloads. Write it down in `song/request.md`.

Driving the page:
- After every Create the form re-renders and element references go stale: find them again before typing.
- Before typing or selecting all, confirm the intended field has focus (`document.activeElement`).
- The lyric box is a rich editor; put lines in as the editor's own paragraphs (one a line) and read the box back.
- Read the field values back after filling and compare them with the request, the whole lyric included.
- Click Create once. If the page is slow, check the library; never click again.
- Audio playing in any tab is the person listening. Never play, pause or reload it.
- Before using a feature you haven't used (Voice, the Song Editor, Extend, Cover), read Suno's own help for it.

## 3. Round 1: one Create per direction

Tell the person before each Create ("Creating direction 2 of 3 now, X credits"), in chat and in the WIP. Each Create
returns two takes. Log every Create in `song/request.md` the moment the page shows its takes: the exact style, settings,
lyric file and the take links (`https://suno.com/song/<id>`), and put the links in chat so the person can listen at once. Write
the time of the first Create into `run.json` as `firstCreateAt`; `tools/clock.py` reports it against the 20-minute target.

While the takes generate and the person listens, the background work from stage 1 lands (the lyric critic, the fact
checks): have `lyric/2/` ready, so a second round can start the moment it's wanted.

**Download nothing yet.** The person's plan caps downloads, and choosing a take is theirs: they listen on Suno and say
which one. Post all six takes in one WIP entry (the Suno links, which direction each is, what to listen for) and put the
links in chat. Then wait for their pick while you work on everything that doesn't need it (below). A pick or note in
chat counts the same as one on the WIP; the note watcher brings it.

## 4. The pick

- **The person picks.** Download only that take (WAV) into `song/takes/`, then its stems and MIDI (step 6).
- **If they write notes instead,** turn each into a narrow change: the style text, an exclusion, a section tag, or lyric
  lines (stage 1 for those lines, then back here). Then make a round 2 with as few Creates as the change needs,
  announced, and post its links the same way.
- **Never pick for them.** If nothing has come after the pick window (`run.json`), remind them once in chat with the
  links, and keep working.

Don't idle while you wait: start what doesn't depend on the take (the look track, the treatment's ideas from the lyric,
the cast, asset gathering), and don't lock anything that does (tempo, section lengths, cuts).

Once the take is downloaded, measure it (Whisper runs on the GPU: through `tools/gpu.py`, outside any command sandbox,
once; if it fails, read the error before running it again, never in a loop):

```sh
python3 tools/gpu.py run --label "words <id>" -- python3 tools/words.py song/takes/<id>.wav lyric/lyric.txt song/takes/<id>/
```

That shows which lines Whisper hears clearly, the length, and where the first word starts. Whisper hears sung words less
reliably than speech: a flagged line is a question, not a verdict, and worth mentioning to the person if it matters.

## 5. Keep the singer

If more Creates may follow (a round 2, an Extend), make a Voice from the chosen take so the singer stays the same, with
Public switched off. Saving a Voice can overwrite the style box with Suno's own description: put your style back.

## 6. Stems and MIDI

From the chosen take on Suno: Get Stems (all of them) and the MIDI (with "Follow tempo changes"), into `song/stems/` and
`song/midi/`. Use Suno's own stems; separating them yourself smears the voice. Some Suno MIDI files carry a malformed key
signature; the tools skip it.

## 7. Trim and master

```sh
python3 tools/master.py song/takes/<id>.wav song/master <name> [--start <s>] [--end <s>] [--tail <s>]
```

- `--start`: cut a slow or long intro on a beat just before it should begin (a short fade-in is added). A cold open
  starts one beat before the first word.
- `--end` and `--tail`: if the take trails off or fades mid-phrase, end on its last strong note and let a reverb tail
  ring out for the end card.
- It masters to −14 LUFS integrated and −1 dBTP, 48 kHz 24-bit WAV and a 320k MP3. The film always uses this file;
  if you trim, the stems are trimmed the same way (it does both).

## 8. Timing and the song's map

```sh
python3 tools/gpu.py run --label timing -- python3 tools/timing.py song/   # every sung word's onset: song/timing.json + timing.png
python3 tools/beats.py song/       # tempo, beats, downbeats, sections, energy, accents: song/map.json + map.md
```

- Word times come from Whisper on the vocal stem, aligned to `lyric/lyric.txt`, then moved onto the voice's actual
  onset (the consonant or the start of voicing) on the stem. MIDI note times can run early or late against the audio;
  they're used only as a cross-check.
- Look at `timing.png` (the vocal waveform with each word's tick) for lines where words bunch up or stretch out; those
  are the guessed ones. `timing.json` marks which words were heard and which were placed between neighbours.
- `map.md` is how you "hear" the song: where each section starts and ends, how its energy compares, where the turning
  point is, which instruments enter where, and the accents worth landing moves on. Read it closely before stage 3.

## 9. Show it

WIP entry: the chosen take, mastered, with why it was chosen; the map in brief; what the film will key to. Check for
notes, then stage 3.
