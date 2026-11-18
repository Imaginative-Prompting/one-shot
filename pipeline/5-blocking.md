# Stage 5: Blocking

The whole film, roughly, on the song's clock: every scene's layout, every camera move, every subject's place and path,
every shot's timing, with simple shapes standing in for what will be built. It makes the film exist early, so the flow can
be judged as a whole before hours go into any one shot.

**Nothing here is final.** Blocking is a sketch of the plan, not a commitment to it. Any shot or whole scene can be
scrapped and remade, now or during the build, when a better idea comes along or when it simply doesn't work. When you
do, rewrite its cards and `shots/shots.json` so the plan stays true, and say why in `log.md`.

## 1. The scene

In Blender (or the engine the brief chose):

- The frame rate and size from the brief (default 1920×1080 at 30 fps). Song time t is frame t × fps; nothing is keyed by
  hand-typed frames that don't come from `timing.json` or `map.json`.
- The mastered song as the scene's sound, and the words and beats as timeline markers
  (`blender -b <file> -P tools/blender/markers.py -- <film>`).
- Colour management set once for the whole film (`craft/light-colour.md`), output in BT.709.
- One collection per scene (its set) and one per shot (its camera and anything only that shot needs), named after their
  cards.

## 2. Block every shot

- Stand-ins at true scale: boxes and simple shapes for sets and props, the real rig (roughly posed) for characters.
- The camera keyed to the card: the start frame, the landing, the speed profile on the beats. Use real camera
  properties (focal length, sensor) so lens choices are real now.
- Placeholders for any words on screen, at their size and place, timed to their onsets.
- Transitions blocked as they'll be built: the whip, the push through a shape, the cut on an action.

## 3. Probe it

Before rendering, measure each shot (`tools/blender/framing.py`): the subject's size and place at each landing against its
card, whether it's actually seen (not hidden behind something), the camera's turn rates and speed changes, and whether the
camera ever enters geometry. Numbers that disagree with the card are questions: fix the shot or change the card, and say
which.

## 4. The animatic

Render the whole film quickly (low resolution, simple shading), join it with the song, and look:

```sh
python3 tools/gpu.py run --label animatic -- \
  blender -b blender/film.blend -P tools/blender/render.py -- --preset blocking --name blocking --out renders/blocking
python3 tools/frames.py renders/blocking/blocking.mp4 --strip 2 --out renders/blocking/strips
```

Step through it, then watch it at speed against the song's map. Does the film build? Do sections differ? Does the
turning point land? Is any stretch the same shot over and over? Then give the critic the animatic's strips, the landing
frames and the plan.

## 5. Show it

WIP entry: the animatic with the song. This file is the film's skeleton: from now on, each built shot replaces its
blocked version and the full film stays current (`pipeline/6-build.md`). Check for notes, then stage 6.
