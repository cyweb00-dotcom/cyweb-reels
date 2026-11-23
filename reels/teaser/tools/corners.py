import numpy as np, cv2
std=np.load('work/std.npy')
m=(std>12).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
H,W=m.shape
def fit(pts):  # fit line through points, returns (a,b,c) with ax+by+c=0
    pts=np.array(pts,np.float32)
    vx,vy,x0,y0=cv2.fitLine(pts,cv2.DIST_HUBER,0,0.01,0.01).ravel()
    return np.array([vy,-vx,vx*y0-vy*x0])
top=[];bot=[];lef=[];rig=[]
for x in range(80,660,4):
    col=np.where(m[300:900,x])[0]
    if len(col): top.append((x,300+col[0]));bot.append((x,300+col[-1]+1))
for y in range(460,760,4):
    row=np.where(m[y,15:715])[0]+15
    if len(row): lef.append((row[0],y));rig.append((row[-1]+1,y))
L=[fit(p) for p in (top,rig,bot,lef)]
def inter(a,b):
    p=np.cross(a,b);return p[:2]/p[2]
C=[inter(L[3],L[0]),inter(L[0],L[1]),inter(L[1],L[2]),inter(L[2],L[3])]
for n,c in zip(['TL','TR','BR','BL'],C): print(n,'%.1f %.1f'%tuple(c))
np.save('work/ref_corners.npy',np.array(C))
