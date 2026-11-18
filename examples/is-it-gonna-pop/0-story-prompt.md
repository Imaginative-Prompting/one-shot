# The story prompt (16 Nov 2026, about 18:53 EST), exactly as the run got it

The opening message of the session that wrote the lyrics, made the song and then (after the direction) the film. The prompt itself is the quoted part, which I wrote with Claude after hearing earlier attempts. The lines around it were added by the setup.

Make a music video, following AGENTS.md from stage 0. The person's prompt (16 Nov 2026, 18:5x), written with them; they asked for it to be adjusted after hearing an earlier attempt:

> Make a music video about the AI bubble.
> 
> The idea: right now there are two schools of thought about AI. Accelerationists believe the exponential growth of AI
> turns into abundance. Others believe it will follow markets like the dot-com bubble into a major crash, and that
> everything in AI right now is insanely overvalued. The song bounces back and forth between the two: a couple of lines on
> something good that's happened in AI in the past few weeks, then a couple on something bad (like the Jensen Huang story,
> or the backlash against data centers), and back again. The lyrics don't label which is which; they just say the lines,
> and the visuals show the difference.
> 
> This is a song for a music video: the visuals tell some of the story, so the lyrics don't have to cram everything in.
> The song should still stand on its own.
> 
> The singer is satirical and gleeful, like the style of this song: https://suno.com/song/24c95ee7-ca3f-4a09-af5e-67c999711773
> 
> The shape:
> - A short, punchy intro that explains what the AI bubble is. I liked this one from an earlier try; keep it or make
>   something at least as good:
>   "They're betting trillions on a thinking machine, / on a future no one's ever seen. / If it's real, we're rich. If
>   it's not, we drop. / That's the bubble, baby! Will it pop?"
> - Each verse opens with a longer stretch on one side, then goes back and forth with the other side a couple of lines at
>   a time before the chorus.
> - The chorus asks whether the bubble is going to pop, and when, and brings in the stock market side, since that's what
>   most people are wondering: should I put my money in, or take it out before it pops? The chorus changes some each time
>   it comes back rather than being the same every time. I liked the direction of this one from the earlier try:
>   "Is it gonna pop? Is it gonna pop? / Are we at the bottom? Are we at the top? / Do I put my money in? Do I pull it
>   out? / Nobody knows, but they all love to shout! / Is it gonna pop? Tell me when, tell me when! / I'm in till the day
>   before, and then—"
> - Length: about 3:20.
> - It ends without an answer: we keep it ambiguous whether it pops, and the not knowing can be part of the song.
> 
> The film whips back and forth between two settings: a world where the bubble pops and a world of abundance. In the
> choruses the picture clashes the two styles. A bubble on the verge of bursting is there the whole time, and at the end we
> still don't know if it bursts.
> 
> The news is still developing: Nvidia reports earnings tomorrow (17 Nov) and the Jensen Huang story is still moving. I
> want to post the video around Saturday, so if things change (bad earnings, Jensen reinstated), lines may need to be
> updated to stay current. That's fine.

Notes about this machine (from the setup, not part of the prompt):
- The WIP is connected (settings.local.json): the person watches it at http://127.0.0.1:7353 and writes notes there.
- Suno is signed in in the person's Chrome; Mixamo is signed in too. Download nothing from Suno until the person picks.
- Renders, Blender frame batches and Whisper go through tools/gpu.py, which joins this machine's shared GPU queue. Other
  projects use the same GPU, so tickets can wait; keep working while they do.
- Don't use Codex (codex exec) unless the person says yes in chat.
