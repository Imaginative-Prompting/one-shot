# Working in Blender

Blender is the default engine: one scene can hold rigged characters, real light, 2D drawing (Grease Pencil), particles,
simulation, procedural geometry and stylized shaders, with one camera and real motion blur. Everything is built by
Python scripts you can re-run, so the film is code even when it's a Blender file.

## Working from scripts

- Build each set, cast and camera from scripts in `films/<slug>/blender/build/`, one file per sequence or set, run
  in order by a top-level script. A rebuild from scratch should always be possible. Hand-editing the saved file without
  a script loses the change at the next rebuild.
- Run headless: `blender -b <file.blend> -P <script.py> -- <args>`. A running Blender with an MCP connection is handy for
  looking around, but anything that matters lives in a script.
- Save before rendering: a headless render (`tools/blender/render.py`) renders the file as it was saved, so building can
  continue in another Blender while frames render.
- Time: frame = song seconds × fps. Every key that matters comes from `song/timing.json` or `song/map.json` through
  `tools/blender/markers.py` (which also writes them as timeline markers).

## Render settings

- **EEVEE** is fast and right for most stylized and many realistic looks; raytracing in EEVEE gives better reflections
  and shadows at a cost. **Cycles** is slower and physically accurate; worth it for glass, complex light, realism.
  Measure the time per frame of a finished look frame early: it sets the schedule.
- **Motion blur** on, shutter 0.5 (180°). For transitions that cut inside a blur, the shutter opening at the frame
  (position Start) keeps the cut frame clean.
- **Colour management:** AgX for most looks, Standard for flat or graphic looks and for images that must show exactly.
  Set it once for the film.
- **Volumes and haze** at low sample counts break into a dot pattern; use them sparingly, at enough samples, or fake
  depth with falloff and fog planes.
- **Output:** PNG frames (RGB, 8-bit is fine for delivery; 16-bit for heavy grading), then `tools/edit.py` encodes.

## Things that cost time once

- **Text orientation:** a text object reads correctly from +Z of its own space looking down; when placed on a wall,
  check from the camera that it doesn't read backwards.
- **Rotation signs:** a positive rotation about +X tips +Y up toward +Z, so -Y swings down. Check props that rotate
  (doors, lids, gavels) from the camera after keying.
- **Bezier camera keys:** auto handles mean moving one key changes the path between its neighbours too. After editing
  a key, compare the camera's curves before and after and re-render every frame that changed.
- **A prop in a hand:** animate the prop in the world and put the hand's IK target on it, rather than parenting the
  prop to the hand.
- **Lights that flood:** link a light to the objects it's for (light linking) rather than lowering it until the subject
  is dark.
- **Missing images** in an image sequence texture render magenta; make sure every frame it asks for exists.
- **Long scripts** in a live session can outlast the connection's timeout; write results to a JSON file and read that.

## Checks that run in Blender

```sh
blender -b <file> -P tools/blender/framing.py -- --frames a-b [--subject <object>]   # size, place, seen, camera speed
blender -b <file> -P tools/blender/clipping.py -- --frames a-b[:step] [--only <collection>]  # intersections
blender -b <file> -P tools/blender/markers.py -- <film>                              # words and beats as markers
blender -b <file> -P tools/blender/render.py -- --preset draft|final --frames a-b --out <dir>
```

Each prints numbers and writes a JSON report. They tell you where to look, not whether a shot is good.
