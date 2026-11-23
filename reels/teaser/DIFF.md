# DIFF.md — mine vs reference, worst first

Measured on the flat screen film (reference unwarped vs mine through the measured screen transfer), 160x90 downsample.
`mean abs diff` is in 8-bit levels per channel; `glow err` is the distance between teal-glow centroids in flat px.
Numbers: `out/diff_metrics.json`. Visual: `out/side_by_side_screen.mp4`, `out/side_by_side.mp4`, `out/stills/_sheet_ref_vs_mine.png`.

## Final state (after 6 compare/fix rounds)
| # | Beat | mean abs diff | glow err | What's still different | Cause |
|---|---|---|---|---|---|
| 1 | Phone tunnel f158–206 | 52.7 | 101 | Phone screens: reference = big white iOS screens; mine = website stand-ins with colour cards. Side phones ~10% narrower than the reference. | Screen content (your 4 screenshots aren't in assets/ yet). Geometry matches: inner edges 327/958/160/534 vs ref 340/945/165/530. |
| 2 | Whip f207–240 | 29.0 | 59 | Phone path and angle within ~10°/~60 px; the reference phone is a little closer to the lens around f215–221; content differs (calendar stand-in). | Keyframed from 8 measured island positions; in-between frames interpolated. |
| 3 | Panel f89–124 | 18.8 | 21 | Glass fill is a bit darker than the reference's frosted card; avatar/chip art is mine (no copied artwork). | Deliberate: everything rebuilt. Quad matches within 2 px. |
| 4 | Push-in f68–88 | 16.7 | 30 | Reference shows the panel's top rim earlier (f73–75) and a brighter beam behind the words. | Panel entry keyed at f74; beam comes only from the glow fit. |
| 5 | Loading bar f241–288 | 16.1 | 21 | Contour band slightly wider/higher than the reference; digits a touch heavier. | Contours are my own vector arcs. Percent per frame, tip position and the 2-frame ghosting match. |
| 6 | End f349–357 | 15.4 | n/a | White level matches; my logo is the full-colour CYWEB mark (reference: dark mark). | Brand. |
| 7 | Title f1–32 | 13.9 | 26 | My product line is longer than "Apple Intelligence", so the right end extends ~40 px further. | Different words; "With" left edge and scale track are 1:1. |
| 8 | Logo f329–348 | 12.2 | 117* | Mark shape differs (CY vs apple). *Centroid error is skewed by the white logo inside the teal mask. | Brand. |
| 9 | Invite f125–157 | 10.3 | 24 | "Message Us" vs "Just Ask": first word longer, so the left-anchored reveal starts further left. | Different words. |
| 10 | Icon f33–67 | 8.0 | 19 | Icon glyph: my CY mark vs the reference glyph. | Brand. |
| 11 | Closing f289–328 | 6.2 | 28 | Weight 500 vs reference ≈ 450. | Font (Inter vs SF). |

## Rounds (what was worst each time, and the fix)
1. **Glow** (all beats): one soft Gaussian, far too weak, wrong shape → replaced with a 3-Gaussian fit per reference frame and the measured G→R,B colour ramp through the inverse screen transfer. Biggest single improvement.
2. **Title line 25 px low; name gradient too dark; no word space** → y track moved up 25 flat px, lighter gradient, 22 px slot.
3. **Push-in wrong**: mine zoomed into the icon and blurred out; the reference icon *flies into the panel's logo tile* and the cursor rides with it → rebuilt as a flying icon handed off to the panel tile; panel drop and scale re-keyed (f74–95).
4. **Whip direction**: mine swung the wrong way and was 2x too small → re-keyed around the phone's top-edge centre from 8 measured frames (tips up toward the lens, turns ~85° clockwise, sweeps left).
5. **Motion blur on the count**: 5 sub-frames stacked 5 ghost numbers; the reference blends exactly 2 frames (n−1 over n) → 2 sub-frames at offsets −1/0 in f244–288; 12 sub-frames for the whip.
6. **Sound**: the icon pop (f34.5) was buried in the bed → pops +4 dB; all 19 cues now detected within 0.5 frame of their reference hit.
