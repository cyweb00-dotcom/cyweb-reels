# Composite the screen film onto the user's desk photo (desk/plate_user.png).
#   film (central 2:1 band, teal glow shifted to CYWEB blue) -> getPerspectiveTransform + warpPerspective
#   onto the measured screen corners, clipped to the screen; glass sheen; screen light blooming onto the
#   bezel, wall and desk in the screen's own colour; light grain; animated labels + captions on top.
import cv2, numpy as np, json, sys, os
sys.path.insert(0, 'tools')
import composite_room as CR                       # reuse labels + captions animation (overlays)
cfg = json.load(open('desk/corners_user.json')); C = np.float32(cfg['corners'])
plate = cv2.imread(cfg['plate']).astype(np.float32); H, W = plate.shape[:2]
BAND = (60, 1020)                                  # film rows used: 1920x960 = 2:1, like this monitor
SRC = np.float32([[0, 0], [1920, 0], [1920, BAND[1] - BAND[0]], [0, BAND[1] - BAND[0]]])
M = cv2.getPerspectiveTransform(SRC, C)
ss = 4; big = cv2.warpPerspective(np.full((BAND[1] - BAND[0], 1920), 255, np.uint8), cv2.getPerspectiveTransform(SRC, C * ss), (W * ss, H * ss), flags=cv2.INTER_NEAREST)
mask = cv2.resize(big.astype(np.float32) / 255, (W, H), interpolation=cv2.INTER_AREA)[..., None]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
u = (xx - C[0, 0]) / (C[1, 0] - C[0, 0]); v = (yy - C[0, 1]) / (C[3, 1] - C[0, 1])
sheen = (0.045 * np.clip(1 - np.abs((u * .8 + v * .6) - .3) / .16, 0, 1) + .02 * np.clip(1 - v, 0, 1))[..., None] * 255
below = np.clip((yy - C[3, 1]) / 500, 0, 1)[..., None]           # desk area under the screen gets more spill
def to_blue(img):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
  h, s = hsv[..., 0], hsv[..., 1] / 255
  w = np.clip(1 - np.abs(h - 88) / 14, 0, 1) * np.clip(s * 2, 0, 1)   # teal band (OpenCV hue ~88)
  hsv[..., 0] = h + 20 * w                                            # -> CYWEB blue (~108)
  return cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
def frame(k):
  f = cv2.imread(f'film/out/{k:04d}.png')[BAND[0]:BAND[1]]
  f = to_blue(f).astype(np.float32) * 0.95 + np.array([10, 6, 4], np.float32)   # panel black level (blue-ish)
  scr = cv2.warpPerspective(f, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
  scr = cv2.GaussianBlur(scr, (0, 0), .6)
  out = plate * (1 - mask) + mask * np.clip(scr + sheen, 0, 255)
  # screen light: bloom over the bezel + soft spill on wall and desk, in the screen's colour
  lit = scr * mask
  def soft(img, sigma, d):   # wide blurs at reduced resolution (same look, far faster)
    sm = cv2.resize(img, (W // d, H // d), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), sigma / d), (W, H), interpolation=cv2.INTER_LINEAR)
  glow = soft(lit, 18, 2) * .22 + soft(lit, 70, 4) * .20 + soft(lit, 220, 8) * (.10 + .25 * below)
  out = 255 - (255 - out) * (1 - np.clip(glow / 255, 0, 1) * (1 - mask * .85))   # screen-blend
  g = np.random.default_rng(k).normal(0, 1, (H, W)).astype(np.float32); g = cv2.GaussianBlur(g, (0, 0), .6) * 1.8
  out = out + g[..., None]
  out = CR.overlays(k, out)
  return np.clip(out + .5, 0, 255).astype(np.uint8)
if __name__ == '__main__':
  os.makedirs('out/desk', exist_ok=True)
  for k in range(int(sys.argv[1]), int(sys.argv[2]) + 1): cv2.imwrite(f'out/desk/{k:04d}.png', frame(k))
