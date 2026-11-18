# Stage 7: Edit and finish

By now every shot is built and the full film is current. This stage looks at the film as a whole, finishes it, and
reports. Read `craft/editing.md`.

## 1. The whole film

Watch the current full film at speed, then step through every seam between shots. Give the critic its strips with the
treatment and the brief. Look for:

- the arc: does the film build, does the turning point land, is the last section the biggest or the most changed;
- pacing: stretches that drag or rush against the music, sections that feel alike;
- seams: a jump in light, colour or motion between shots that wasn't meant;
- consistency: the look holding across the film, with its planned shifts;
- the opening and the ending: the first seconds should pull someone in; the last should feel like an end.

Fix what you find in the shots themselves and re-render them.

## 2. The ending

The film ends with the song: on its last note, or on a final image held through the song's tail. If the person asked for
an end card, make it part of the world rather than a separate slide, unless the treatment says otherwise.

## 3. The final render and the file

```sh
python3 tools/edit.py final <film>
```

When the final render sits outside the time limit (`run.json` `"finalRenderAfterLimit"`), this section is what runs
after the deadline: render every shot with `--preset final` (at `"deliverySize"` when set), splice each with `--kind
final`, then run the command above. The shots' content doesn't change here.

It joins the final shot renders in order, checks every frame is present (the count equals the song's length × fps), and
muxes the picture with the mastered WAV, encoded once (H.264, BT.709 tagged, AAC from the WAV, or what the brief asked
for). Then check the file itself: its length against the song's, the first word against its frame, `tools/checks.py` over
the whole film, and a full watch at speed.

## 4. The report

`films/<slug>/report.md`:

- the film file and its length, the song, the lyric;
- what was decided at each stage and why, in a few lines each, and what the person's notes changed;
- what was spent: Suno Creates and downloads, time per stage, and tokens and API-equivalent cost
  (`python3 tools/usage.py <film> --out films/<slug>/usage.md`);
- credits: the song's service, every asset with its source and license;
- what you would do next with more time, honestly.

## 5. Show it

The last WIP entry: the finished film, the report, and the credits. Tell the person in chat where the film is (its full
path) and that it's finished.
