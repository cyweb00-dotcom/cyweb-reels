# CYWEB teaser — 12 s, 1080x1920, 30 fps

A keynote-style screen film on a monitor in a desk shot, built in code and rendered frame by frame. Timing, layout, motion and sound hits follow `ref/reference.mp4` (measured, see SHOT.md / REF.md / DIFF.md). Every graphic is rebuilt; nothing is cut out of the reference.

- `out/final.mp4` — the reel
- `out/stills/` — one desk still per scene + `_sheet_ref_vs_mine.png`
- `out/qc.json`, `out/qc_text.json`, `out/diff_metrics.json` — checks

## Lines
| Slot | Reference | CYWEB |
|---|---|---|
| Intro (With + 2-word name) | With Apple Intelligence | With CYWEB Websites |
| Invite (2 words) | Just Ask | Message Us |
| Payoff (3 words) | See The Magic | Watch It Grow |
| Closing (2 + 1 words) | Pro Workflow / Unleashed | Your Business / Online |
| Label 1 | OPUS 5.5 COOKED | CYWEB BUILT THIS |
| Label 2 | COMMENT "CLAUDE" FOR FULL GUIDE | COMMENT "WEBSITE" TO GET YOURS |

## Stand-ins still in use
- **Desk shot**: `desk/plate.html` (built in code) until your photo/clip is in `assets/`. Then: `python3 tools/fit_desk.py assets/desk.jpg` (or `.mp4`) → check `desk/corners_marked.png` → re-run the composite.
- **Phone screenshots**: 4 website screens built in `film/screens.js`. Drop `assets/screens/1.png … 4.png` (left, top, right, bottom/whip) and re-render.

## Rebuild
```
npm i                                     # gsap + fonts
python3 tools/glowfit.py                  # glow track from the reference (needs ref/flat)
node tools/render_film.js 0 359 5 | python3 tools/avg.py film/out    # screen film, sub-frame motion blur
python3 tools/audio.py && ffmpeg -i out/audio.wav -af loudnorm=I=-14:TP=-1 out/audio_norm.wav
./tools/finish.sh                         # composite on the desk, encode, side-by-sides, QC
```

## Caption
Your business, online. We design and build websites that help local businesses grow.
Comment "WEBSITE" and we'll show you how yours could look.
CYWEB team
