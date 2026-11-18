# Stage 3: Treatment

## The look track (starts during stage 1)

As soon as the song's concept and sound are chosen, start a helper (a general-purpose agent, in the background) on the
film's look, so style references exist by the time the song does. Give it the brief, the concept, the sound, the scenes
the lyric suggests, and `craft/look.md`, `craft/light-colour.md`, `craft/people.md`, `craft/sets.md`, `craft/blender.md`.
It builds, in Blender:

- two or three different style directions, each as one sample scene rendered full size (a real set, real light, real
  materials, at the film's size), for the places the story will probably go;
- the lead character (and any recognisable person the story needs) in the leading style, checked full size from the
  front, side and back.

It writes into `treatment/look/` and posts each frame to the WIP as it's made, so the person can react early. These are
references, not the film: the treatment below chooses from them, and a look can change once the song exists.

## The treatment (after the song)

The film's one idea, made now that the song exists. Read `craft/story.md` (the film half), `craft/look.md`,
`craft/light-colour.md`, `craft/people.md`, `craft/sets.md` and `craft/music-to-picture.md`, and the song's `map.md`.

## 1. Treatments

Write at least four genuinely different treatments in `treatment/options.md`. They can differ in kind: a narrative that
follows people through the story; a single world that transforms as the song goes; a metaphor made physical; a graphic,
typographic or abstract film; a performance; a hybrid. For each:

- the idea in one sentence, and what the viewer should feel at the end;
- the arc across the song's sections, using the map: what each section shows, how the turning point lands in the
  picture, how the last section differs from every earlier one;
- the look in a few words, and the techniques it would use where (3D sets, 2D animation, particles and simulation,
  shader-driven looks, type as the image);
- who's in it, and what it needs to build;
- what's hard about it, honestly.

Give the options, the brief, the lyric and the map to the critic. Pick the strongest for the story, not the easiest to
build. Write `treatment/treatment.md`: the chosen idea, the arc section by section, and the lines of the lyric whose
pictures are the film's key moments.

## 2. The look

Write the look in `treatment/look.md` and prove it in pictures:

- **The style and its structure.** What makes it a style rather than a filter: shading, edges and line, texture, how
  light falls, how type looks. How it shifts between sections, and what stays constant so it reads as one film.
- **Colour.** A palette per section or place, chosen for what each moment should feel like, and how colour changes
  across the arc. Check that the palettes stay distinguishable for colour-blind viewers (`craft/light-colour.md`).
- **Light.** The approach (low-key with practical sources, bright and flat, theatrical, natural) and why.
- **Camera language.** How the camera behaves in this film: one continuous camera, cuts, handheld, locked-off and
  graphic. If the prompt asked for a continuous camera, read `craft/camera.md` ("One continuous camera").
- **The words on screen.** Whether and how the lyric appears, and the secondary text in the world (`craft/type.md`).

Then build two or three look frames in the chosen engine for the film's key moments: real sets, real light, real
materials, at full resolution. Look at each full size, alone. Give them to the critic with `look.md`. Revise until the
frames look like the film you described. These frames are the bar for every shot that follows.

## 3. The cast

If the film has characters, decide now, before any set: who they are, how they look, whether they have faces (and why),
and where their motion comes from. Read `craft/people.md`. Build the lead first: the rig, the clothes, the hair. Render
them full size from the front, side and back, standing and mid-walk, and measure that no limb is twisted against its
rest pose. Only then build anyone else on the same base.

## 4. What the world needs

List the sets, props, assets and references the film needs, and where each comes from (built, a CC0 library, a sign-in
the person gave). Anything recognisable from the real world is built true to the real thing. Any picture inside the
picture (a poster, a screen, a cover) is finished art, made for it.

## 5. Show it

WIP entry: the treatments considered and the chosen one, the look frames, the lead's turnaround, the critic's verdict.
Check for notes, then stage 4.
