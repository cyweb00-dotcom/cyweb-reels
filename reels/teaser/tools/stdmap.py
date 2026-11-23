import cv2, numpy as np, glob
fs=sorted(glob.glob('ref/frames/*.png'))
acc=None;acc2=None;n=0
for f in fs[::2]:
    im=cv2.imread(f).astype(np.float32).mean(2)
    if acc is None: acc=np.zeros_like(im);acc2=np.zeros_like(im)
    acc+=im;acc2+=im*im;n+=1
mean=acc/n;std=np.sqrt(np.maximum(acc2/n-mean**2,0))
np.save('work/std.npy',std);np.save('work/mean.npy',mean)
v=np.clip(std*4,0,255).astype(np.uint8)
cv2.imwrite('work/std.png',v)
m=(std>12).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
cnts,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
c=max(cnts,key=cv2.contourArea)
print('area',cv2.contourArea(c),'bbox',cv2.boundingRect(c))
hull=cv2.convexHull(c)
ap=cv2.approxPolyDP(hull,0.01*cv2.arcLength(hull,True),True)
print(ap.reshape(-1,2))
