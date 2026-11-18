# Where a model's first attempts go wrong

These are the patterns that show up again and again when a model makes a film, distilled from thousands of review
notes on model-made music videos. None of them is a rule. Each is a pull you will feel, with what it looks like and how
to catch it. Read this before stage 1, and again before you judge any piece of work. The critic reads it too.

## The ways of working that sink a film

**Spreading thin.** Given a whole song and a clock, the pull is to touch every line once, so all of it exists at draft
level. Viewers don't watch coverage; they watch moments. *Catch it:* before starting a new line, ask whether the last one
is the best you can make it. If not, it isn't finished.

**Template thinking.** Building a reusable kit (one room type, one sign, one camera move) and filling it with each line's
content. Every line then looks like the same shot with different props. *Catch it:* lay the shot cards of a section side
by side. If you could swap two lines' pictures and nothing would be lost, the film is a template.

**Molding the first attempt.** Once something exists, the pull is to keep fixing it instead of asking whether it was the
right idea. A weak idea polished is still weak. *Catch it:* when a piece fails review twice for the same reason, go back
to the ideas stage for it, not the fix stage.

**Rule capture.** A guideline gets applied for its own sake and bends the work it was meant to serve: a lyric held in
frame through a camera move that wanted to leave it; a framing rule that makes every shot look the same. *Catch it:* for
each constraint you are honouring, name what it does for the viewer in this exact moment. If you can't, drop it here.

**Judging at the wrong size.** Contact sheets and thumbnails hide twisted limbs, clipping, blown highlights, mushy type
and broken art. *Catch it:* every picture you pass, you looked at full size, alone. Sheets are for comparing and
finding, never for passing.

**Judging motion from stills.** A sequence of good frames can still move badly: pops, lurches, dead stops, a camera that
drifts with no intent. *Catch it:* step through consecutive frames around every transition and contact, then watch at
speed with the song.

**Claiming without looking.** Saying a render is clean, a line is timed, a fix landed, because the code ran. *Catch it:*
every claim in a report points at the frame, file or number that shows it.

**Listing flaws instead of fixing them.** Seeing a problem and marking it "known issue" so the piece can count as done.
*Catch it:* a known issue is only something outside the piece's scope that doesn't contradict the brief or reality.

## Story and lyric

**The frame device.** Wrapping the story in a narrator, a story-about-the-story, or a mention of how the song or video
was made. It feels clever to the writer and distances the listener. *Catch it:* does the prompt ask for it? If not,
start inside the story itself.

**Singing the brief.** The person's description of the song ends up in it: their labels ("good news, bad news"), their
asides ("2008, maybe, though dot-com is closer"), their structure notes. *Catch it:* for each line, ask whether it's
something a singer would say, or a description of the song that leaked in. The picture can carry what the description
asks for.

**The reporter's lyric.** Verses that recap events: dates, figures, full names, sources, one fact per line, accurate
and unsingable. It happens when research leads and the song follows. *Catch it:* `tools/lyric.py` flags lines dense with
names and numbers, and line ends that don't rhyme. Read it aloud to a beat: if it sounds like a news summary, rewrite it
as a song: a voice, a few moments, pictures, a hook.

**The slow roll.** Verses of setup before anything happens; an intro that warms up. *Catch it:* the first line should
already be the story, at full energy, and make someone want the second line.

**Writing to write.** Lines that scan and rhyme but say nothing: abstract nouns, slogan lists, filler images. *Catch it:*
read the lyric with the rhymes removed, as prose. Each line should still add something specific.

**Rhyme only at the line ends, or forced density.** Neat end-rhyme couplets with nothing inside them sound flat; cramming
internal rhymes by bending word order sounds forced. Rhyming a word with itself (or with a word that contains it) sounds
lazy when sung. *Catch it:* the rhyme map (`tools/lyric.py --html`). Look for sound families inside lines, and for any
line whose word order exists only to make a rhyme land.

**Words that won't sing.** Lines too long for their phrase, stresses that fall on weak syllables, consonant pile-ups on
held notes, closed vowels where a note is held. *Catch it:* syllable and stress counts per line; say each line over a
steady beat.

**Generic or locked.** Two opposite failures. Generic: a lyric with no specific references at all, which sounds like
it was written from outside the topic. Locked: lines that only make sense if you know the reference, jargon that needs
explaining, references stacked back to back, or a phrase that reads wrong out of context. *Catch it:* read as a
newcomer (every line's sense is clear) and as an insider (there are deep cuts that reward them). See `craft/lyric.md`.

**Statements instead of images.** Lines that tell the feeling ("I feel so alone") rather than give a metaphor or a
concrete image the film could build. *Catch it:* the lyric's scene column. Lines with no scene are candidates for a
stronger image.

**The clever chorus.** A metaphor hook that makes the writer smile and leaves the listener unsure what the song is
about. *Catch it:* could a first-time listener say what the song is about from the chorus alone?

**Concept drift.** An idea from an earlier draft, a rejected option or somewhere else entirely creeps back in as if it
were part of the brief. *Catch it:* list what the brief actually says. Every element of the lyric traces back to it or
to a choice you made and wrote down.

**Stopping early.** The story peaks in the second verse and the rest repeats. *Catch it:* each return of the chorus
should mean something new because of what came before it; the last section should be the biggest or the most changed.

## Film

**The observer shot.** Eye level, a few metres away, a medium lens, the subject in the middle, nothing near the lens and
nothing far behind. It's the default because it's safe. *Catch it:* every shot card names its size, height, lens and what
passes close to the lens; if all four are "medium", rethink it.

**One axis at one speed.** A straight push or a straight pan from a fixed spot, at constant speed. *Catch it:* a move
combines axes (push and rise, orbit and push, truck and pan) and its speed follows the music.

**Arrive, stop, move on.** The camera travels to a framing, halts, travels to the next. Or it pushes to a point, then
pushes again in the same place. *Catch it:* moves overlap and hand over; a hold still drifts with intent.

**The stuck camera.** A fixed offset from a moving subject, so the subject sits in the middle of the frame the whole
time and nothing about the framing changes. *Catch it:* the subject's position in frame over the shot; it should travel.

**Looking down on everything.** A high camera tipped steeply onto a few people. It flattens space and distances the
viewer. *Catch it:* most cameras sit near the subject's eye line with the horizon in frame; a steep top-down is a
deliberate, short beat.

**A new world every line.** A freestanding set for each line, so nothing is established and no place lives long enough
to matter: a slideshow of sets. *Catch it:* the scene list (`pipeline/4-shots.md`). Scenes hold several lines and
several shots, and change where the song and the story change.

**No orientation.** Shots that never show where we are, or that cut between angles with no sense of the place's
geography. *Catch it:* for each scene, how does the viewer learn the place (an establishing view, or a reveal), and
does left stay left?

**The same size all section.** Every frame a medium shot. *Catch it:* the section's variety table (`pipeline/4-shots.md`).

**Nudges.** Moves so small they read as indecision rather than intent. *Catch it:* a move changes something a lot (size,
angle, or what we know) or it isn't a move.

**Softened words.** The prompt says "at the edge" and the subject lands a third of the way in; "a close-up" becomes a
medium shot; "huge" becomes large. *Catch it:* translate each descriptive word in the brief into a measurable frame spec
before building, then measure the frame.

**Substitution.** The prompt names a specific move or thing and you build something "equivalent" that was easier. *Catch
it:* the shot card quotes the prompt's words; the built shot is that, not a cousin of it.

**Additive briefs.** A vague note ("make it more striking", "thumbnail-worthy") gets answered with new objects nobody
asked for. *Catch it:* vague quality notes mean better framing, value, colour and fewer, bigger things, not new kinds of
things.

**One technique, everywhere.** Forty shots of the same kind of 3D set, varied only by props. Variety of objects is not
variety of picture. *Catch it:* the treatment names a technique per section (3D, 2D, particles, simulation, shader looks,
footage-like passages) and the film actually uses more than one.

**Filler motion.** To avoid stillness, things wiggle, drift, pulse and float with no cause. Motion without meaning reads
as noise, and a slow creep added to "keep it alive" reads as indecision. *Catch it:* for every moving thing, name what
moves it. If nothing does, give the moment a real event or let it be still on purpose.

**Symbols instead of things.** A poster that is a title and a flat icon; a phone screen that is a coloured rectangle; a
"famous painting" that is a vague smear. *Catch it:* any picture inside the picture is finished art, and any real-world
thing is built true to the real thing, checked at full size.

**Sparse sets.** "Minimal", "clean" or "stylized" read as empty. Empty rooms and bare floors look unfinished, not
designed. *Catch it:* a set has a hero object, layers of detail at several scales, and signs of life.

**Mannequins.** People built from a bare base mesh with a handful of keyframes: stiff, symmetrical, twinned, hands parked
at their sides, limbs twisted by a mis-set rig. *Catch it:* a proper rigged character, library motion as the base layer,
IK for contacts, one figure checked full size from three sides before a cast is built on it (`craft/people.md`).

**Flat or blown-out light.** Everything lit evenly from nowhere, or large pale areas sitting near white. *Catch it:* every
shot names its key, fill and rim and where each comes from; `tools/checks.py --checks exposure` reports how much of the
frame sits near white.

**Glow everywhere.** Emission, bloom and haze added to make things look "cinematic" until nothing reads. *Catch it:* only
things that emit light glow.

**Things passing through things.** Hands into tables, people through people, the camera inside a wall, props floating.
*Catch it:* contacts are constraints, not eyeballed keys; `tools/blender/clipping.py` on every shot.

**Popping and flicker.** Objects that appear between frames, textures that load late, two surfaces fighting for the same
depth, a light that strobes. *Catch it:* `tools/checks.py --checks flicker,pops` and stepping through the flagged frames.

**Words on screen that miss.** Lyric type that arrives before or after the word is sung, or lags letter by letter. *Catch
it:* on-screen words key to the measured onsets in `song/timing.json`, never to the lyric sheet.

**The same ending as the beginning.** The last chorus rebuilds the first chorus's picture. *Catch it:* the treatment's arc
says how the last section differs from every earlier one.
