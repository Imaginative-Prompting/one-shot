# Song

The music carries more of the feeling than the words do. You can't hear it, so you shape it through the request, measure
what comes back, and let the person's ears decide.

## Structure

Common shapes: verse–chorus–verse–chorus–bridge–chorus; with pre-choruses; a short intro or none; an outro that resolves.
Choose by the story: a story with a turn wants a bridge; a build wants each section bigger than the last; a short, punchy
song can skip the second verse's length. Total length follows the brief.

## The arc of the music

- **Dynamics.** Sections differ in energy: sparse verses and full choruses, a stripped bridge, a last chorus that's the
  biggest. A song at one level all the way through is tiring and flat.
- **The turning point.** The story's turn deserves a change in the music: a key change (often up a step for the last
  chorus), a switch to half-time, a drop to one instrument, a new instrument entering, a different groove. A big tonal
  shift (bright to dark, cheerful to unsettling) can carry a whole story's reversal.
- **Transitions between sections.** A fill, a riser, a pause of a beat, a pickup line. Abrupt jumps sound like mistakes
  unless they're deliberately abrupt. Instrumentals dropping to complete silence mid-song should be a choice, not an
  accident.
- **Openings.** Straight in on the first line, or a short intro that sets the groove in a bar or two. Long intros lose
  listeners; trim them later if they happen (`tools/master.py --start`).
- **Endings.** A real ending: a final hit, a held chord, the hook alone. A fade-out on a music video leaves the picture
  nowhere to land. If a take trails off, end it on its strongest last note and let a tail ring out.

## Choosing a sound

The sound is chosen with the song's concept, before the lyric, because the lyric is written in the genre's voice
(`craft/lyric.md`). Genre, tempo, key and mode, instruments and the voice should all serve the story's feeling, and can
carry irony: a dark story over a bright, cheerful sound is a strong device when it's deliberate. Tempo shapes the film
too: faster songs give more, shorter shots; slow songs want long, beautiful moves.

- **Tempo:** ballads 60–80 BPM, mid-tempo pop 90–115, upbeat pop and rock 115–135, dance 120–130, punk and drum and
  bass faster.
- **Mode:** major sounds open and bright; minor sounds tense or sad; a minor verse into a major chorus lifts.
- **Voice:** gender, range, character (breathy, raw, clean, deadpan, belted), and how it delivers the words (sung,
  talk-sung, rapped). Diction matters: a voice the listener can understand makes a story song work.

## Writing a style prompt for Suno

- A few compatible, specific instructions in priority order: genre and groove, tempo and key, the core instruments, the
  voice and its delivery, the arrangement arc (what changes where), the production feel.
- Describe traits, never artists or songs.
- Say how it starts and ends ("starts on the first line with the full band"; "ends on one held chord").
- Say what happens at the turn ("the bridge drops to half-time with piano; the last chorus is up a key and biggest").
- Exclusions are for real risks: a long instrumental intro, a fade-out, a heavily processed or mumbled vocal, a guitar
  solo where the story needs words.
- The lyric box holds the sung words and plain section tags (`[Verse]`, `[Chorus]`, `[Bridge]`, `[Instrumental]`,
  `[Outro]`, `[End]`), nothing else. Directions inside brackets ("one bar of silence", "up a key") can be sung as words;
  put them in the style prompt instead. Words in parentheses are usually sung as backing vocals.
- Tempo and length words are suggestions to Suno, not settings; use its duration and BPM controls if it has them, and
  expect variation.

## Judging takes without hearing them

What you can measure: how much of the lyric Whisper hears clearly (diction and whether lines were dropped or repeated);
the length; whether every section arrives in order; where the first word starts; whether it ends cleanly or fades;
loudness and clipping; the energy of each section (`tools/beats.py`). What you can't: whether it sounds good. The person
decides that when they listen; when they don't, the measurements decide, and you say so.

## Finishing

- Use the service's own stems for timing and analysis; separating a mix yourself smears the voice.
- Master the chosen take to a consistent loudness (−14 LUFS integrated, −1 dBTP true peak is the streaming norm). Raw
  generations are often quieter and thinner than commercial releases; the master evens that out without changing
  timing.
- Timing for the film always comes from the audio actually used, measured: the voice's onsets on its own stem, the
  beats from the drums.
