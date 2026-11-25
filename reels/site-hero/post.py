# Cinematic finish: bloom, vignette, grade, grain. Pure function of the frame number so the loop stays seamless.
import cv2, numpy as np, sys, os
a, b = int(sys.argv[1]), int(sys.argv[2]); os.makedirs('out/final', exist_ok=True)
H, W = 1080, 1920
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vig = (1 - .42 * (((xx - W / 2) / (W * .62)) ** 2 + ((yy - H / 2) / (H * .62)) ** 2))[..., None]
for f in range(a, b + 1):
    im = (cv2.imread(f'out/raw/{f:04d}.png').astype(np.float32) / 255.0) ** 2.2
    hi = np.clip(im - .35, 0, None)
    bloom = cv2.GaussianBlur(hi, (0, 0), 10) * .55 + cv2.GaussianBlur(hi, (0, 0), 40) * .6 + cv2.GaussianBlur(hi, (0, 0), 110) * .5
    out = im + bloom
    # lens: soft anamorphic streak (horizontal blur of the brightest parts)
    streak = cv2.GaussianBlur(np.clip(im - .7, 0, None), (0, 0), 1) ; streak = cv2.blur(streak, (301, 1)) * .5
    out += streak * np.array([1.0, .75, .45], np.float32)[::-1] * 0 + streak * .6
    out = np.clip(out, 0, 4) ; out = out / (1 + out * .35)            # soft shoulder
    out = out ** (1 / 2.2) * vig
    out[..., 0] *= 1.04; out[..., 2] *= .98                          # cool, blue-black grade
    out = np.clip(out, 0, 1) * 255
    g = np.random.default_rng(f).normal(0, 1, (H, W)).astype(np.float32); g = cv2.GaussianBlur(g, (0, 0), .55) * 2.4
    out += g[..., None]
    cv2.imwrite(f'out/final/{f:04d}.png', np.clip(out + .5, 0, 255).astype(np.uint8))
