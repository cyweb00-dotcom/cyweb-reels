# DIFF.md — mine vs reference, worst first

Measured on the flat screen film (reference unwarped vs mine through the measured screen transfer), 160x90 downsample.
`mean abs diff` is in 8-bit levels per channel; `glow err` is the distance between teal-glow centroids in flat px.
Numbers: `out/diff_metrics.json`. Visual: `out/side_by_side_screen.mp4`, `out/side_by_side.mp4`, `out/stills/_sheet_ref_vs_mine.png`.

## Final state (round 2: "as close to the reference as possible")
`screen` = flat screen film vs the unwarped reference; `frame` = the whole 1080x1920 frame vs the reference (both mean abs diff, 8-bit levels).

| # | Beat | screen | frame | What's still different | Cause |
|---|---|---|---|---|---|
| 1 | Phone tunnel f158–206 | 38.4 (was 52.7) | 28.4 | Screen content is mine (CYWEB site stand-ins, not the reference's iOS apps); side phones ~10% narrower. | Your 4 screenshots aren't in assets/ yet. Geometry matches (inner edges within 13 px). |
| 2 | Whip f207–240 | 24.6 (was 29.0) | 24.6 | Phone path within ~10° / ~60 px between the 8 measured keys. | Interpolated between measured frames. |
| 3 | Push-in f68–88 | 16.7 | 25.5 | Reference beam behind the words is brighter at f73–75. | Beam comes only from the glow fit. |
| 4 | Panel f89–124 | 18.8 | 22.1 | Avatar/chip artwork is mine. | Nothing copied. Quad within 2 px. |
| 5 | Bar f241–288 | 16.1 | 22.1 | Contour band slightly wider. | My own vector arcs. Count, tip and ghosting match per frame. |
| 6 | Logo / end f329–357 | 12–15 | 25–27 | CY mark vs apple. | Brand. |
| 7 | Title, icon, invite, closing | 6–14 | 20–21 | Different words ("CYWEB Websites", "Watch It Grow", "Your Business Online"). | Copy. "Just Ask" now identical. |
| — | Desk (all frames) | — | ~20 baseline | Rebuilt room: no keycap legends, no "BenQ" chin logo, simplified ceiling. | 3D rebuild, not a copy of the reference footage. |

## Rounds (what was worst each time, and the fix)
1. **Glow** (all beats): one soft Gaussian, far too weak, wrong shape → replaced with a 3-Gaussian fit per reference frame and the measured G→R,B colour ramp through the inverse screen transfer. Biggest single improvement.
2. **Title line 25 px low; name gradient too dark; no word space** → y track moved up 25 flat px, lighter gradient, 22 px slot.
3. **Push-in wrong**: mine zoomed into the icon and blurred out; the reference icon *flies into the panel's logo tile* and the cursor rides with it → rebuilt as a flying icon handed off to the panel tile; panel drop and scale re-keyed (f74–95).
4. **Whip direction**: mine swung the wrong way and was 2x too small → re-keyed around the phone's top-edge centre from 8 measured frames (tips up toward the lens, turns ~85° clockwise, sweeps left).
5. **Motion blur on the count**: 5 sub-frames stacked 5 ghost numbers; the reference blends exactly 2 frames (n−1 over n) → 2 sub-frames at offsets −1/0 in f244–288; 12 sub-frames for the whip.
6. **Sound**: the icon pop (f34.5) was buried in the bed → pops +4 dB; all 19 cues now detected within 0.5 frame of their reference hit.

### Round 2
7. **Desk**: the flat stand-in plate was the biggest whole-frame difference → rebuilt the reference room in 3D (three.js): camera + monitor pose solved from the 4 corners (focal 1580 px, 0.6 px error), lamp (r 7.7 cm) and keyboard placed by casting rays from their reference pixel positions, then LAB colour transfer to the reference in 4 horizontal bands.
8. **Labels**: accent changed to the reference orange (#D57C58); boxes, font, sizes unchanged (already measured 1:1).
9. **Invite line**: "Just Ask", as in your brief and the reference.
10. **Phone screens** were brighter than the reference camera captured them (measured phone white ≈ 176,189,191) → white iOS-style screens at 76% brightness: tunnel diff 55.7 → 38.4, whip 30.8 → 24.6.
11. Tried a lighter frosted panel glass: diff got worse (18.8 → 21.4), reverted.

### Round 3: own camera angle, more realism
The reference room was only a match target; this round the shot moves to its own angle (front-right, higher, monitor turned the other way), so whole-frame numbers against the reference no longer apply. The screen film is unchanged (same beat-by-beat match as round 2).
12. **Light**: the room is relit every frame by the screen itself (6 screen-cell light passes, linear light), so teal scenes wash the desk and keyboard teal and the white phone tunnel lights them white.
13. **Glass**: the screen keeps the room's reflection from the base pass on top of the picture; slight off-axis contrast loss.
14. **Lens**: bloom on the lamp, light strip and bright screen, depth of field from the depth pass (keyboard and mouse slightly soft, screen sharp), ACES tone mapping, vignette, chromatic aberration, grain.
15. **Labels**: same boxes; 85.6 px clear of the light bar (projected from 3D), 144 px clear of the screen.
