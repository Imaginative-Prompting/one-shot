# Camera

The camera decides what the viewer sees, how close they are, and how they feel about it. Every shot and move should have
a reason you can say in a sentence.

## Size

Measured on the frame, so a card's words become numbers:

| Size | What fills the frame | Feels |
|---|---|---|
| ECU, extreme close-up | a detail (an eye, a hand on a key) fills most of the width | intimate, intense, significant |
| CU, close-up | the head, a third to half of the frame's height | emotion, connection |
| MCU, medium close-up | head and chest | conversation, attention |
| MS, medium shot | waist up | action with expression |
| WS, wide shot | the whole body, a third to half the height, with surroundings | the person in their place |
| EWS, extreme wide | the subject small, under a tenth of the height; the world is the subject | scale, isolation, context |

A section that moves between sizes feels alive; one that stays at medium feels flat. The film's biggest emotional moments
usually go close; its biggest reveals go wide.

## Height and angle

- **Low** (below the subject's waist, looking level or up): power, scale, awe.
- **Eye level:** connection, neutrality. Keeping the horizon in frame grounds the viewer.
- **High** (looking down): vulnerability, pattern, overview. A steep top-down is graphic and detached; use it for short,
  deliberate beats.
- **Dutch** (rolled): unease. Rarely, and on purpose.

## Lens

- **Wide** (14–28 mm on a full-frame sensor; a vertical field of view of 60° or more) close to the subject: energy,
  immersion, exaggerated depth, things rushing past.
- **Normal** (35–50 mm): natural.
- **Long** (85 mm and up; under about 25°) from far away: compression, isolation, intimacy at a distance, a flattened
  crowd.

A normal lens at a middle distance is the most neutral choice possible; make it a decision, not a default. Move the
camera to make something bigger; don't zoom, unless the zoom itself is the effect you want.

## Moves and what they do

- **Push in (dolly in):** attention, realisation, tension.
- **Pull out:** reveal, context, isolation, an ending.
- **Truck (sideways):** following, surveying; with something in the foreground, strong parallax.
- **Pedestal or crane (up and down):** revealing scale, rising emotion, an overview.
- **Pan and tilt (turning on the spot):** following, revealing what's beside; a quick whip pan is a transition.
- **Orbit (arc around the subject):** importance, a moment held in time; it needs to travel far enough (45° or more) to
  read as an orbit, and stay centred on the subject.
- **Handheld:** presence, urgency, documentary feel. Real handheld has weight and lag, not random noise.
- **Drone or FPV:** flight. A flown path, banking into turns, passing close to things, with real speed changes.
- **Locked off:** stillness as a statement; graphic compositions; letting the action carry the frame.

## A good move

1. **One idea, written first.** "From [start], [move] so we [reveal / follow / feel] [what], landing on [end] on [beat or
   word]." A move with no verb but "show" has no reason.
2. **Something changes a lot.** Over the move, at least one of: the subject's size (doubles or halves), the angle (45° or
   more around them, or a metre or more of height), or what we know (a reveal). A move that ends where it started is
   wasted.
3. **Combined axes, one leading.** Push and rise (crane in), pull and rise (reveal), orbit and push (spiral), truck and
   pan (parallax slide). Pure single-axis moves read as mechanical.
4. **Parallax.** Something near the lens (a shoulder, a leaf, a railing, a passing car) crossing the frame, and something
   far behind. That is what makes a move feel like moving through space.
5. **Reveal structure.** Start tight or blocked, then open; or start wide and push to the one thing that matters. Put the
   reveal on the music.
6. **Speed follows the music.** It starts and lands on beats, speeds into accents, eases through held notes. One rise and
   one fall of speed per move, no lurches.
7. **Decisive.** Each parameter (distance, height, heading, aim) moves one way during a move. A camera that swings past a
   framing and back, or nudges a little left then right, reads as indecision. Turn the aim smoothly; don't drag a look-at
   point around.
8. **Holds still have life.** A hold can be a slow, directional drift, a hover, or a deliberate dead stop for emphasis.
   Use dead stops rarely; use slow creeping drifts only when they mean something.
9. **Smooth, by the numbers.** Turning faster than about 90° a second, or changing speed sharply, reads as a jolt unless
   it's a deliberate whip with motion blur. `tools/blender/framing.py` reports turn rates and accelerations.

## Depth of field and blur

- Shallow focus isolates the subject and adds depth; deep focus shows the whole world. Pull focus to move attention.
- Motion blur at a 180° shutter (half the frame time) looks like film. Without it, fast motion strobes. Fast whips need
  it.

## Cuts or one camera

Both are languages. **Cuts** compress time, juxtapose, punctuate the music. Cut on action, on the beat, between shots
that differ clearly in size or angle (a cut between nearly identical framings looks like a mistake). **One continuous
camera** (below) immerses and makes the whole film one journey. Many films mix them: continuous within a section, cuts
between sections.

## One continuous camera

A film shot as a single unbroken camera that flies between compositions, used when the prompt asks for it or the
treatment chooses it.

- **The camera never cuts.** Every change of shot is a move: a fast whip, an arc around something, a pull out and push in,
  a flight to the next composition.
- **Each line still gets its own composed frame.** The camera arrives at a designed landing for each line or phrase,
  sits with it (alive, not frozen), then travels on. Travel is short and motivated; the time belongs to the subjects, not
  to the trip between them.
- **Changing worlds without a cut:** pass through a real object that fills the frame (a doorway, a screen, a dark shape,
  a hand) and come out somewhere else; push into a shape (a window, a circle, an eye) and let the next world grow
  inside it; whip past something with motion blur. The hero goes through first and is seen on the other side at the same
  place in frame. Nothing flashes white or fades to cover the swap.
- **Momentum.** Moves overlap: the next one begins easing in before the last one finishes. Speed rises into transitions
  and settles into landings, keyed to the music.
- **Real motion blur** on every move, so fast travel reads as speed rather than as a jump.
- **Space stays consistent.** Places the camera has passed can still be there behind it; the world has a geography the
  viewer can feel.
