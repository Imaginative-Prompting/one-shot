# Film direction: the AI bubble, from take 3a

Written by the setup session on 16 Nov 2026 (about 22:00 EST), at the person's request: "write the shot direction for
the rest of the film AND ... write in lyric direction for all of the film including the parts I already gave basic shot
direction for". Their own message is at the end, verbatim. Read it first: where this file and their words differ, their
words win.

**Whose is what.** Lines marked **(theirs)** quote or follow their direction closely; keep those closest. Everything
marked **(setup)** was written here because they said "you can decide everything". Treat it as a strong first plan, not a
lock: if an idea doesn't frame well or doesn't read in its four seconds, or a better one turns up while building,
change it and say why in the log. Blocking is never final.

**The song.** Take 3a: round 1, direction 3 ("slyer cabaret", 114 BPM), take A, 3:24,
https://suno.com/song/ff769e0a-6c4a-454c-8b05-535da5f3a365. It sings lyric version 1 (`lyric/lyric.txt`). At 114 BPM a
bar is about 2.1 s, so a two-bar line gives each picture about **4 seconds**. That's the budget for every idea below: one
clear picture per line that reads at a glance, with the small print saved for anyone who pauses. Every time here comes
from the take as measured (`words.py`, `timing.py`, `beats.py`), never from these estimates. The bridge is piano and
voice, slower; the last chorus is up a key with double-time claps; the song stops dead on the last "then—".

---

## 1. The film in one paragraph (setup, built on theirs)

A gleeful, over-the-top capitalist in a top hat dances us into a prairie where the world is betting trillions on
thinking machines. The money piles up, vanishes, and drops him into a pit, and we pull out to find the whole place
inside a soap bubble that wobbles and bursts. Its burst opens on **Main Street of a Wild West boomtown**: the boom side
of the street is warm and sunlit, the bust side cold. The camera rolls down the street, whipping 180° from side to side
as each line flips between the good news and the bad, then turns to face the end of the street: the capitalist, and
the bubble hanging over the town. In verse 2 the town's market becomes a **train**, and the camera rides it through
gold-rush country, still whipping between the sunny side of the tracks and the wrong side. In chorus 2 the camera rises
off the train and the whole world curls up into a **miniature planet** with the bubble as its sky. The bridge stops at a
traveling medicine show where he asks a fortune-telling machine, and gets a very long non-answer. The last chorus brings
the whole town back onto Main Street under a bubble bigger than ever. On the final "and then—" the film cuts to black
before anything happens.

## 2. The look

**2D characters in 3D sets (theirs).** Every character is flat and drawn: ink outlines, flat color, hard-edged shadow
shapes. The sets are real 3D dioramas in the same style: flat-shaded surfaces, ink lines on their edges, one hard light
with crisp cast shadows (theirs: "very bright colors with hard shadows"). Think of each line's scene as a small built
diorama the camera passes, cut open like a dollhouse where we need to see inside.

**Western (theirs: "an overall western theme of the sets for the most part ... that fits the style of the music").**
False-front storefronts, boardwalks, hitching posts, a schoolhouse, a telegraph office, a bank, a water tower, a railroad,
a general store, a saloon porch, a medicine show wagon. Wood type on the signs. The intro sits on the open prairie
outside town, so it can be the most fantastical part.

**The two sides (theirs, refined by setup).** Their words: one side reds and oranges, the other greens and blues; the
warm side for the good news, cold "like blue and green and purple" for the bad.
- **Boom side, warm:** reds, oranges, golds and hot pinks, under a high, bright sun. The lightest values in the film.
- **Bust side, cold:** blues, teals, greens and purples, a low cold light, longer shadows. Clearly darker overall.
- Many color-blind viewers can't separate red from green, so the two sides also differ in **brightness** and in
  **light** (high sun against low cold light), and the main contrast runs warm-against-blue, which most of them do
  see. Check both sides through the color-blind simulations (`tools/checks.py`) on the first look frames.
- In the choruses the two palettes clash in one frame (theirs, from the prompt: "In the choruses the picture clashes the
  two styles").

**The capitalist against both sides (theirs: "needs to be contrastive to the scene on both sides somehow maybe his
color shifts some or maybe his colors are just chosen to contrast well in both scenes").** A setup proposal, open to a
better one: build him mostly on **value**, which reads on any color: a black top hat and tails, a bright white shirtfront,
white gloves and spats, a white handlebar moustache, and gold (the cane's head, a monocle, a watch chain). Then give him
one loud accent (a waistcoat and hatband) that **takes the other side's color**: teal on the warm side, tangerine on the
cold side. It swaps inside the blur of each whip pan, so it never visibly changes on screen. Proving it is a look frame
of him standing on each side.

## 3. The characters

**The capitalist (theirs).** "An overcharacterized capitalist depiction similar to monopoly man but probably a bit more
colorful", 2D. "Simple 2d mouth animations for the singing, but be more expressive in his overall movements with his
cane and everything else." Not a copy of the board-game mascot: his own silhouette (setup: rounder, with a taller hat, a
longer cane and bigger gestures). Setup ideas to try:
- the cane's head is a **gold ring**, so the cane doubles as a bubble wand (used on "Is it gonna pop?");
- a tiny stock-ticker band scrolling around his hat;
- a pocket watch on a chain.

He moves all the time when he's on screen: struts, twirls, leans, points the cane, tips the hat. His dance in the intro
is the first thing anyone sees; make it great.
- **Mouths:** a small set of drawn mouth shapes (closed; A/I; E; O; U; F/V; M/B/P; L), keyed from the vocal stem's
  measured words.
- **Lip-synced lines (setup's pick, about five of 48, so it stays special):** "That's the bubble, baby!"; chorus 1's
  first line; chorus 1's "Tell me when, tell me when!"; the bridge's first line; and the last chorus's first line.
- Theirs: "he isnt always on screen and he also doesnt need to be lip synced every time he is". In the verses he can
  turn up as a small figure in a diorama (buying in the bank, smirking at the pundits) or dancing on the train's roof
  between whips.

**Jensen Huang (theirs: "the depiction of jensen needs to be very good").** 2D like everyone else, not hyperreal, "but I
want his main features like his hair and leather jacket of course to be very accurate."
- Work from many reference photos of his recent keynotes. Search for them; they stay local and never go on the WIP.
- The hair: its real shape, volume and silver-gray color.
- The black leather jacket: its real cut, collar and zips, with a hard specular highlight even in flat color.
- The black T-shirt, the big grin, and his stage pose holding up a chip.
- Make a model sheet (front, three-quarter, profile, three expressions: the grin, a falter, a shrug) and post it to the
  WIP **early** for the person's check, before he's animated anywhere. He's the riskiest likeness in the film.
- The woman in the story is never shown. The satire is about the market's reaction.

**Everyone else (setup).** All generic, none a likeness of a real person:
- a professor in tweed and a bow tie;
- three "pros" (mathematicians in bowler hats and spectacles);
- a robot schoolteacher;
- townsfolk;
- TV pundits;
- Jensen's fans (a few in leather jackets of their own);
- the board (gray suits);
- racing robots, and the monkeys they turn into;
- a fortune-telling robot;
- a saloon band of five, playing the take's instruments: stride piano, clarinet, muted trumpet, upright bass, gypsy-jazz
  guitar.

Anything alive keeps moving.

## 4. The camera

**One continuous camera (theirs, in practice).** Their direction keeps the camera moving from the intro through chorus
1, with the bubble's burst as the one wipe. The rest below follows suit: each scene change rides a move (a whip, a
follow, a rise, a dive) or an object that carries us across. The film's only cut is the last one, to black.

**The street grammar (theirs).** "This whole time we have been moving the camera in one direction and turning back and
forth 180 degrees so when on the bright colors side we are moving the camera to the right and the sad colors side we
move the camera to the left."
- In practice: the camera travels one way along the street (or the railroad) at a steady pace, looking sideways.
- Facing the warm side, that travel reads as moving right; whipped 180° to face the cold side, it reads as moving left.
- Each whip is a fast, motion-blurred 180° pan that lands on the downbeat of the new line (theirs: "whipping the
  camera to the right 180 degrees in a blur transition").
- **Setup's refinement:** warm-to-cold whips turn right and cold-to-warm whips turn left. Both then sweep *through* the
  view straight down the street, where the bubble hangs at the far end, so every whip flashes the bubble past for a few
  frames. When chorus 1 finally stops on that view (theirs: "we turn 90 degrees to the left ... to face the direction we
  have been moving"), it pays off a glimpse we've had all verse.
- The 90° turn left from the cold side is the right direction for that view.

**Reading order on each side (setup, worth knowing).** On the warm side, new things enter from the right edge as the
camera travels, so words laid along the street are revealed left to right, in reading order. On the cold side the
world enters from the **left**, so a line laid along the street would be revealed backwards. Lay out cold-side words so
each line fits in one frame (stacked, or on one sign) instead of relying on the travel to reveal it. That backwards
world drift on the bust side also quietly feels wrong, which suits it.

**Lenses (theirs: "FOV changes to 360 camera size").**
- Normal lenses for the street, wider (around 14–18 mm equivalent) for chorus 1's spin.
- A true **little-planet** (stereographic 360°) move for chorus 2 (theirs: "including the mini world shot for chorus 2
  since i didn't get it in chorus 1").
- In Blender: render the panorama (Cycles' equirectangular camera), then reproject it to stereographic and animate the
  field of view so the street curls into the planet in one continuous move. ffmpeg's `v360` filter has a stereographic
  output, or write a small remap.
- Prove this early on a test set. It's the riskiest shot in the film.

**The bubble is always there (the prompt).** It hangs at the end of Main Street (seen in every whip and in chorus 1), on
the horizon ahead of the train (verse 2), as the planet's sky (chorus 2), in the fortune teller's crystal ball (bridge),
and over the whole town at its biggest (last chorus). It wobbles to the music. In the main story it never leaks and
never thins to a weak spot: those tip the ending toward the pop. The intro's bubble is the one exception, and it does
burst (theirs).

## 5. The lyrics on screen

This is a lyric video (theirs: "I kinda forgot about making this a lyric video"). Every sung line is on screen, and
"not every but almost every line should be a very creative implementation of the lyrics and should be intentional and
should be planned to frame well in the camera shots" (theirs). Their examples: the capitalist singing a line ("dont
overuse this please"), money stacks that spell "WE'RE RICH", and "bubble words that pop out of the bubble itself in an
arc around it."

**How the words live (setup).** The words are **things in the world**:
- painted signs, chalk, ticker tape, telegrams, newspapers;
- bank notes, smoke rings, steam, water;
- branding irons, departure boards, TV chyrons;
- bubble letters.

Each line's treatment comes from what the line says, as listed line by line below. The line-by-line choices are a
starting point; a better idea for a line is always welcome.

**Type.**
- Wood type for most lines: heavy slab serifs and Tuscan display faces from the West's posters.
- A clean condensed sans for screens and chyrons, a chalk hand on the blackboard, a typewriter face for tape and
  telegrams.
- Only openly licensed fonts (OFL), as static instances.
- Lettering is flat with the scene's own hard shadow, so it belongs to the world.

**Reading it (setup, as craft, not rules).**
- Each word appears on its sung onset, measured on the vocal stem.
- Each line stays readable long enough to read twice.
- Words face the camera when they need reading, and stay whole: not cut by the set, not crossed by other moving type.
- They contrast with their background in brightness, not only in hue.
- The **lyric reads first and the signs second**: facts, numbers, dates and names go on smaller signs, newspapers and
  labels, sized to be read on pause, never competing with the sung words.
- When a line's idea would only work by bending the camera, change the idea, not the camera.

**The details on signs (theirs: "legible signs giving more details on the references like what math equations were
solved, maybe even as newspapers or something").**
- Every fact on a sign comes from `research/facts.md` and `research/factcheck-1.md`, worded as carefully as they are.
- Real company logos where the line points at a company (theirs, for the data centers).
- Signs show only what's true, and show a claim as a claim (the proof is "claimed").

---

## 6. Line by line

Format: **Shot** (camera and scene), **Words** (how the line is on screen), **Detail** (signs and small print).

### Intro: the prairie and the bubble (about 4 bars of piano, then 4 lines)

**0. The music before the lyrics (about 8 s)**
- **Shot (theirs):** "introduce the capitalist 2d figure doing some dance that fits well to the song, should be very
  animated and should use his cane an tophat in the dance as well."
- **Shot (setup):** a soft-shoe to the stride piano on a small round vaudeville stage with footlights, on a hill above
  the prairie. Start on his spats tapping on the first downbeat, then tilt up into the dance. A move per bar, landing on
  the downbeats:
  - a hat tip;
  - a cane twirl;
  - the hat rolled down one arm and flicked back onto his head;
  - a freeze, cane pointed off frame at the data centers.
  The camera turns with the cane into line 1.
- **Words:** the song's title on the stage's little marquee behind him, in bulb letters (the title as it is on Suno).

**1. "They're betting trillions on a thinking machine,"**
- **Shot (theirs):** "turn the camera towards a stylized set of datacenters with the different ai company logos above
  them with stylized cash flying towards the datacenters from all directions."
- **Shot (setup):** the data centers are huge windowless barns on the prairie, glowing from their vents, each with a
  company's logo on a tall sign above it like a saloon's. The cash streams in like flocks of birds.
- **Words:** for a beat the flying cash flocks into the shape of **BETTING TRILLIONS** in mid-air, then pours on into the
  barns. **A THINKING MACHINE** lights up in bulb letters across the biggest barn on "machine".
- **Detail:** the logos (OpenAI, Anthropic, Google, Meta, xAI, Microsoft, Amazon, Nvidia: whichever read best).

**2. "on a future no one's ever seen."**
- **Shot (theirs):** "pan the camera up to an idealistic abundant future with flying cars and robots doing chores and
  everything."
- **Shot (setup):** a bright retro-future skyline floating above the barns: flying cars, robots folding laundry,
  walking dogs, watering lawns.
- **Words:** one flying car skywrites the line across the sky in looping script, finishing on "seen."

**3. "If it's real, we're rich."**
- **Shot (theirs):** "the idealistic future scene falls away and a huge pile of stylized money piling up and pushing the
  capitalist guy up where he's just sitting on it."
- **Words (theirs):** "have the money pile instead of being a pile be stacks of money that spell out the lyrics 'we're
  rich'."
- **Words (setup):** the stacks slam up letter by letter on the beat with him riding the top of the **R**. **IF IT'S
  REAL,** is printed on the paper band of the first giant bundle to land.
- **Color (setup):** this is the first fully **warm** moment, so it teaches the film's color code.

**4. "If it's not, we drop."**
- **Shot (theirs):** "all the money disappears in a poof (not a comic poof with the words or something, but like it
  disappears and there is a subtle effect), and then the camera flys above the capitalist as he falls down into a
  bottomless pit that appears."
- **Words (setup):** **IF IT'S NOT,** on the last bill left in the air as the stacks vanish. **WE DROP.** falls into the
  pit after him, letter by letter, with "DROP" falling last and fastest. The camera looks straight down the shaft.
- **Color (setup):** the pit is the first fully **cold** moment.

**5. "That's the bubble, baby!"**
- **Shot (theirs):** "the camera turns to see the capitalist much larger behind the horizon as we zoom out to see that
  the entire scene itself was in a bubble (so the capitalist in this shot is a giant the size of like the moon peaking
  over the horizon as we zoom out to the massive bubble)."
- **Words (theirs):** "on 'that's the bubble baby' have the lyrics be bubble words that pop out of the bubble itself in
  an arc around it."
- **Words (setup):** the giant capitalist sings "baby!" with a wink (lip-synced). The bubble words bud out of the film
  one word at a time and float, iridescent, in an arc over the top of the bubble.

**6. "Will it pop?"**
- **Shot (theirs):** "the bubble starts wobbling around and then it bursts just a bit after the will it pop to
  transition us into verse 1 (the bubble popping fills the screen for a clean transition)."
- **Words (setup):** **WILL IT POP?** is written on the bubble's own film and wobbles with it. When it bursts, the
  letters break up with the film into droplets.
- **Transition (setup):** the burst's edge sweeps across the frame as a thin iridescent sheet. Behind it is Main Street,
  already moving. No white flash.

### Verse 1: Main Street (theirs: warm lines 1–4, cold 5–6, warm 7–8, cold 9–10)

Theirs for the whole verse: "Now I want to have each of the different lines contribute to a scene ... What goes on in
these shots should probably be diorama like scenes with objects describing the lines and what they are referencing
well probably with legible signs giving more details on the references."

Setup: as the bubble's film clears, the first thing in frame is the town's sign, **WELCOME TO BOOMTOWN · POP. ?** (the
population is a question mark). It's passed in the first second, as line 1 starts.

**1. "A machine just did, or so they claim,"** (warm, camera moving right)
- **Shot (setup):** a red one-room schoolhouse, cut open like a dollhouse. A robot schoolteacher writes a proof across a
  long blackboard at blinding speed.
- **Words:** the line is chalked onto the board in a chalk hand as it's sung, one word per onset. **OR SO THEY CLAIM** is
  painted on a gold-rush **claim stake** that gets hammered into the schoolyard dirt on "claim".
- **Detail:** the board carries the real statement of the **local smoothing conjecture** (the wave equation's estimate
  from harmonic analysis), written correctly from a source, with "PROVED?" and "Lean-checked 19 Oct" beside it. A notice
  on the door reads "OpenAI says its models proved 3 results · 26 Oct · experts still checking".

**2. "some math that put the pros to shame."** (warm)
- **Shot (setup):** three mathematicians at the small desks, their own slates tiny next to the robot's board. They sink
  lower in their seats as the board fills.
- **Words:** the line continues on the board, read left to right as the camera rolls on. On "shame" the robot drops a
  dunce cap lettered **SHAME** onto the nearest pro.

**3. "One professor heard the news come through,"** (warm)
- **Shot (setup):** the telegraph office next door. A professor in tweed (generic, not a likeness of the real one) leans
  over the sounder as the tape spools out.
- **Words:** the line prints onto the ticker tape as it spools, word by word on the clicks. The tape loops up toward
  the lens so it reads.
- **Detail:** a telegram form pinned to the counter: "OCT 26 — MACHINE PROVES LOCAL SMOOTHING CONJECTURE — STOP —
  EXPERTS STILL CHECKING — STOP".

**4. "said 'Historic!' and felt a little blue."** (warm, then the whip)
- **Shot (theirs):** "'felt a little blue' has the professor character turn blue before transitioning into the next
  line by whipping the camera to the right 180 degrees in a blur transition to the next line's scene about datacenters
  which will be in cold colors like blue and green and purple."
- **Shot (setup):** he throws his arms up on "Historic!". On "blue" the color drains down him from the hair to the
  shoes, the only cold thing on the warm side. The whip goes on the next downbeat.
- **Words:** **HISTORIC!** bursts above him as a wood-type newspaper "EXTRA" slapped onto the wall. "felt a little blue"
  is in blue letters that sag.
- **Detail:** a quote card on the wall: "'...this historic development' / 'I feel a twinge of sadness' — Prof. Alex
  Iosevich, University of Rochester, 27 Oct" (his words as reported; he didn't check the proof, so the card doesn't say
  he did).

**5. "Forty towns went out and voted no:"** (cold, camera moving left)
- **Shot (theirs):** "for the datacenter one we will have a few datacenters with the different company logos above them."
- **Shot (setup):** a row of the same barn-like data centers at the edge of town, glowing blue, logos above them. In
  front, a big wooden tally board and a line of townsfolk.
- **Words:** **FORTY TOWNS WENT OUT** is painted across the tally board's header, and tally marks race up to 40 under
  "NO" on the beat. On "no" a giant ballot stamp slams **NO** across the nearest data center's wall. Laid out to fit one
  frame (cold side).
- **Detail:** "BALLOT MEASURES, NOV 3 · NO: 40 · YES: 1 · 10 STATES · OHIO ALONE: 21".

**6. "'Your data center hikes our bills, so go!'"** (cold, then the whip)
- **Shot (setup):** the townsfolk hold up placards and one giant electric bill. An electric meter on a pole spins
  wildly.
- **Words:** the quote is split across three placards raised in order on their onsets: **YOUR DATA CENTER** / **HIKES OUR
  BILLS** / **SO GO!** The last is a wooden arrow sign pointing out of town (leftward, with the travel).
- **Detail:** the bill reads "AMOUNT DUE" with arrows climbing. A poster says "Power bills · water · noise". Whip left
  180° (through the bubble view) to the warm side.

**7. "A chatbot's sales went up ten times this year."** (warm)
- **Shot (theirs):** "the chatbot sales thing into wall street a trillion can be screens we focus in on one being an
  exponential graph."
- **Shot (setup):** the First Bank of Boomtown has a wall of screens in carved wooden frames in its window. The camera
  pushes into one.
- **Words:** the line rides the exponential curve as it draws, climbing with it. **TEN TIMES** is biggest, at the steep
  end.
- **Detail:** "Anthropic · revenue, first half: $1.2B (2025) → $16.3B (2026) · ×13.6", with the logo on the screen's
  frame.

**8. "Next stop, Wall Street: a trillion, so we hear."** (warm, then the whip)
- **Shot (theirs):** "the next being something for the anthropic ipo."
- **Shot (setup):** the next screen is a train depot. A steam train with Anthropic's logo on the engine pulls in under a
  flip-board. This train sets up verse 2.
- **Words:** **NEXT STOP: WALL STREET** clacks onto the departure board, letter flaps flipping on the beat. **A TRILLION**
  puffs out of the smokestack as twelve zero-shaped smoke rings after a "$1,", and "so we hear" trails off small in the
  steam.
- **Detail:** "ANT · Nasdaq · $70–$78 a share · about $1.4 trillion · prices Wed 18 Nov, trades Thu 19 Nov". Update this
  once it lists. Whip right 180° to the cold side.

**9. "The market's dropped three days in a row,"** (cold)
- **Shot (theirs):** "then we turn back to the other side for the stock market falling three days in a row."
- **Shot (setup):** across the street, the screens in the window of *The Daily Bust* (the town paper), three side by
  side, one per day.
- **Words:** split across the three screens, **THE MARKET'S DROPPED** / **THREE DAYS** / **IN A ROW**, all in one frame
  (cold side). As each chunk lands, that day's calendar page tears off and falls.
- **Detail:** "THU 12 · FRI 13 · MON 16 NOV · Nasdaq −2.5% · S&P 500 −1.9% · Dow −739 (Mon)". Down is shown by arrows
  and position, not by red and green alone. Update after Tuesday's close.

**10. "and the guys on TV say, 'I told you so!'"** (cold, then the turn)
- **Shot (theirs):** "and then the news saying I told you so in the same sorta way."
- **Shot (setup):** a wall of old TV sets, each with a smug 2D pundit (generic). They all point at the lens at once on
  "so!".
- **Words:** "and the guys on TV say," runs along a crawl at the bottom of the sets. **I TOLD YOU SO!** is the chyron on
  every screen at once, landing together.
- **Shot (theirs):** "so then we turn 90 degrees to the left I think? to face the direction we have been moving."

### Chorus 1: the end of Main Street (the two worlds clash)

**1. "Is it gonna pop? Is it gonna pop?"**
- **Shot (theirs):** "we see the capitalist and the bubble as he says 'is it gonna pop? is it gonna pop?'"
- **Shot (setup):** a high-noon showdown framing: low and wide, the capitalist in the middle of the street, the bubble
  enormous at its end, warm storefronts on one side of frame and cold on the other. Lip-synced.
- **Words:** he waves the cane, and each "Is it gonna pop?" floats out of its gold ring as a string of bubble letters
  that drift up toward the big bubble and don't pop.

**2. "Are we at the bottom? Are we at the top?"**
- **Shot (theirs):** "a big graph appears and the capitalist points his cane to where we are ... the idea is we have the
  same historical data but from today onward is either an exponential or a crash, and when he says are we at the bottom,
  the graph is the exponential version, and he points to the time now, and when he says are we at the top, the graph
  turns into the crash version and he again taps the point where we are now but now it looks like a different graph."
  Also: "might be better to just stylize our own graph."
- **Shot (setup):** the graph unrolls down from the sky across the end of the street like a painted backdrop. The past
  is in neutral ink and fixed; a vertical "TODAY" line; the future swings like a rope between the two versions.
- **Words:** **BOTTOM?** appears at his cane's tip on the first tap, with the exponential future in warm color.
  **TOP?** appears at the same point on the second tap, with the crash future in cold color.

**3. "Do I put my money in? Do I pull it out?"**
- **Shot (theirs):** "I want money to be falling and flying around in random directions as the camera spins around."
- **Words (setup):** the line is printed on a few oversized bank notes that ride along with the camera's spin, so they
  hold steady on screen while the street whirls behind. Each turns face-on as its words are sung. **IN** notes fly
  toward the lens, **OUT** notes away.

**4. "Nobody knows, but they all love to shout!"**
- **Shot (theirs):** "a bunch of TV screens with news anchors saying things like 'crash imminent' 'liquidate your 401k'
  or 'nvda on sale!' 'its still early' having an equal amount of doomer and hype versions, camera is still spinning
  around and aiming more upward."
- **Shot (setup):** the TVs form a ring around the camera, doom screens cold and hype screens warm, alternating.
- **Words (setup):** the sung line runs as **one continuous news crawl around the whole ring**, so the spin itself reads
  it in order. The anchors' chyrons are what they shout:
  - doom: CRASH IMMINENT, LIQUIDATE YOUR 401(K), IT'S 1999 AGAIN, SELL EVERYTHING;
  - hype: NVDA ON SALE!, IT'S STILL EARLY, BUY THE DIP, THIS TIME IS DIFFERENT.

**5. "Is it gonna pop? Tell me when, tell me when!"**
- **Shot (theirs):** "then the capitalist comes into frame above us now for the 'is it gonna pop?'"
- **Shot (setup):** he leans over the lens from above, upside down to us, singing straight down into it (lip-synced).
- **Words:** smaller bubble letters from the cane for "Is it gonna pop?". His pocket watch swings down on its chain to
  fill the frame, and its face has **WHEN?** where the numbers should be: "Tell me when" on the first swing, "tell me
  when!" on the second.

**6. "I'm in till the day before, and then—"**
- **Shot (theirs):** "then he follows a line graph as its going up and down and up (more up than down) and somehow
  depict that he's about to press the sell button and just waiting for the top of the market for the 'im in till the
  day before, and then'."
- **Shot (setup):** a big brass SELL button on a stand (labelled, so its color doesn't have to carry it), his finger
  hovering and trembling.
- **Words:** the line rides the graph's moving tip, word by word, with "the day before" landing near a peak. The dash in
  "then—" **becomes the graph line itself**, running on past the frame's edge into the unknown.
- **Transition (setup):** the camera follows that line as it stretches out over the land, and it settles into a pair of
  rails across the desert. We drop onto the roof of a moving train, facing forward with the bubble on the horizon, and
  turn 90° right to the cold side for verse 2.

### Verse 2: the train (setup; same grammar: cold lines 1–4, warm 5–6, cold 7–8, warm 9–10)

The market is now a steam train, the camera riding its roof toward the bubble on the horizon. The sunny side of the
tracks is the boom (a gold-rush canyon in reds, oranges and golds, in daylight). The other side is the bust,
literally the wrong side of the tracks (moonlit badlands in blues, teals and purples). Whips as in verse 1. The
capitalist rides the roof and can be glimpsed dancing on it in the forward view mid-whip.

**1. "Jensen in his leather, king of chips,"** (cold)
- **Shot:** a grand keynote stage on a lonely station platform: velvet curtains, and a giant screen behind with a
  glowing chip on it. Jensen in his leather jacket, his grin, holding a gold chip up like a nugget, a crown made of
  chips on his head.
- **Words:** **JENSEN IN HIS LEATHER** in marquee bulbs around the stage's arch. **KING OF CHIPS** engraved on the crown's
  band.

**2. "had to let a secret pass his lips:"**
- **Shot:** a push in to a medium close-up. The grin falters.
- **Words:** the words slip out between his lips as a ribbon of letters. He grabs at it to stuff it back in, and it keeps
  coming.

**3. "he'd had a fling. He quit."**
- **Shot:** on "fling", a newsboy on the platform **flings** a newspaper that slaps flat against a post in frame (the
  pun). On "He quit." Jensen lifts off the crown, sets it on the empty podium and walks off. The spotlight tightens onto
  the crown.
- **Words:** the newspaper's headline: **HE'D HAD A FLING** with **HE QUIT.** stamped across it.
- **Detail:** the paper: "Huang admits affair to staff (8 Nov) · resigns as CEO 'effective immediately' (12 Nov)". If
  he's reinstated before posting, this line and the picture change.

**4. "and in a week the whole stock market sprang a leak."** (then the whip)
- **Shot:** the railroad water tower by the tracks, painted **STOCK MARKET**. On the beats of "in a week", seven holes
  burst in it, one per day, and water sprays out.
- **Words:** **SPRANG A LEAK** arcs out of the biggest hole as letters made of water, splashing as they land.
  "and in a week the whole stock market" is painted across the tower (one frame, cold side).
- **Detail:** a gauge on the tower's leg, "NVDA −13% IN A WEEK". The bubble on the horizon wobbles but doesn't leak.
  Whip left 180° to the warm side.

**5. "The shop he left still doubled what it sold."** (warm)
- **Shot:** a trading post by the tracks, **NVIDIA GENERAL STORE · PICKS · SHOVELS · CHIPS** (in a gold rush, the one
  selling the shovels gets rich). His leather jacket still hangs on the peg by the door. Inside, every crate on the
  shelves splits into two on the beat.
- **Words:** "The shop he left" is painted on the window. On "doubled" the word **DOUBLED** splits into two copies side by
  side. **WHAT IT SOLD** is on the price board.
- **Detail:** a sign in the window, **UNDER INTERIM MANAGEMENT**. A ledger on the counter: "Revenue $96.2B · up 106% on a
  year ago" until Tuesday's results, then the new quarter's numbers (and the lyric's fallback if it no longer doubled).

**6. "The chips fly out the door, as good as gold."** (warm, then the whip)
- **Shot:** gold-ingot chips fly out of the swinging doors in arcs, over the lens and into the train's open boxcars,
  and into wagons with the AI companies' logos.
- **Words:** **THE CHIPS FLY OUT THE DOOR** is painted across the two swinging doors and read as they swing. **AS GOOD AS
  GOLD** is stamped into the ingots like an assay mark, with two or three landing face-up toward the lens.
- **Detail:** whip right 180° to the cold side.

**7. "The fans all signed a note: 'Give back his crown!'"** (cold)
- **Shot:** a crowd of fans on a platform (several in leather jackets of their own), unrolling a petition so long it runs
  alongside the train. One fan holds the crown up.
- **Words:** **GIVE BACK HIS CROWN!** is the petition's heading in big hand lettering. "The fans all signed a note" is
  above it as the title. The signatures scroll by.
- **Detail:** "180,000+ signatures · about 1 in 5 Nvidia employees". Among the signatures, legible: Elon Musk, Tim
  Sweeney, Tobias Lütke (named by CBS).

**8. "So far the board has turned them down."** (cold, then the whip)
- **Shot:** a private railroad car on a siding, through its window a long boardroom table of gray suits.
- **Words:** the line is painted on **a wooden board** hanging over the car's door (the pun). On "turned them down" the
  board swings on its hinge and flips upside down. Through the window, the suits turn their chairs away.
- **Detail:** a nameplate, "INTERIM CEO", and a notice, "CEO SEARCH IN PROGRESS". Whip left 180° to the warm side.

**9. "The smart machines get smarter twice as fast:"** (warm)
- **Shot:** robots race the train along the canyon floor. Each new model catches up at twice the speed of the last and
  overtakes, with version numbers on their racing bibs.
- **Words:** **THE SMART MACHINES GET SMARTER** on a race banner they run under. **TWICE AS FAST** with speed lines,
  stretched as it passes.
- **Detail:** "METR, 5 Nov: progress at about twice the earlier rate".

**10. "each one makes a monkey of the last."** (warm, then the turn)
- **Shot:** as each robot overtakes, the one it passed turns into a monkey (a clean swap, still running, then
  sitting). Behind the leader, a line of monkeys like the march-of-progress drawing run backwards.
- **Words:** the monkeys each hold up a card with one word, in order, read left to right as the camera rolls past:
  EACH / ONE / MAKES / A MONKEY / OF THE / LAST. The newest monkey, at the front, holds LAST.
- **Transition:** turn 90° right to face forward: the train, the capitalist on its roof, and the bubble ahead.

### Chorus 2: the miniature planet (setup, from theirs: "the mini world shot for chorus 2")

**1. "Is it gonna pop? Is it gonna pop?"**
- **Shot:** the camera rises straight up off the train, tilting down, and the lens opens from normal to a 360°
  stereographic view. The land curls into a **tiny round world**:
  - the railroad runs around it like an equator;
  - one half is the warm day side and the other the cold night side, the two worlds clashing on one globe;
  - the bubble is the planet's thin, iridescent sky;
  - the capitalist stands on top, singing up at us.
- **Words:** **IS IT GONNA POP?** runs around the inside of the bubble's shell, curved, twice (two rings, one per sung
  question).

**2. "Or does it go up and never stop?"**
- **Shot:** the track peels off the planet in a rising spiral (an exponential curve), and the train climbs it into the
  sky. The camera follows it up a little, then looks back down.
- **Words:** the line is painted along the spiral's sleepers. "never stop" trails up and away into dots.

**3. "Do I buy the dip? Do I sell the rip?"**
- **Shot:** the planet's skyline is now a stock chart wrapped around the globe, all valleys and peaks. The capitalist
  slides down into a valley and runs up to a peak.
- **Words:** **BUY THE DIP** on a sign at the bottom of the valley, where he scoops up coins. **SELL THE RIP** on a sign
  at the peak, and the chart's paper **rips** through the sign's middle.

**4. "Everybody's got a red-hot tip!"**
- **Shot:** all over the little planet, tiny townsfolk pop out of every window, roof and mine shaft (the projection makes
  them bristle outward like a pincushion), each waving a glowing branding iron.
- **Words:** one iron brands **RED-HOT TIP** into a big wooden sign, with glowing letters and smoke.

**5. "Is it gonna pop? Tell me when, tell me when!"**
- **Shot:** the camera dives back down and the lens closes from planet to normal as we land at the station platform.
- **Words:** the station clock fills the frame. Its face reads **WHEN?** instead of numbers, its hands spinning.
  "Is it gonna pop?" in bubble letters from the cane.

**6. "I'm in till the day before, and then—"**
- **Shot:** the capitalist crouched over a dynamite plunger box stenciled **SELL** (chorus 1's button, now western). A wall
  calendar beside him tears off a page per beat.
- **Words:** the page that stays reads **THE DAY BEFORE**. The dash of "then—" is the plunger's wire, running away along
  the tracks toward the horizon.
- **Transition:** the camera follows the wire along the ground to its far end: a plug in the back of a medicine show
  wagon, as the music drops to piano and voice.

### Bridge: the fortune machine (setup; piano and voice, slower, mock-serious)

The one place the camera stops traveling. Night, lit only by the wagon. Its painted side reads **THE GREAT ORACLE · ASK
THE MACHINE · 5¢**. Inside a glass booth is a fortune-telling robot (generic, no company's mascot) with a crystal ball,
the bubble reflected in it. The palette mixes both sides, with warm lamplight on the capitalist and a cold glow from the
machine.

**1. "So I asked the machine: is it gonna pop?"**
- **Shot:** he drops in a coin and feeds in a typed ticket (lip-synced).
- **Words:** **SO I ASKED THE MACHINE** on the booth's marquee. **IS IT GONNA POP?** typed on the ticket as it's swallowed.

**2. "It said, 'Great question!' and it wouldn't stop:"**
- **Shot:** the machine whirs awake and a fortune card starts printing. It never stops: an endless ribbon of paper
  spools out, curls round the capitalist and fills the wagon.
- **Words:** **GREAT QUESTION!** heads the card in big type. "and it wouldn't stop" runs along the ribbon as it unspools.

**3. "'On one hand, boom. On the other hand, bust.'"**
- **Shot:** the robot raises two hands. In one palm sits a tiny warm boomtown in its own little bubble, in the other a
  tiny cold bust town.
- **Words:** **BOOM** on the first palm, **BUST** on the second, lit on their words. "On one hand," / "On the other hand,"
  on the robot's two cuffs.

**4. "'This is not advice.' In bots we trust!"**
- **Shot:** the camera pushes in on the very end of the ribbon, where tiny print reads **THIS IS NOT ADVICE**. Then the
  machine dispenses a dollar bill: the robot's portrait in the oval, and **IN BOTS WE TRUST** where the real motto goes.
  The capitalist holds it up to the lamp, delighted.
- **Words:** the fine print, then the bill itself.
- **Transition:** he flicks the bill up into the air. The camera follows it as the band crashes back in up a key, and it
  flutters down onto Main Street.

### Last chorus: everyone under the bubble (setup; the biggest)

Back on Main Street, facing down it like chorus 1, but now both sides are packed with **every character from the film**:
- the robot teacher and the pros;
- the professor (still a little blue);
- the townsfolk with their NO placards;
- the pundits on their TVs;
- the fans with the petition, and the board on their car's roof;
- the racing robots and the monkeys;
- the oracle machine on its wagon.

The saloon band plays on the porch. The bubble hangs over the whole town, bigger than ever, trembling to the claps.

**1. "Is it gonna pop? Is it gonna pop?"**
- **Shot:** chorus 1's showdown framing, but twice as full. The whole street sings it with the capitalist: simple shared
  mouth shapes, lip-synced.
- **Words:** one giant bubble-letter **IS IT GONNA POP?** blown from his cane, rising over the crowd.

**2. "The band's still playing, so I can't stop!"**
- **Shot:** the band on the saloon porch. The capitalist dances again, the intro's dance bigger, with the cane and the hat
  (a bookend).
- **Words:** **THE BAND'S STILL PLAYING** painted on the bass drum's head. **SO I CAN'T STOP!** on the front of the piano.
- **Detail:** a newspaper on the porch boards: "July 2007, Citigroup's chief: 'As long as the music is playing, you've
  got to get up and dance.'" (a deep cut for anyone who pauses).

**3. "Do I put my money in? Do I pull it out?"**
- **Shot:** the bank's double doors. He bursts in with money bags and straight back out with them, in and out.
- **Words:** **IN** and **OUT** on the two doors. The line in gold leaf across the bank's window.

**4. "I did both this morning, and I'm still in doubt!"**
- **Shot:** there are suddenly **two** of him, one tinted warm and one cold, colliding in the doorway with their bags,
  then both shrugging at the lens. The bank clock reads 9:30.
- **Words:** **I DID BOTH THIS MORNING** across the clock's banner. **AND I'M STILL IN DOUBT!** as one big question mark
  painted on the window behind them, with the words around it.

**5. "Is it gonna pop? Tell me when, tell me when!"**
- **Shot:** the whole street turns to look up at the bubble, and the camera cranes up over the crowd toward it.
- **Words:** every sign in the film flips to **WHEN?** at once: the placards, the petition, the chyrons, the tally board
  and the oracle's marquee. "Is it gonna pop?" as bubble letters.

**6. "I'm in till the day before, and then—"**
- **Shot:** he's back on top of a money pile (the intro's "WE'RE RICH" stacks), finger over the SELL button, calendar
  pages flying.
- **Words:** the line rides a graph line again (chorus 1's device), and its dash runs out across the sky.

**7. "Is it gonna pop? Is it gonna pop?"**
- **Shot:** the camera pulls up and back, out through the bubble's wall, and the whole town is inside it (the intro's
  reveal, now with everything we've met). It hangs in the dark, trembling.
- **Words:** bubble words arc around the bubble, as in the intro's "That's the bubble, baby!".

**8. "I'm in till the day before, and then—"**
- **Shot:** the bubble at its fullest, holding. On "then—" the song stops dead and the film **cuts to black** before
  anything happens. No pop and no sound after: the not knowing is the ending (the prompt).
- **Words:** **AND THEN—** written on the bubble's film. The dash is still drawing when the cut comes.

---

## 7. Staying current (from the prompt)

The lines and signs that may change before the person posts (around Sat 21 Nov), from `research/facts.md`:
- **Nvidia's results (Tue 17 Nov, evening):** verse 2 line 5's lyric and ledger.
- **The market's streak (Tuesday's close):** verse 1 line 9 and its screens.
- **Anthropic's listing (prices Wed 18, trades Thu 19 Nov):** verse 1 line 8's lyric and departure board.
- **Jensen (any day):** verse 2 lines 3, 7 and 8 if he's reinstated.

A changed lyric means a sung change, so ask the person before any new Suno generation. A changed sign is just a rebuild.

## 8. What to show the person first (setup)

Through the WIP, early, so they can steer before the expensive parts:
1. The capitalist's model sheet and a few dance poses.
2. Jensen's model sheet.
3. One look frame each of the warm side, the cold side and a whip in the middle, with the capitalist on both sides
   (checked through the color-blind simulations).
4. The little-planet test move.
5. The intro blocked to the song as an animatic.

---

## Their words (16 Nov 2026, about 21:5x EST, verbatim)

> I want to just go through the whole lyrics and write the real one shot prompt from here as a starting point basically.
>
> - 8 ish seconds of music before lyrics: introduce the capitalist 2d figure doing some dance that fits well to the song, should be very animated and should use his cane an tophat in the dance as well
> 'they're betting trillions on a thinking machine' - turn the camera towards a stylized set of datacenters with the different ai company logos above them with stylized cash flying towards the datacenters from all directions
> 'on a future noones ever seen' - pan the camera up to an idealistic abundant future with flying cars and robots doing chores and everything
> 'if its real we're rich' - the idealistic future scene falls away and a huge pile of stylized money piling up and pushing the capitalist guy up where he's just sitting on it,
>
> then 'if its not, we drop' all the money disappears in a poof(not a comic poof with the words or something, but like it disappears and there is a subtle effect), and then the camera flys above the capitalist as he falls down into a bottomless pit that appears and then the camera turns to see the capitalist much larger behind the horizon as we zoom out to see that the entire scene itself was in a bubble(so the capitalist in this shot is a giant the size of like the moon peaking over the horizon as we zoom out to the massive bubble), and that's for the 'that's the bubble baby!' and then on the will it pop, the bubble starts wobbling around and then it bursts just a bit after the will it pop to transition us into verse 1(the bubble popping fills the screen for a clean transition).
>
> Now I want to have each of the different lines contribute to a scene, so a machine did, or so they claim some math that put the pros to shame, one professor... through historic are all warm tones in the stylized look I was talking about with simple colors and hard shadows and lines then 'felt a little blue' has the professor character turn blue before transitioning into the next line by whipping the camera to the right 180 degrees in a blur transition to the next line's scene about datacenters which will be in cold colors like blue and green and purple.  What goes on in these shots should probably be diorama like scenes with objects describing the lines and what they are referencing well probably with legible signs giving more details on the references like what math equations were solved, maybe even as newspapers or something, I'm feeling an overall western theme of the sets for the most part if you can manage that since that fits the style of the music.  We do the same sort of sets for the other lines so for the datacenter one we will have a few datacenters with the different company logos above them, the chatbot sales thing into wall street a trillion can be screens we focus in on one being an exponential graph, the next being something for the anthropic ipo, then we turn back to the other side for the stock market falling three days in a row and then the news saying I told you so in the same sorta way.
>
> This whole time we have been moving the camera in one direction and turning back and forth 180 degrees so when on the bright colors side we are moving the camera to the right and the sad colors side we move the camera to the left
>
> so then we turn 90 degrees to the left I think? to face the direction we have been moving and we see the capitalist and the bubble as he says 'is it gonna pop? is it gonna pop?' then for the 'are we at the bottom are we at the top?' a big graph appears and the capitalist points his cane to where we are, we have a graph of the stock market or something, might be better to just stylize our own graph, but the idea is we have the same historical data but from today onward is either an exponential or a crash, and when he says are we at the bottom, the graph is the exponential version, and he points to the time now, and when he says are we at the top, the graph turns into the crash version and he again taps the point where we are now but now it looks like a different graph.
>
> For do I put my money in do I pull it out? I feel like I want money to be falling and flying around in random directions as the camera spins around and 'nobody knows but they all love to shout' then has a bunch of TV screens with news anchors saying things like 'crash imminent' 'liquidate your 401k' or 'nvda on sale!' 'its still early' having an equal amount of doomer and hype versions, camera is still spinning around and aiming more upward then the capitalist comes into frame above us now for the 'is it gonna pop?' then he follows a line graph as its going up and down and up(more up than down) and somehow depict that he's about to press the sell button and just waiting for the top of the market for the 'im in till the day before, and then'.
>
> the depiction of jensen needs to be very good, like all the other characters in this I think I want 2d characters in 3d scenes, I obviously dont want a hyperrealistic jensen, but I want his main features like his hair and leather jacket of course to be very accurate.
>
> I want you to come up with the rest of the direction for the film actually, including the mini world shot for chorus 2 since i didn't get it in chorus 1, but you can decide everything but make sure that its just as detailed as I gave up to this point.
>
> Also I kinda forgot about making this a lyric video, so can you update that for me? basically before you send this prompt to the run session, I want you to write the shot direction for the rest of the film AND to write in lyric direction for all of the film including the parts I already gave basic shot direction for?  not every but almost every line should be a very creative implementation of the lyrics and should be intentional and should be planned to frame well in the camera shots.  a couple examples of things you can do is have the capitalist sing them(dont overuse this please), have the money pile instead of being a pile be stacks of money that spell out the lyrics 'we're rich',  on 'that's the bubble baby' have the lyrics be bubble words that pop out of the bubble itself in an arc around it.  There's tons of stuff you can do for them just make sure they are creative.  you can also talk to the working session tbh about this since it has more context on the lyrics it picked I guess
