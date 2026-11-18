# Stage 6: Build

Each shot, in film order, made as good as you can make it before the next one starts. The question for every shot is:
what's the most impressive version of these few seconds?

## Time

With no time limit, a shot is finished when you and the critic can't find anything worth improving. With a number of
hours, plan it before the first shot:

```sh
python3 tools/clock.py <film>
```

It reads the start time and hours from `run.json` and the shot list from the cards, and keeps back time for the edit
(the final render, measured from your look frames' render time per frame, plus the final checks). It gives each remaining
shot an equal share of the rest, and it recomputes as you go: a shot that finishes early gives its time to the others.
It also prints the deadline as a clock time. What `run.json` can say about time:

- `"hours"`: the limit, counted from `"started"`.
- `"pauses"`: `[{"from": …, "to": …}]`, time the person paused the run; it doesn't count. A pause with no `"to"` is
  still going.
- `"graceHours"`: extra time the person has said the run can ask for at the end, if it needs it. Plan for the deadline;
  near it, if the film needs more, ask (how much, and what it's for). Their answer goes in `"hours"`.
- `"finalRenderAfterLimit": true`: the person put the final render outside the limit. Then every shot is finished at its
  final look inside the limit (built, lit, reviewed, its draft spliced into the full film and judged), and the final
  render, the delivery file and its checks run after the deadline. Nothing else does: the shots themselves stop changing
  at the deadline, unless the person asks.
- `"deliverySize"`: the size of the final render when it differs from the working size (`"size"`, used for blocking,
  drafts and look frames), for example `[3840, 2160]` for 4K. `render.py --preset final` and `edit.py final` use it.
  Render one look frame at the delivery size early (`render.py --preset look --size 3840x2160`): line widths set in
  pixels, texture resolution and the edges of type all change with size, and its seconds per frame are what the final
  render will cost.
When a shot's share runs out, finish it cleanly (no visible flaws, everything at its final look) rather than leaving it
half-built, and move on. Never thin the bar for later shots to rescue an earlier one; never leave a stretch of the film
at blocking.

## For each shot

1. **Re-read its card** and the shots on either side. Think about the details now: the hero object, what makes the set
   feel lived-in, what the characters do with their hands, what the light comes from, what small thing rewards someone
   who pauses. Write the best ideas into the card.
2. **The scene's set,** built the first time one of its shots is built (later shots in the scene reuse and add to it), to
   the look frames' standard: real materials, detail at several scales, a hero object worth looking at. Use CC0
   libraries where they're better than what you'd make (`craft/sets.md`); build what's specific to the story.
3. **The people:** library motion as the base, retargeted to the rig; hand keys on top for the acting; IK and constraints
   for every contact (feet on the floor, hands on a table, a prop in a hand). See `craft/people.md`.
4. **Light it** for this shot: the key, fill and rim, where each comes from, what's brightest and why. Measure the frame
   (`tools/checks.py --checks exposure`): large areas sitting near white mean the light is wrong, not the camera.
5. **Animate everything with a cause.** Every force moves what it touches, and what it moves follows through. Things
   that are alive move like themselves. See `craft/animation.md`.
6. **The words on screen,** per the card, landing on their measured onsets.
7. **Look at the landings,** rendered full size, one at a time. Run `tools/blender/clipping.py` and
   `tools/blender/framing.py` on the shot. Fix what you find.
8. **Render a draft of the shot** and look at it as motion: step through consecutive frames around every transition,
   contact and fast move; run `tools/checks.py` (flicker, pops, image speed); then watch it at speed with the song.
9. **The critic** gets the card, the landing frames full size, frame strips of the motion, the check numbers, the brief
   and `tendencies.md`. Act on its notes, or write down why not.
10. **Final render** of the shot (`tools/gpu.py`, in chunks of about 15 minutes), checked the same way, then spliced into
    the full film so the full film is always current (`tools/edit.py splice`).
11. **Post it** (the shot's clip and the current full film) and check for notes before the next shot.

Repeat steps 2–9 as many times as the shot needs. When a shot fails review twice for the same reason, go back to its
ideas (step 1) rather than fixing again. The blocking is never final: if a better idea for a shot or a whole scene comes
along, or something doesn't work, scrap it and make the better one, then update the cards, `shots/shots.json` and the
neighbouring shots' transitions.

## After each scene and each section

When a scene's last shot is done, join its shots (`tools/edit.py section <film> <scene>`) and watch them in a row: does
the place hold together, does the coverage read? At the end of a section, join it with the song
(`tools/edit.py section <film> <section>`) and watch it whole, then give the critic the joined section's strips with
the treatment. Fix the seams between shots, the pacing, and any shot that only works alone, before
the next section starts. Post the joined section.

## Saving and rendering

- Save the Blender file before every render. A headless render (`blender -b … -P tools/blender/render.py`) renders the
  file as it was saved, so you can keep building in another Blender while it runs.
- A change to an earlier shot can move a neighbour's camera handles: after any edit to a shot, re-render the frames
  where its curves changed, not just the keys you moved.
- Large frame folders go once their encoded clip exists.
