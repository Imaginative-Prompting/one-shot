# Stage 4: Scenes and shots

The film planned as scenes (environments where something happens) and the shots that live in them, before anything is
built. Read `craft/scenes.md`, `craft/camera.md`, `craft/composition.md`, `craft/transitions.md`, `craft/type.md` and
`craft/music-to-picture.md` first.

## 1. Scenes

Divide the song into scenes using the treatment, `song/timing.json` and `song/map.json`. A scene is one place or world
with its own look and life, holding several lines and several shots; a verse usually has a few scenes at least, and a
scene can come back later in the film, changed. Scene changes are the film's biggest transitions, so put them where the
song and the story change.

For each scene, a card in `shots/scenes.md`:

- **The place,** in a sentence, and why the story is here for these lines.
- **The lines it holds** and its time span.
- **What happens here,** and what's different when we leave from when we arrived.
- **Its look:** palette, light, the hero object, the technique (a 3D set, a 2D passage, a simulation, type as the image).
- **How we arrive and leave:** the transition in from the scene before and out to the next.
- **Whether we come back,** and how it will have changed.

Read the scene list down the whole film: does it build, does each scene earn its place, does the turn land in a new or
changed place? A new scene for every line is a slideshow; one scene for the whole song needs a strong reason.

## 2. Shots within each scene

Inside a scene, the shots are its camera angles and framings, each focused on something. Usually a shot carries one
line, sometimes two or three lines that are one thought, sometimes a line split at a turn inside it. Instrumental
stretches get shots too, keyed to the music's own events. Every frame of the song belongs to exactly one shot.

Think about the scene's coverage as a whole before the single shots (`craft/scenes.md`): how the viewer first meets the
place (an establishing wide, or a detail that reveals it later), where it goes closer, which details get inserts, how
the action's direction holds across shots. These are tools, not a recipe: decide for each scene.

Keep the list as data too, in `shots/shots.json`, which the edit, the clock and the WIP read:

```json
[{ "id": "s01", "scene": "diner", "section": "Intro", "lines": [], "t0": 0.0, "t1": 7.68, "technique": "3D set",
   "status": "planned" }]
```

Shots are in film order, each `t0` is the previous shot's `t1` (seconds of the master), the first starts at 0 and the
last ends at the song's end. `status` goes `planned` → `blocked` → `built` → `done` (final render spliced in).

## 3. A card per shot

`shots/cards.md` (or one file per scene). For each shot:

- **Its scene, the line(s) and their times** (first and last sung onset, from `timing.json`).
- **What the moment means,** in a sentence, and what the viewer should feel.
- **Ideas:** at least three genuinely different pictures for it, and which one you chose and why.
- **Its job in the scene's coverage:** establishing, closer, insert, reaction, reveal, point of view.
- **The move, as a sentence:** "From [start frame], [move] so we [reveal / follow / feel] [what], landing on [end frame]
  on [word or beat]." A locked-off shot can be the right choice; say why.
- **The start and landing frames:** the subject and its size (ECU, CU, MCU, MS, WS, EWS, measured as in
  `craft/composition.md`), where it sits in frame, the camera's height and angle, the lens, what's in the foreground,
  middle and background, and what's at the edges.
- **What passes close to the lens,** and what's far behind (parallax).
- **Speed:** where the move starts, accelerates, and lands, against the beats and accents in `map.json`.
- **In and out:** a cut, a move or a transition from the shot before and to the shot after (`craft/transitions.md`).
  Within a scene, changes are usually simpler; between scenes, they're the big ones.
- **The words on screen,** if any: what they're made of, where they live, when each lands (on its sung onset), and how
  they leave. Or why this line's words don't appear.
- **Anything you're deliberately breaking,** from `craft/` or the treatment, and the reason.

The shot comes first and the words are placed into it. Never shape a camera move to keep words in frame; if a move and the
words fight, change how the words appear.

## 4. Variety, scene by scene

For each scene, a table of its shots' landings: size, camera height, which side of the subject, lens, where the subject
sits. Neighbouring shots should differ clearly (in at least two of these, or by a change of subject) unless sameness is
the point. Read the column of sizes down the scene and down each section: it should go somewhere (wide to close, close
to the widest at the peak), not sit at "medium".

## 5. The film against the music

A short `shots/sync.md`: which musical events drive what. Scene changes on section changes and the turn, downbeats where
moves land or cuts fall, prominent notes that get an accent, held notes the camera moves through, the quiet places where
the picture can breathe. Not every beat gets something; the strongest moments get the strongest events.

## 6. Review

Give the scene cards, the shot cards, the tables, `sync.md`, the treatment and `tendencies.md` to the critic, a section
at a time. Revise until no shot is the first idea you'd have had without trying, no scene is there only to change the
scenery, and no section reads as a template.

## 7. Show it

WIP entry: the scenes (a line each, with the lines they hold), then the shots as a table per scene (line, meaning, shot
in a sentence, size, technique), the variety tables, the sync plan. Check for notes, then stage 5.
