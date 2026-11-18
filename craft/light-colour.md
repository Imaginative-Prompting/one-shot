# Light and colour

Light tells the viewer where to look and how to feel. Colour carries mood and change over time. Both are designed per
shot and planned across the film.

## Light

- **Key, fill, rim.** The key is the main light, and it decides the shape and mood. The fill softens the shadows it
  leaves (or doesn't, for drama). The rim (back light) separates the subject from the background. Place each on purpose
  and know what it represents in the world.
- **Motivated light.** Light seems to come from something: a window, a lamp, a screen, the sky, a fire, headlights.
  Visible sources in the frame (practicals) make a scene feel real and give it a reason to be lit that way.
- **Low-key and high-key.** Low-key (mostly dark, pools of light, strong contrast) is moody, dramatic, intimate.
  High-key (bright, soft, few shadows) is open, cheerful, clean. Choose for the story and the section; a film can move
  from one to the other as part of its arc.
- **Direction.** Front light flattens; side light shows form and texture; back light silhouettes and glows; light from
  below is unnatural and unsettling.
- **Quality.** Hard light (small source, sharp shadows) is dramatic and graphic; soft light (large source, gradual
  shadows) is gentle and flattering.
- **The subject is the brightest thing,** or the highest contrast, unless darkness is the point. The eye goes to the
  brightest area first.
- **Falloff.** Light that fades with distance gives depth and keeps the background from competing. A dark space lit by a
  few sources reads better than a black void or a flatly lit room.
- **Exposure.** Large areas near white (pale walls, paper, skin in a strong light) look blown out even when nothing
  clips. `tools/checks.py --checks exposure` reports how much of the frame sits near white and how much near black;
  look at the frame when either is large.
- **Only things that emit light glow.** Bloom, emission and haze on non-emitting surfaces make a frame murky and
  cheap. Lamps, screens, fire, neon: real levels, at their source.

## Colour

- **Palette per place or section.** A small set of colours that belong together, chosen for the feeling of that part
  of the story. Different sections can have different palettes; the film's arc can be told in colour (cold to warm, grey
  to saturated, one colour slowly taking over).
- **Contrast and affinity.** Similar colours across shots (affinity) feel calm and unified; strongly different colours
  (contrast) feel intense. Increase colour contrast as intensity rises; return to affinity in calm places.
- **Accent.** One colour reserved for one thing (a character, an idea) makes it pop everywhere it appears and turns it
  into a motif.
- **Warm against cool** separates subject from background and creates depth.
- **Saturation** draws the eye; desaturation recedes. A desaturated world with one saturated element is a strong device.

## Colour-blind safe

About one viewer in twelve sees red and green poorly. Don't let anything important depend on telling red from green.
Pairs that stay distinct for most viewers: blue and orange, blue and yellow, dark and light of any hue. Make important
differences differences of value (light versus dark) as well as of hue. Check palettes by looking at them in greyscale
and through a colour-blindness simulation (`tools/checks.py --checks colourblind <frame>`).

## In Blender

- **View transform.** AgX (the default) handles bright light and saturated colour gracefully; Standard shows colours
  exactly as set, for graphic looks, flat colour and anything that must match source images. Choose once for the film.
- **Light linking** keeps a light on the objects it's for (a lamp that should light a face, not flood the floor).
- **Specular on area lights** opposite the camera can mirror off glossy surfaces as a hard rectangle; lower that
  light's specular if it shows.
- **Light per set.** In a film with many sets, turn each set's lights on only while it's on screen; most render time
  goes on lights that aren't contributing.
- **Output** is tagged BT.709 for video; `tools/edit.py` encodes with the right tags.
