# Animation

How anything moves: characters, objects, the camera, type. Good animation has a cause, weight, and life.

## Every frame is a function of time

Any frame can be rendered alone, in any order, and comes out the same. Motion is computed from the song's time, never
accumulated frame to frame. Simulations are baked from a fixed starting state before rendering. This is what makes
renders in chunks, re-renders and retimings safe.

## The grammar of a move

A move reads as alive when it has its parts:

1. **Hold:** the thing at rest, so the move has something to start from.
2. **Anticipation:** a small move the opposite way first (a crouch before a jump, a wind-up before a throw). It tells the
   viewer something is coming.
3. **Action:** fast, with acceleration.
4. **Overshoot:** it goes a little past where it's going.
5. **Settle:** it comes back and comes to rest, with a little wobble that dies away.

Not every move needs all five, but a move that starts and stops instantly at constant speed looks mechanical. Ease in
and out; overshoot and settle on stops.

## The twelve principles (Thomas and Johnston)

Squash and stretch (mass and flexibility); anticipation; staging (make the action readable); pose to pose or straight
ahead; follow-through and overlapping action (parts keep moving after the main body stops, at different rates);
slow in and slow out; arcs (natural motion travels in curves); secondary action (smaller motions that support the main
one); timing (the number of frames sets weight and mood); exaggeration (push it further than real, to read clearly);
solid drawing (forms with volume, seen from any angle); appeal.

## Cause and material response

Every action affects what it acts on, and the effect travels:

- **Cause, propagation, consequence.** A force acts somewhere, travels through connected material, and leaves
  follow-through. A hit on one side shouldn't make every part react at once and identically.
- **Travel changes the body.** Accelerating leaves loose parts trailing; a turn throws them outward; stopping lets them
  overtake and settle. Hair, cloth, tails, cables, loose parts all respond to how the body moves.
- **Carry it forward.** After a hit or a move, things don't snap back to how they were. The displaced state carries into
  the next action.
- **Specific to the material.** Rigid, elastic, liquid and granular things respond differently. Things that aren't
  touched don't need to move.
- Decorative wobble, noise or sine waves are not a response. Change the force and the response should change.

## Weight and gravity

Falling things accelerate, starting from rest. Heavy things are slow to start and slow to stop; light things are quick
and floaty. Impacts land: a heavy object hitting the ground compresses, maybe bounces lower each time, and shakes what
it lands on. Things don't float unless something holds them.

## Contacts

Wherever two things touch (a foot on the floor, a hand on a table, a prop in a hand, a body in a chair), the contact is
a constraint, not two animations that happen to line up. Feet don't slide; hands don't sink into tables; held things
move with the hand. In Blender: IK targets on the contact points, Child Of or Copy Transforms constraints for held
props (animate the prop and put the hand's target on it, rather than parenting the prop to the hand, whose twist is hard
to predict). `tools/blender/clipping.py` checks for things passing through each other.

## Alive

Anything alive (a person, an animal, a plant in wind, a crowd) keeps moving in a way true to what it is: breathing,
shifting weight, looking around, reacting. A living thing frozen mid-shot looks dead. But motion needs a cause; life is
specific behaviour, not a generic wiggle.

## Timing to music

Big actions land on beats and accents; the anticipation goes before the beat so the action hits on it. A character can
move with the music's feel (sway in a slow song, sharp in a fast one) without dancing unless the story calls for it.

## Smears and blur

Motion blur at a 180° shutter makes fast motion read smoothly. For stylized animation, drawn smears and stretched forms
do the same job. Without either, fast motion strobes.

## Checking motion

Look at motion as motion: step through consecutive frames at every fast move, contact and transition; look at the
animation curves for spikes and flat tops you didn't intend; then watch at speed. `tools/checks.py --checks pops,speed`
flags sudden jumps and very fast image motion to look at.
