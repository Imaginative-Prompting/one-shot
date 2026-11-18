# Is It Gonna Pop? (the prompts)

Everything I wrote for this one, and the full direction that Claude and Codex each made their music video from.

- Claude's film: https://www.youtube.com/watch?v=lOzNg0pUnmU
- Codex's film: https://www.youtube.com/watch?v=xW3cD6YALIM
- What I'd change in each one: https://www.youtube.com/watch?v=HqhIITgB9c4

## What I wrote

| File | What it is |
|---|---|
| [0-story-prompt.md](0-story-prompt.md) | The story prompt that started the run. I wrote it with Claude after hearing a few earlier tries at the song. From it the run wrote the lyrics and made the song in Suno. |
| [1-the-look.md](1-the-look.md) | My first message about how the video looks, sent after I heard the take I liked. Yes, "obviously". |
| [2-my-direction.md](2-my-direction.md) | My shot-by-shot direction for the intro, verse 1 and the first chorus, and me asking for the rest. |
| [3-full-direction.md](3-full-direction.md) | The full direction both sessions got: my message, plus the rest of the film and lyric direction for every line, written by another Claude session once I got too tired to keep going. It's the exact same file in both runs, byte for byte. |

## The fine print

This isn't a scientific test by any means. I was literally just working the way I normally would on the story side,
to see what a one-shot of this pipeline would make. Then GPT-6.2 Astra came out and I was like, let's make it a test!

So Codex started from exactly where Claude was when I sent the full direction: the same session, message for message.
That covers the story prompt, writing the lyrics, the Suno takes and my pick. The only changes were file paths and a
short note at the top explaining the setup. Codex also got the song files Claude downloaded a few minutes after the direction, so it didn't have to download them again.

From there, neither one got any more direction on the video. Both had 16 hours, not counting the final 4K render. A
couple of things weren't identical:

- About two hours after I sent the full direction, I cut Claude off from subagents and gave it one extra session
  instead, since the subagents were eating my usage like they always do. That's not direction on the video, but it did change how Claude worked. Codex
  kept its subagents the whole time.
- Codex got my two later messages (the 16-hour limit, and a note about sharing the GPU queue and a grace period) right
  at the start. Claude got them 20–45 minutes in.
- Both shared my GPU queue with my other projects, but Codex's renders waited about half as long (median 6.6 minutes
  against Claude's 12.9), and for its last few hours I moved it to the front of the queue.

The models were Claude Fable 5.2 (xhigh) in Claude Code, and Codex CLI on GPT-6.2 Astra (xhigh).
