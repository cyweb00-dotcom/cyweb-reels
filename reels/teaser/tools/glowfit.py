# Fit 3 elliptical Gaussians per reference frame to the teal glow (captured G excess over black).
# Objects (text, glass, phones: low-saturation bright pixels) are masked out of the fit.
import cv2,numpy as np,json
from scipy.optimize import least_squares
W,H=64,36; K=3; GB=18.0
ys,xs=np.mgrid[0:H,0:W].astype(np.float64)
def model(p):
  m=np.zeros((H,W))
  for k in range(K):
    cx,cy,sx,sy,a=p[5*k:5*k+5]
    m+=a*np.exp(-0.5*(((xs-cx)/sx)**2+((ys-cy)/sy)**2))
  return m
p=np.array([32,24,14,8,80, 32,12,10,10,30, 32,30,25,6,40],float)
lo=np.array([-20,-20,2,2,0]*K,float); hi=np.array([84,56,80,60,400]*K,float)
out=[]; err=[]
for i in range(1,358):
  im=cv2.imread('ref/flat/%04d.png'%i).astype(np.float32)
  sm=cv2.resize(im,(W,H),interpolation=cv2.INTER_AREA)
  b,g,r=sm[...,0],sm[...,1],sm[...,2]; mx=sm.max(2); mn=sm.min(2); sat=(mx-mn)/(mx+1)
  E=np.clip(g-GB,0,None)
  w=np.ones_like(E); w[(sat<0.28)&(g>55)]=0.0      # objects
  if w.mean()<0.25: w[:]=1.0                         # white-out frames: nothing to fit
  if i>=349: E[:]=0
  f=lambda q:((model(q)-E)*w).ravel()
  best=None
  for start in (p, np.array([32,18,20,10,max(E.max(),1)]+[32,30,12,6,E.max()/2]+[32,8,12,8,E.max()/3])):
    s=np.clip(start,lo+1e-3,hi-1e-3)
    r_=least_squares(f,s,bounds=(lo,hi),max_nfev=400)
    if best is None or r_.cost<best.cost: best=r_
  p=best.x; e=np.sqrt(np.mean(((model(p)-E)*w)**2)); err.append(e)
  sx=1280/W
  out.append([dict(cx=round(p[5*k]*sx*1.5+sx*0.75,1),cy=round(p[5*k+1]*sx*1.5+sx*0.75,1),sx=round(p[5*k+2]*sx*1.5,1),sy=round(p[5*k+3]*sx*1.5,1),a=round(p[5*k+4],1)) for k in range(K)])
json.dump(out,open('film/glow3.json','w'))
open('film/glow.js','w').write('window.GLOW3='+json.dumps(out)+';')
print('rms fit error (G levels): mean %.1f max %.1f at frame %d'%(np.mean(err),np.max(err),int(np.argmax(err))+1))
