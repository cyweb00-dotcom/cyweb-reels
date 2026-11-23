# Turn the user's desk photo (assets/desk_user.png, 1122x1402) into the 1080x1920 plate:
#  1. paint out the labels baked into the photo (column-wise blend between clean rows above and below;
#     the wall is vertical slats + vertical LED strips, so columns continue naturally) + matching grain
#  2. zoom to full height and crop around the monitor
#  3. map the measured screen corners into the plate
import cv2, numpy as np, json
im = cv2.imread('assets/desk_user.png').astype(np.float32)
H0, W0 = im.shape[:2]
y1, y2, x1, x2 = 126, 346, 172, 1000                      # baked label boxes incl. their glow
top = im[y1 - 4:y1].mean(0); bot = im[y2:y2 + 4].mean(0)
t = ((np.arange(y1, y2) - y1) / (y2 - y1))[:, None, None]
fill = top[None] * (1 - t) + bot[None] * t
rng = np.random.default_rng(1)
fill += rng.normal(0, 1.6, fill.shape) * (fill.mean(2, keepdims=True) / 128 + .3)
mask = np.zeros((H0, W0), np.float32); mask[y1:y2, x1:x2] = 1; mask = cv2.GaussianBlur(mask, (0, 0), 3)[..., None]
full = im.copy(); full[y1:y2, x1:x2] = fill[:, x1:x2]
im = im * (1 - mask) + full * mask
# corners measured on the photo (screen glass, original px)
C0 = np.float32([[205, 475], [927, 471], [929, 846], [205, 835]])
s = 1920 / H0; cx = (175.3 + 963.9) / 2 * s; x0 = cx - 540
big = cv2.resize(np.clip(im, 0, 255).astype(np.uint8), (round(W0 * s), 1920), interpolation=cv2.INTER_LANCZOS4)
plate = big[:, int(round(x0)):int(round(x0)) + 1080]
C = C0 * s - np.float32([round(x0), 0])
cv2.imwrite('desk/plate_user.png', plate)
json.dump({'plate': 'desk/plate_user.png', 'corners': C.round(1).tolist(), 'source': 'assets/desk_user.png',
           'source_corners': C0.tolist(), 'scale': s, 'crop_x0': round(x0)}, open('desk/corners_user.json', 'w'), indent=1)
m = plate.copy(); cv2.polylines(m, [C.astype(np.int32)], True, (0, 255, 255), 3)
for n, p in zip(('TL', 'TR', 'BR', 'BL'), C): cv2.circle(m, tuple(int(v) for v in p), 12, (0, 0, 255), 3); cv2.putText(m, f'{n} {p[0]:.0f},{p[1]:.0f}', (int(p[0]) + 8, int(p[1]) - 14), 0, .9, (0, 255, 255), 2)
cv2.imwrite('desk/corners_user_marked.png', m)
print('corners', C.round(1).tolist())
