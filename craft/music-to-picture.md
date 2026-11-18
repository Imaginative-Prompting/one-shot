# Music to picture

A music video feels right when the picture moves with the music: not every beat illustrated, but the important moments
landing together. Everything here keys to measured data (`song/timing.json`, `song/map.json`), never to guessed times.

## The grid

- **Beats and bars.** At B BPM a beat lasts 60 / B seconds and a 4/4 bar 240 / B. Downbeats (the first beat of each
  bar) are the strongest places to land something.
- **Phrases.** Music moves in phrases of 4 and 8 bars. A change at a phrase boundary feels inevitable; a change in the
  middle of a phrase feels like an interruption, which is useful when you want one.
- **Sections.** The biggest changes in the picture (a new world, a new technique, a new palette) belong at section
  boundaries, especially the turn.

## Energy

`map.json` has each section's energy and how it rises and falls. Match the picture's intensity to it: shot length, camera
speed, how much moves, contrast, saturation. The loudest, densest part of the song is not the place for a slow, quiet
shot, unless the contrast is the point. Plan the film's biggest image for the song's biggest moment.

## Landing on the music

- **Moves start and land on beats.** A camera move that begins on one downbeat and lands on another feels intentional.
- **Anticipate.** Motion takes time to read: start a move slightly before the beat it should land on, so the arrival, not
  the departure, is on the beat. A cut, by contrast, works exactly on the beat or a frame before.
- **Accents.** A prominent note (a piano hit, a snare crack, a vocal stab) can carry a small event: a light flicking on,
  a step, an object landing, a push. Pick the notes that stand out in `map.json`'s accents, not every onset.
- **Held notes and swells** are where the camera moves through a long, smooth arc or something grows.
- **Silence and space** are where the picture can breathe or hold. A sudden drop in the music is a strong moment for
  stillness.

## Words

When a word matters to the picture (a word shown on screen, an action that illustrates it), key it to that word's sung
onset from `timing.json`: the moment the voice actually starts the word, not when the lyric sheet says or when a MIDI
note starts. Sung words stretch; a long held word has an onset and a long tail, and a word can begin with a pickup
before the bar.

## Not everything

Illustrating every beat and every word turns into noise. Choose: the section changes, the turn, a handful of accents per
section, the key words. Let the rest of the picture move with the music's feel (fast or slow, smooth or sharp) without
being locked to its grid.

## Instrumental stretches

Intros, breaks and endings with no singing still have a structure: their own phrases, builds and drops. Give them shots
keyed to those events. They're often the best places for the film's biggest visual moments, because nothing is competing
with the words.
