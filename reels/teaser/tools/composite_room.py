# Composite the screen film into the 3D room (own camera angle), physically:
#   frame = base + sum_k screen_cell_k * light_k   (all in linear light; light_k = room lit only by screen cell k)
#   screen = warped film (getPerspectiveTransform + warpPerspective) + glass reflection from the base pass
#   then bloom, depth of field (depth pass, focus on the screen), ACES tone map, phone-camera finish, labels.
import cv2, numpy as np, json, sys, os
R = 'desk/room/'
def lin(p): return (cv2.imread(p).astype(np.float32) / 255.0) ** 2.2
base = lin(R + 'base.png'); lights = [lin(R + f'light{k}.png') for k in range(6)]
depth = cv2.imread(R + 'depth.png', cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0 * 4.0  # metres
C = np.float32(json.load(open(R + 'corners.json')))
H, W = base.shape[:2]
SRC = np.float32([[0, 0], [1920, 0], [1920, 1080], [0, 1080]])
M = cv2.getPerspectiveTransform(SRC, C)
ss = 4; big = cv2.warpPerspective(np.full((1080, 1920), 255, np.uint8), cv2.getPerspectiveTransform(SRC, C * ss), (W * ss, H * ss), flags=cv2.INTER_NEAREST)
mask = cv2.resize(big.astype(np.float32) / 255, (W, H), interpolation=cv2.INTER_AREA)[..., None]
lab = cv2.imread('desk/labels.png', cv2.IMREAD_UNCHANGED).astype(np.float32); la = lab[..., 3:4] / 255; lrgb = lab[..., :3]
# depth of field: focus on the screen centre, thin-lens style CoC in px
df = float(np.median(depth[mask[..., 0] > .9])); coc = np.clip(np.abs(1 / np.maximum(depth, .05) - 1 / df) * 7.5, 0, 9)
coc[mask[..., 0] > .5] = 0; coc = cv2.GaussianBlur(coc, (0, 0), 6)[..., None]
def dof(img):
  b1 = cv2.GaussianBlur(img, (0, 0), 2.5); b2 = cv2.GaussianBlur(img, (0, 0), 6)
  w1 = np.clip(coc / 3, 0, 1); w2 = np.clip((coc - 3) / 6, 0, 1)
  return img * (1 - w1) + (b1 * (1 - w2) + b2 * w2) * w1
def aces(x):
  a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14; return np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0, 1)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vig = (1 - 0.32 * (((xx - W / 2) / (W * .62)) ** 2 + ((yy - H / 2) / (H * .62)) ** 2))[..., None]
S_SCREEN, G_SPILL, R_GLASS, EXPO = 1.3, 0.75, 0.55, 1.55
def frame(k):
  f = cv2.imread(f'film/out/{k:04d}.png')
  fl = (f.astype(np.float32) / 255) ** 2.2                                  # film in linear light
  fl = fl * 0.93 + 0.0035                                                    # off-axis viewing: a little contrast loss
  scr = cv2.warpPerspective(fl, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
  cells = cv2.resize(fl, (3, 2), interpolation=cv2.INTER_AREA)               # 3x2 screen cells -> light colours
  out = base.copy()
  for c in range(6): out += lights[c] * cells[c // 3, c % 3][None, None] * G_SPILL
  out = out * (1 - mask) + mask * (scr * S_SCREEN + base * R_GLASS)          # emissive screen + room reflection in the glass
  # bloom
  hi = np.clip(out - 0.55, 0, None); bl = cv2.GaussianBlur(hi, (0, 0), 6) * .5 + cv2.GaussianBlur(hi, (0, 0), 22) * .35 + cv2.GaussianBlur(hi, (0, 0), 60) * .25
  out = dof(out + bl * 0.35)
  img = aces(out * EXPO) ** (1 / 2.2) * vig
  img = np.clip(img, 0, 1)
  # slight lateral chromatic aberration
  def scale_ch(ch, s): Ms = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s); return cv2.warpAffine(ch, Ms, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
  img[..., 2] = scale_ch(img[..., 2], 1.0008); img[..., 0] = scale_ch(img[..., 0], 0.9992)
  img = img * 255
  rng = np.random.default_rng(k); g = rng.normal(0, 1, (H, W)).astype(np.float32)
  g = cv2.GaussianBlur(g, (0, 0), .6) * (2.2 + 3.0 * (1 - img.mean(2) / 255))
  img += g[..., None]
  img = img * (1 - la) + lrgb * la
  return np.clip(img + .5, 0, 255).astype(np.uint8)
if __name__ == '__main__':
  os.makedirs('out/desk', exist_ok=True)
  for k in range(int(sys.argv[1]), int(sys.argv[2]) + 1): cv2.imwrite(f'out/desk/{k:04d}.png', frame(k))
