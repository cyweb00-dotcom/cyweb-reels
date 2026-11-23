import cv2,numpy as np,glob
C=np.load('work/ref_corners.npy').astype(np.float32)
W,H=1280,720
M=cv2.getPerspectiveTransform(C,np.float32([[0,0],[W,0],[W,H],[0,H]]))
for f in sorted(glob.glob('ref/frames/*.png')):
  im=cv2.imread(f)
  cv2.imwrite(f.replace('frames','flat'),cv2.warpPerspective(im,M,(W,H),flags=cv2.INTER_CUBIC))
