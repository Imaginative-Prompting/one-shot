# Sets and props

A set is a place that tells part of the story before anyone moves in it. It's designed around what the shot needs the
viewer to see.

## Design

- **A hero object.** Each set has one thing worth looking at that carries the line's idea, built with the most care and
  placed where the camera lands.
- **Detail at three scales.** Big shapes that read at a glance, medium forms that make it a specific place, and small
  details that reward a closer look. A set with only big shapes looks like a blockout.
- **Lived-in.** Signs of the people who use it: a mug, cables, a jacket over a chair, wear on the floor, things slightly
  out of place. Plain is a choice; empty is unfinished.
- **Scale cues.** Doors, chairs, steps and people tell the viewer how big things are. Without them, a set can read as a
  model.
- **The story in the props.** What's on the walls, the screens, the desks says who lives here and what's happening.
- **Built for the camera.** Know where the camera goes before dressing: keep its path clear, put detail where it looks,
  and don't build what it never sees.

## Real things, true to life

Anything the viewer will recognise (a game, a product, a famous painting, an app, a building, a street sign) is built
true to the real thing: its real shapes, colours, rules and proportions, checked against the original at full size.
Random filler that only looks busy reads as fake. Any picture inside the picture (a poster, a book cover, a screen, a
billboard) is finished art made for it, not a title and a flat symbol.

## Secondary text

Screens, signs, papers and packaging carry small, readable text: real-sounding names, dates, messages, in-jokes and
references for people who pause, rather than blank rectangles or gibberish. Keep it small and quiet, so the main words of the
shot stay dominant.

## Sources (free)

- **Poly Haven** (CC0): textures, HDRIs, models. Real materials for almost any surface.
- **ambientCG** (CC0): textures and materials.
- **Quaternius** and **Kenney** (CC0): stylized models and kits.
- **Sketchfab** and **BlenderKit**: many models; check each one's license and credit it in the report.
- **Geometry nodes:** procedural buildings, scattering (rocks, plants, litter), repeated structures, things that
  assemble.
- **Your own models** for anything specific to the story. A distinctive hero object is usually worth building.

Record every downloaded asset's source and license in `films/<slug>/assets.md`; the report lists them as credits.

## Checks

- Nothing floats (every object rests on something), nothing intersects that shouldn't, no two surfaces sit at the same
  depth (they flicker). `tools/blender/clipping.py` reports intersections; stepping through frames shows flicker.
- Nothing pops in as the camera moves: no objects appearing at a distance, no late textures, no culling at the edge.
- Every set is checked full size from every landing the camera makes in it.

## Performance

Many sets in one file render slowly if all their lights and objects are always on. Instance repeated things, and turn
each set's lights (and heavy objects) on only while the camera can see them.
