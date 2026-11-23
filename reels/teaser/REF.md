# REF.md — the reference screen film, beat by beat (measured)

All numbers come from the unwarped screen (`ref/flat/`, 1280x720, one image per frame) unless marked "film px" (= flat x1.5, my 1920x1080 render).
Frames are 1-based at 30 fps (frame n = (n−1)/30 s). The reference has 357 frames (11.9 s); mine has 360 (12.0 s, last 3 hold the end card).
Raw per-frame data: `data/ref_per_frame.json` (glow moments, white-object boxes, mean level), `data/ref_text_boxes.json` (text boxes), `data/ref_glow_fit.json` (3-Gaussian glow fit).

## Beat map
| Beat | Frames | What happens |
|---|---|---|
| Title | 1–32 | "With" on screen at f1, flash f4–9 (screen floods teal), full line sharp by f11, slow push-in |
| Icon | 33–67 | words slide apart (f32–43), glass icon lands between (f33–41), cursor glides in (f41–59) |
| Push-in | 67–89 | words drop and blur away (f70–78), icon grows and rises (f72–77) then settles into the panel's logo tile (f77–89) |
| Glass panel | 74–124 | panel drops in from the top tilted back (f74–95), holds, cursor clicks the logo f107, panel lifts away f119–124 |
| Invite | 125–157 | "Just" f125, "Ask" f128, line rises into place by f137, flash f139–144, holds and recedes |
| Phone tunnel | 155–209 | phones fly in (bottom f155, left/right f157, top f159), tunnel drifts, phones fly out f202–210 |
| Line change | 177–203 | invite blurs out f177–182, payoff blurs in word by word f181–190, holds, fades f200–203 |
| Whip | 207–243 | the floor phone tips up into the lens and turns ~85° clockwise while sweeping left, heavy motion blur |
| Loading bar | 238–288 | glass capsule from the left edge, percent counts 7 → 100, contour lines sweep up from f254 |
| Closing line | 289–328 | "Pro" f291, "Workflow" f297, "Unleashed" f309; line drifts left to centre |
| Logo | 329–348 | logo slides in from the right (f329–343), teal V-beam bloom from the top f337–347 |
| End | 348–357 | screen flashes to white, small dark logo centred |

## Glow (the one teal light)
Fitted per frame as 3 elliptical Gaussians on the captured green excess over black (`tools/glowfit.py`, objects masked). Mean fit error 10.6 green levels. Values below in film px: centre (x,y), σx×σy, amplitude (green levels above black).
Captured colour ramp (G → R,B): G100 → (1,113) teal · G150 → (66,150) · G190 → (128,204) · G210 → (140,227) pale cyan-white.

| Frame | Gaussians (strongest first) |
|---|---|
| 1 | (940,958) σ337×239 A154 · (945,555) σ177×86 A52 · (939,1023) σ119×60 A20 |
| 7 | (933,983) σ369×286 A181 · (932,399) σ400×252 A170 · (932,50) σ376×157 A110 |
| 13 | (926,992) σ437×176 A200 · (-585,494) σ2400×235 A101 · (2535,50) σ2400×209 A80 |
| 25 | (407,957) σ1607×156 A139 · (917,680) σ611×120 A59 · (1526,97) σ213×129 A6 |
| 45 | (668,778) σ339×122 A81 · (698,542) σ209×60 A66 · (1369,730) σ258×162 A60 |
| 60 | (944,714) σ172×151 A64 · (427,-585) σ697×368 A35 · (1695,449) σ283×449 A16 |
| 75 | (938,38) σ468×231 A198 · (961,580) σ323×216 A126 · (960,1026) σ286×141 A88 |
| 85 | (-118,-12) σ523×298 A201 · (911,1337) σ456×431 A193 · (1959,-102) σ615×333 A172 |
| 105 | (996,515) σ80×60 A123 · (-249,741) σ2400×114 A103 · (-90,984) σ2400×123 A100 |
| 121 | (1019,497) σ60×60 A129 · (926,729) σ388×110 A106 · (952,984) σ273×105 A98 |
| 130 | (946,936) σ301×193 A138 · (939,638) σ187×60 A83 · (1805,353) σ166×163 A8 |
| 141 | (932,997) σ361×288 A173 · (942,387) σ364×283 A170 · (947,46) σ326×139 A81 |
| 150 | (909,1024) σ492×274 A189 · (101,160) σ236×358 A136 · (1784,164) σ234×351 A105 |
| 170 | (153,396) σ202×277 A221 · (993,144) σ242×60 A177 · (1316,917) σ1356×221 A134 |
| 195 | (852,58) σ185×60 A96 · (952,747) σ156×65 A37 · (990,559) σ110×60 A35 |
| 211 | (926,80) σ537×162 A150 · (940,397) σ379×144 A113 · (967,696) σ290×142 A84 |
| 225 | (1035,1010) σ749×172 A110 · (1819,-195) σ173×221 A77 · (976,717) σ331×94 A58 |
| 245 | (106,1695) σ148×392 A95 · (350,944) σ2400×142 A83 · (927,707) σ1183×107 A66 |
| 265 | (904,1009) σ286×103 A197 · (900,792) σ228×96 A172 · (1311,733) σ215×169 A73 |
| 280 | (777,939) σ336×199 A267 · (422,223) σ330×270 A165 · (1440,419) σ304×502 A152 |
| 295 | (356,997) σ370×151 A158 · (1497,989) σ351×148 A123 · (871,720) σ711×114 A73 |
| 320 | (1049,740) σ247×125 A68 · (675,723) σ153×123 A42 · (1733,387) σ293×474 A13 |
| 335 | (952,834) σ147×170 A94 · (-585,-585) σ1146×576 A35 · (1724,486) σ281×598 A24 |
| 345 | (946,-23) σ489×344 A169 · (956,889) σ294×609 A100 · (1835,868) σ134×313 A17 |

## Title (f1–32)
- Left edge of "With" (flat px): f1 575 · f9 467 · f11 458 · f15 441 · f19 431 · f25 423 · f29 414 · f31 409 · f32 394.
- Scale (vs f25, line width 498): f11 0.862 · f15 0.929 · f19 0.968 · f25 1.0 · f29 1.035 · f31 1.055. Ease: fast-out then near-linear creep, speeds up again from f28.
- Cap height 38–39 px at f25 (Inter 78 px in film px). Cap centre y ≈ 356. Line centre x ≈ 677 (not centred: 37 px right).
- Blur-in: "With" ≈ 0.6 px at f1, rises to ~16 px at the flash peak f7, back to 0 by f13. Product name absent until f7, ~18 → 0 px blur over f7–13 (expo out).
- Product name gradient: pale teal-white on the left → deeper teal on the right; deepens by f60.

## Icon + cursor (f32–67)
- f60: "With" 272–395, icon 432–530 (98 px square, radius ≈ 18), name from 580. Gaps 26–37 px / 17–50 px.
- "With" cap height 47 px at f60 → line scale 1.2 vs f25. Group drifts left 288 → 271 (f45 → f67).
- Icon: scale-in with slight overshoot f33–41, blur ~10 → 0 px by f39.
- Cursor: hollow rounded triangle, ≈45 px. Visible from f41 at ≈(800,395), glides to the icon's lower right (541,392) by f59, ease-out.

## Push-in → panel (f67–95)
- "With" drops from y 352 to ≈419 by f75 while the icon rises: icon centre (481,341) 98 px → (533,293) ≈160 px at f77 → (613,373) at f85–89 → (635,382) panel tile at f105.
- Cursor rides with the icon, offset ≈(+50…+75, +55…+70).
- Panel bottom edge: f77 ≈150 · f79 ≈317 · f85 ≈475 · f89+ 527.

## Glass panel (f89–124)
- Measured quad at f105: TL(240,122) TR(1035,120) BR(1125,525) BL(152,527).
- Fitted CSS 3D (perspective 1920 film px, origin centre): centre (957.9, 454.7) film px, 1312.6 × 729.4, **rotateX 32.0°**, **rotateY 0.24°**. Corner error ≤ 2 px.
- Contents (flat, f105): logo tile 535–735 × 310–455; avatar circle r≈90 at (650,240) with a purple ring; small icon r≈32 at (478,208); tiny avatar r≈25 at (750,158); chip row y≈430 at x 340/460/818/938 with labels; "SUGGESTIONS" (328,402), "SHOW MORE" (955,402); bottom row y≈495 (search pill, two pills, home bar 500–780).
- Cursor tip ≈(705,435) f97–121; click f105–111 (press f105–107, release by f111); audio click at f107.5.
- Exit f119–124: lifts ≈95 px, tilts further, fades and blurs.

## Invite (f125–157)
- Bbox centre y: f126 447.5 · f128 429.5 · f130 415 · f132 405 · f134 394.5 · f136 387 · f137 384.5 (ease-out rise), f145 367, f150 362.5.
- Width (scale vs f150 = 212 px): f129 0.976 · f133 1.014 · f150 1.0 · f155 0.925 · f157 0.863; ≈0.6 inside the tunnel.
- Cap height 45 px (Inter 93 film px). Left-anchored: first word appears in its final place, second word appended.
- Blur: first word ~14 → 0 px over f125–131, second f128–133; flash f139–144 re-blurs (peak ≈16 px).

## Phone tunnel (f155–209)
- Inner edges at f195 (flat): left 340, right 945, top 165, bottom 530; inner edge lengths: left 350, right 395, top 430, bottom 365.
- Built as a true box tunnel: perspective 1100 film px, walls at x ±908, y ±546, far edge at z −1100 → measured in Chrome at f195: 327 / 958 / 160 / 534.
- Each phone's top (island) faces the vanishing point; long axis runs along the tunnel.
- Entry: expo-out from outside the frame, 9 frames, staggered bottom f155 / sides f157 / top f159. Drift: roll −4° → +3°, push +160 px over f161–205. Exit f202–210 ease-in outward.

## Line change (f177–203)
- Payoff final box f195: 519–760 × 347–377 → centre (639.5, 361), cap 28 px (Inter 58–60 film px).
- Appears f184 (541–658) and grows to full by f189 (526–768): scale ≈0.9 → 1.0 expo-out, words staggered 1 frame, blur ≈14 → 0 px.

## Whip (f207–243)
Island (top-edge centre) path, film px / rotation / tilt / scale: f209 (960,810) 0° 70° 0.5 · f213 (975,640) 14° 40° 0.7 · f215 (971,620) 40° 25° 1.0 · f217 (960,660) 55° 15° 1.3 · f221 (906,745) 70° 5° 1.7 · f229 (904,800) 72° 0° 1.9 · f237 (720,561) 80° · f240 (540,580) 83° · gone by f243.
Motion blur in the reference is roughly a full-frame exposure.

## Loading bar (f238–288)
- Capsule: y 228–497 (height 269, radius 134.5), left end off-screen, tip x = **338 + 7.38 × percent** (flat px), checked against every frame f241–277 (within ±4 px).
- Percent shown per frame: 241: 7 · 242: 10 · 243: 13 · 244: 18 · 245: 24 · 246: 33 · 247: 43 · 248: 51 · 249: 58 · 250: 64 · 251: 69 · 252: 72 · 253: 76 · 254: 78 · 255: 81 · 256: 83 · 257: 85 · 258: 87 · 259: 88 · 260: 90 · 261: 91 · 262: 92 · 263: 93 · 264: 94 · 265: 95 · 266: 95 · 267: 96 · 268: 97 · 269: 97 · 270: 98 · 271: 98 · 272: 98 · 273–276: 99 · 277–288: 100.
- Ghosted digits on many frames = a 2-frame blend (frame n−1 over frame n).
- Digits: cap height 73 px, right edge ≈100 px left of the tip, light grotesk, white.
- Tip retreats 36 px over f280–288.
- Contour lines: appear f254 bottom-right, sweep up by f265; bright teal band (captured ≈ rgb 26,217,199) with dark lines, arcs rising to the right; a pale glow floods from the bottom-left f271–283.

## Closing line (f289–328)
- Left edge per frame: f296 570 · f298 558 · f301 545 · f305 530 · f309 499 · f310 483 · f313 453 · f317 436 · f321 429 · f325 417 · f326 410.
- Full-line width 449 at f310, cap ≈ 30 px, y centre 361.5. Words appear in place and the line slides left to centre (ease-out after each new word).
- Glow: wide bottom band at f289 shrinking to a centred oval (σ ≈ 200 × 150 flat) by f319.

## Logo + end (f329–357)
- Logo centre x: f329 722 · f330 702 · f331 689 · f333 672 · f335 660 · f337 653 · f339 647 · f341 643 · f343 640 (ease-out), y 362; size 83 × 101 px.
- V-beam bloom f337–347 from the top centre down to the logo; white flash f348; end f349–357: white screen (captured ≈ rgb 208,219,205), dark logo 58 × 72 px centred (637,361).

## Sound (reference waveform)
Spectral-flux onsets (frame = t·30+1). Music bed ≈ 92 bpm (184 bpm autocorrelation peak, half-time).
Main hits used: 4.0 title flash · 34.5 icon lands · 72.5 push-in · 107.5 cursor click · 121.5 panel out · 125.5 / 128.5 invite words · 138 invite flash · 158 tunnel in · 181 line swap · 185.5 payoff · 211.5 whip · 241–277 rise under the count · 277 100% · 289 cut to the closing line (strongest onset) · 294.5 / 310.5 closing words · 329 logo · 345.5 bloom hit.
