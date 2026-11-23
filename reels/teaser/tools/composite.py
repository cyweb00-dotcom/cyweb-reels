# Pin the screen film onto the desk plate.
#   film/out/NNNN.png (1920x1080, display RGB)  ->  out/desk/NNNN.png (1080x1920)
# getPerspectiveTransform + warpPerspective onto the 4 screen corners, clipped to the screen,
# bezel and anything in front stay on top; faint glass reflection; light spill in the screen's colour.
import cv2, numpy as np, json, sys, os
sys.path.insert(0, 'tools'); from screen_xfer import xfer
cfg = json.load(open('desk/corners.json'))
C = np.float32(cfg['corners'])                                  # TL TR BR BL, output px
plate = cv2.imread(cfg['plate']).astype(np.float32)
lab = cv2.imread('desk/labels.png', cv2.IMREAD_UNCHANGED).astype(np.float32)
la = lab[..., 3:4] / 255.0; lrgb = lab[..., :3]
H, W = plate.shape[:2]
M = cv2.getPerspectiveTransform(np.float32([[0, 0], [1920, 0], [1920, 1080], [0, 1080]]), C)
# anti-aliased screen mask: warp a full-white rect (4x supersampled edges)
ss = 4; Ms = cv2.getPerspectiveTransform(np.float32([[0, 0], [1920, 0], [1920, 1080], [0, 1080]]), C * ss)
big = cv2.warpPerspective(np.full((1080, 1920), 255, np.uint8), Ms, (W * ss, H * ss), flags=cv2.INTER_NEAREST)
mask = cv2.resize(big.astype(np.float32) / 255.0, (W, H), interpolation=cv2.INTER_AREA)[..., None]
# fill the plate's screen hole with the screen-off colour so no key colour can survive
plate = plate * (1 - mask) + mask * np.array([20, 18, 13], np.float32)
# glass reflection (static: the camera never moves)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
u = (xx - C[0, 0]) / (C[1, 0] - C[0, 0]); v = (yy - 556) / (1244 - 556)
refl = (0.035 * np.clip(1 - np.abs((u * 0.8 + v * 0.6) - 0.35) / 0.18, 0, 1) + 0.025 * np.clip(1 - v, 0, 1) * np.clip(1 - u, 0, 1))[..., None] * 255
# spill falloff around the screen (wall above/sides, stronger on the desk below)
dist = cv2.distanceTransform((mask[..., 0] < 0.5).astype(np.uint8), cv2.DIST_L2, 5)
spill = np.exp(-dist / 170.0) * (1 - mask[..., 0]); spill[yy > 1520] *= 1.6
side = np.clip((xx - 540) / 540, -1, 1)                          # left/right weighting
spill = spill[..., None]
def frame(k):
  f = cv2.imread(f'film/out/{k:04d}.png')
  scr = xfer(f, soft=1.8)                                        # as the camera sees it
  warped = cv2.warpPerspective(scr, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
  # light spill: mean colour of each half of the screen
  sm = cv2.resize(scr, (2, 1), interpolation=cv2.INTER_AREA).reshape(2, 3) - np.array([20, 18, 13])
  sm = np.clip(sm, 0, None)
  col = (sm[0][None, None] * (0.5 - side[..., None] * 0.5) + sm[1][None, None] * (0.5 + side[..., None] * 0.5))
  out = plate + spill * col * 0.30
  out = out * (1 - mask) + mask * np.clip(warped + refl, 0, 255)
  out = out * (1 - la) + lrgb * la                               # labels on top of everything
  out += np.random.default_rng(k).normal(0, 1.6, out.shape)      # camera grain
  return np.clip(out + .5, 0, 255).astype(np.uint8)
if __name__ == '__main__':
  os.makedirs('out/desk', exist_ok=True)
  ks = range(int(sys.argv[1]), int(sys.argv[2]) + 1)
  for k in ks:
    if os.path.exists(f'film/out/{k:04d}.png'): cv2.imwrite(f'out/desk/{k:04d}.png', frame(k))
