# Stage 1: Lyric (about 8 minutes)

What matters most is how it sounds: words that flow, rhyme and sit on the beat, telling a story simple enough that anyone
follows what's happening on first hearing. Research supplies a few true moments and references; it never decides a line.
The picture carries the specifics. It has to be good the first time and fast: the person hears it sung within minutes,
and their ears plus a background review shape the next round.

Read `craft/lyric.md` first (all of it: "Sound first" above all) and the structure part of `craft/song.md`. If the story
needed research, take from `research/facts.md` only the few moments and references that sing well; anything sung is true,
but simple and true beats precise.

## 1. Concepts (about 2 minutes)

Write three genuinely different song concepts in `lyric/concepts.md`. Different means a different way in, not the same
idea reworded: who is singing and to whom, where the story starts, what the hook says, what the turn is. For each, in a
few lines:

- the hook and the title;
- **the sound:** genre, feel and tempo, the voice and its delivery. The prompt may set it; if not, choose what serves the
  story. The lyric is written in this genre's voice, and stage 2's directions are variations within it;
- the arc, section by section, and the turn;
- the scenes it suggests, its central metaphor if it has one, and the deep cuts it could carry.

Pick the strongest for the story yourself, and write why in `log.md`. No critic gate here.

## 2. The lyric (about 5 minutes)

Plan it quickly: the three or four story beats and which section carries each; the length in bars from the target (at B
beats a minute a two-bar line lasts 480 / B seconds; Suno stretches a lyric that's short for the length and rushes one
that's long); each section's rhyme scheme and line length.

**Write the chorus first:** the hook, short and singable, saying what the song is. Then the verses, each telling one
simple beat of the story in pictures, leading to the chorus. Say every line aloud over a steady beat as you write it.
Use a handful of references at most, where they sound good. Put it in `lyric/1/lyric.txt` (only the sung words and
section tags: `[Verse 1]`, `[Chorus]`, `[Bridge]`, `[Outro]`). Then check it:

```sh
python3 tools/lyric.py lyric/1/lyric.txt --html lyric/1/rhymes.html
```

Rewrite every line it marks ✕ (no rhyme near it) or ? (vowel only) unless leaving it unrhymed is deliberate (a hook
line, a punch), every line it calls dense with names and numbers, and any line far longer than its neighbours. Aim for
almost every line end in a rhyme slot to be a real rhyme. Then read the whole lyric aloud to a beat, as someone who knows
nothing about the topic: if a line makes you stumble or needs background to follow, rewrite it. Write `lyric/1/notes.md`
briefly: the references and what they refer to, the facts used, and a scene for each line (stage 3 starts from it).

## 3. The file Suno needs (a minute)

- `lyric/lyric.txt`: the lyric. The film and the timing use this one.
- `lyric/suno.txt`: the same words as they should be sung. Respell names, acronyms and numbers for sound ("A I",
  "twenty twenty-six") and drop quote marks. Use plain section tags only: `[Intro]`, `[Verse]`, `[Pre-Chorus]`,
  `[Chorus]`, `[Bridge]`, `[Outro]`, `[Instrumental]`, `[End]`. Everything about how it sounds (energy, instruments,
  stops, key changes, who sings what) goes in the style prompt, not the lyric box: Suno sings what it finds in a bracket
  it doesn't recognise (a test run's take sang "[Stop: one bar of silence]"). No parentheses unless backing vocals should
  sing those words. Keep it under the lyric box's limit.

## 4. Show it, and the background review

Post the concepts, the pick and the lyric with its rhyme map as one WIP entry, then go straight to stage 2.

In the background, start one critic on the lyric (with the brief, `craft/lyric.md` and `tendencies.md`) and check every
sung fact at its source. When they land (usually while the takes generate or the person listens), write `lyric/2/` with
what's worth changing. It's used in the next round of Creates: one the person asks for, or one you make because the
review found a real problem (a wrong fact, a line that doesn't work sung). Say what changed and why.
