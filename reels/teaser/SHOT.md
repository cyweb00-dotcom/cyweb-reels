# SHOT.md — reference desk shot, measured

Source: `ref/reference.mp4` (720x1280, 30 fps, 357 frames, 11.91 s, AAC audio).
All numbers come from `tools/stdmap.py`, `tools/corners.py` and the label scripts. Reference px first, then output px (x1.5 → 1080x1920).

## Camera
- Locked off. Phase correlation of the wall band (y 20–160) on every 10th frame: max drift **0.32 px**. Treated as static.

## Monitor screen (active area)
Found from the temporal std-dev map (pixels that change = screen), edges fitted with Huber lines, corners from line intersections.

| Corner | Reference (720x1280) | Output (1080x1920) |
|---|---|---|
| TL | 35.8, 370.9 | 53.7, 556.4 |
| TR | 703.6, 433.2 | 1055.4, 649.8 |
| BR | 696.3, 792.4 | 1044.5, 1188.6 |
| BL | 33.0, 829.3 | 49.5, 1244.0 |

- Left edge 458.4 px tall, right edge 359.2 px: the monitor is turned away on the right (right side farther).
- Flat study size: 1280x720 (`ref/flat/`). Screen film render size: 1920x1080.
- Screen as captured by the camera: black level ≈ rgb(13,18,20), full white ≈ rgb(200,207,195), teal glow peak ≈ rgb(0,112,118), bright contour teal ≈ rgb(26,217,199).

## Label boxes (static, whole reel)
| | Reference box (x0–x1, y0–y1) | Size | Output box | Output size |
|---|---|---|---|---|
| Label 1 | 196–524, 175–240 | 329 x 66 | 294–786, 262.5–361.5 | 492 x 99 |
| Label 2 | 124–596, 251–302 | 472 x 52 | 186–894, 376.5–454.5 | 708 x 78 |

- Both centred on x = 360 (output 540). Gap between boxes 10 px (15 out). Box 2 bottom to light bar ≈ 35 px.
- Corner radius ≈ 7 px (≈ 10.5 out). Fill: opaque near-black rgb(1,1,1), no border, no shadow.
- Cap height: label 1 = 29 px (43.5 out), label 2 = 23 px (34.5 out). Text width: label 1 = 243 px, label 2 = 403 px.
- Text colours: white rgb(250,250,251); accent word rgb(213,124,88) #D57C58 (reference orange). Mine uses CYWEB blue as the accent.
- Spark icon: 12-ray starburst in the accent colour, ≈ 43 px across in label 1 (x 210–252), ≈ 34 px in label 2 (x 136–169), left of the text with a ≈ 12 px gap.

## Label font match
Rendered each candidate at the reference cap height and scored glyph overlap (IoU) against the reference text masks (`tools/fontmatch.js`):

| Font | Label 1 IoU | Label 2 IoU |
|---|---|---|
| **Barlow Condensed 700** | **0.852** | **0.894** |
| Barlow Condensed 800 | 0.810 | 0.779 |
| Barlow Condensed 600 | 0.776 | 0.836 |
| Oswald 600 | 0.744 | 0.593 |
| Bebas Neue | 0.767 | 0.434 |
| Fjalla One | 0.632 | 0.370 |

→ **Barlow Condensed Bold (700)**, all caps.

Screen-film type: the reference uses a SF-Pro-style grotesk (semibold "With", regular lines, light digits). Matched with **Inter** (600 / 400 / 300).

## Set colours (reference, for the stand-in plate)
Wall between slats ≈ rgb(54,45,26), bezel ≈ rgb(8,9,12), desk ≈ rgb(20,7,1).
