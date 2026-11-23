# side-by-side: reference flat (left) vs mine through the screen transfer (right), 1-based ref frames
import sys,cv2,numpy as np
sys.path.insert(0,'tools'); from screen_xfer import xfer
fs=[int(a) for a in sys.argv[2:]]; rows=[]
for f in fs:
  r=cv2.imread('ref/flat/%04d.png'%min(f,357)); m=cv2.imread('film/out/%04d.png'%(f-1))
  m=xfer(cv2.resize(m,(1280,720),interpolation=cv2.INTER_AREA)).clip(0,255).astype(np.uint8)
  row=np.hstack([r,np.full((720,8,3),255,np.uint8),m]); row=cv2.resize(row,None,fx=.5,fy=.5)
  cv2.putText(row,str(f),(8,30),0,1,(0,255,255),2); rows.append(row)
cv2.imwrite(sys.argv[1],np.vstack(rows))
