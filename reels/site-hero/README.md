# CYWEB website hero video (8 s seamless loop, 1920x1080, no sound)

A black glass monitor with a blue dashboard floats in a dark studio: blue rim light, haze, dust, a slow push-in and orbit, glow, grain.
Built in code (three.js + OpenCV), not generated, so no credits are used. The last frame leads straight into the first, so it loops with no jump.

Files in `out/`: `cyweb-hero.mp4` (1.6 MB), `cyweb-hero.webm` (0.4 MB), `poster.jpg`.

## How to use it on a website (nothing here changes cywebdev.com)
```html
<video autoplay muted loop playsinline preload="metadata" poster="poster.jpg">
  <source src="cyweb-hero.webm" type="video/webm">
  <source src="cyweb-hero.mp4" type="video/mp4">
</video>
```
Put the text and buttons over it with CSS. The video has no text, so it works behind any headline. `muted` and `playsinline` are needed for autoplay on phones.

## Rebuild
`python3 -m http.server 8801 &`, then `node render.js 0 239` (scene), `python3 post.py 0 239` (finish), then ffmpeg (see git history).
