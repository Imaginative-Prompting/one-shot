# People

People are the hardest thing to make look right and the first thing viewers judge. Decide the cast early, build it on
proper foundations, and check it at full size before anything else is built on it.

## Foundations: don't start from a bare mesh

A good character is a well-made body with a proper rig and real motion underneath, with your acting on top. Sources
that need no sign-in:

- **Quaternius, Universal Base Characters and the Universal Animation Library** (CC0): stylized bodies on one shared
  skeleton, with hundreds of clips (walks, runs, idles, gestures, sitting, interactions) made for that skeleton, so they
  apply without retargeting.
- **MPFB** (the MakeHuman add-on for Blender; its output is CC0): realistic human bodies of any shape and age, with
  clothes, hair and a choice of rigs.
- **Rigify** (built into Blender): a full control rig (IK and FK limbs, foot roll, fingers) for any humanoid body.

With the person's sign-in: **Mixamo** (Adobe): thousands of motion-captured clips and an auto-rigger. Its license allows
use in your film but not redistributing its files, so they stay in the film folder and out of git.

Motion from another skeleton is retargeted onto yours (map bone to bone, match rest poses, then bake); check what the
installed Blender or a free retargeting add-on offers. Always check a retargeted clip from several sides: rest-pose
mismatches show up as twisted limbs.

## Check the lead before the cast

Render the lead full size from the front, the side and the back, standing and mid-walk. Measure each limb's twist
against its rest pose; an IK pole set the wrong way turns a leg backwards and wrings the hips, and it looks like "just
the stylization" on small images. Only when one figure is right do you build others on the same base.

## Look

- **Faces or faceless.** Faces carry emotion but are hard to animate well; a face that's slightly wrong is worse than
  none. A blank or minimal face (a smooth head, simple eyes) can carry a stylized film, with the body doing the acting.
  Choose for the story and the look, and say why.
- **Recognisable people** (a public figure in a satire, a type of person) are built from their defining features:
  silhouette, hair, glasses, signature clothes. Those features get real work: a real garment with its seams and folds,
  real hair, not a recoloured base mesh.
- **Variety in a crowd:** body shape, height, age, clothing, colour, posture. Twins next to each other break the
  illusion.

## Acting

- **The whole body talks.** Without a face, the body is the performance: the spine's line, the weight's shift, the head
  leading, the hands. Moves ripple from the hips out to the fingertips.
- **Line of action.** A strong pose has a clear curve through the body. Stiff, straight, symmetrical poses look like
  mannequins.
- **Weight.** People stand on one leg more than the other, lean into what they do, push off to move.
- **Hands** are posed from the fingertips: relaxed curves, different on each hand, holding things properly. Avoid hands
  parked at the sides or on the thighs, hands mirroring each other, and pointing as the only gesture.
- **Eyes and head lead.** A person looks at something before they move toward it or reach for it.
- **Acting to the words.** Big gestures land on the stressed words of a line; between lines, the body breathes and
  shifts, it doesn't freeze.
- **No twinning:** two people side by side doing the same thing at the same time, or one person's arms moving as mirror
  images, looks mechanical. Keep it for when sameness is the point (a march, a dance line, a crowd under control).

## Contacts and collisions

Feet planted on the floor (no sliding), hands on tables and rails (not sinking in), bodies in chairs (sitting on the
seat), props in hands (moving with them), people passing each other (not through each other). All of these are
constraints and IK targets, then checked with `tools/blender/clipping.py` on every shot.

## Crowds

Many people from a few well-made ones: instances with variation in clothing colour, scale and animation offset; clips
from the library spread across the crowd so nobody moves in sync; detail reduced with distance. A crowd seen in the
background of an earlier shot has to exist from that frame on.
