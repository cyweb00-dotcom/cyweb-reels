# CYWEB teaser — 12 s, 1080x1920, 30 fps

A keynote-style screen film on a monitor in a desk shot, built in code and rendered frame by frame. Timing, layout, motion and sound hits follow `ref/reference.mp4` (measured, see SHOT.md / REF.md / DIFF.md). Every graphic is rebuilt; nothing is cut out of the reference.

- `out/final.mp4` — the reel (high quality) · `out/final_small.mp4` — light export for posting (~2.7 MB)
- Captions (`desk/captions.json`), hook labels animate in over the first second, sound rebuilt in `tools/audio.py`
- `out/stills/` — one desk still per scene + `_sheet_ref_vs_mine.png`
- `out/qc.json`, `out/qc_text.json`, `out/diff_metrics.json` — checks

## What the screen says about CYWEB
| Beat | Shows |
|---|---|
| Title + icon | "With CYWEB Websites", CY logo on a glass app icon |
| Panel | What CYWEB does: Websites · Photos · Videos · Bookings, plus WhatsApp, Google Maps and "Your business"; cywebdev.com and "Local businesses" along the bottom; cursor clicks the CYWEB logo |
| Phone tunnel | Four sites like the ones CYWEB builds: a café (Book a table, WhatsApp us, Google stars, menu, map), a salon (Book online, free times), a clinic (Call now, Book a visit, services, hours), a booking calendar |
| Line change | "Get Found" → "Get More Bookings" |
| Whip | The booking site ("Book your visit") flies past the lens |
| Bar | Counts to 100% |
| Close | "Your Business Online", then the CYWEB mark; end card: full CYWEB logo with "Websites that help local businesses grow" and cywebdev.com |

## Lines
| Slot | Reference | CYWEB |
|---|---|---|
| Intro (With + 2-word name) | With Apple Intelligence | With CYWEB Websites |
| Invite (2 words) | Just Ask | Get Found |
| Payoff (3 words) | See The Magic | Get More Bookings |
| Closing (2 + 1 words) | Pro Workflow / Unleashed | Your Business / Online |
| Label 1 (hook) | OPUS 5.5 COOKED | CUSTOMERS CAN'T FIND YOU? (accent: reference orange #D57C58) |
| Label 2 | COMMENT "CLAUDE" FOR FULL GUIDE | COMMENT "WEBSITE" TO GET YOURS |

## Stand-ins still in use
- **Desk shot (own angle)**: a 3D room built in code (`desk/room.html`): light-oak slatted wall, wall-mounted 27" monitor with light bar, orange ball lamp, slim aluminium keyboard (low-profile keys with legends), white mouse on an aluminium base, grey felt desk mat, ceramic mug, snake plant in a matte pot, walnut desk; soft daylight from the left plus warm practicals. Camera sits front-right and higher than the reference, the monitor is turned toward it (its right edge is the tall one; in the reference it's the left).
  Rendered as linear light passes: `base` (room lights + glass reflections), `light0..5` (room lit only by one sixth of the screen), `depth`. `tools/composite_room.py` relights the room every frame from the screen's own colours, pins the film with getPerspectiveTransform/warpPerspective, adds the glass reflection, bloom, depth of field (focus on the screen), ACES tone mapping, vignette, slight chromatic aberration and grain, then the labels.
  Your own desk shot can still replace it: `python3 tools/fit_desk.py assets/desk.jpg`, then `tools/composite.py`.
- **Phone screenshots**: 4 website screens built in `film/screens.js`. Drop `assets/screens/1.png … 4.png` (left, top, right, bottom/whip) and re-render.

## Rebuild
```
python3 -m http.server 8765 &            # the 3D room loads three.js over http
node tools/render_room.js                 # base, depth, 6 screen-light passes + corners
npm i                                     # gsap + fonts
python3 tools/glowfit.py                  # glow track from the reference (needs ref/flat)
node tools/render_film.js 0 359 5 | python3 tools/avg.py film/out    # screen film, sub-frame motion blur
python3 tools/audio.py && ffmpeg -i out/audio.wav -af loudnorm=I=-14:TP=-1 out/audio_norm.wav
./tools/finish.sh                         # composite on the desk, encode, side-by-sides, QC
```

## Caption
Customers can't find you? Let's fix that.
CYWEB builds websites for local businesses in Cyprus, with online bookings, WhatsApp, Google Maps, and photos and videos that show you at your best.
Comment "WEBSITE" and we'll show you how yours could look.
cywebdev.com
CYWEB team
