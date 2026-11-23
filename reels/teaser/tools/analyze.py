import cv2,numpy as np,json
N=357;out=[]
for i in range(1,N+1):
  im=cv2.imread('ref/flat/%04d.png'%i).astype(np.float32)
  b,g,r=im[...,0],im[...,1],im[...,2]
  mx=im.max(2);mn=im.min(2);sat=(mx-mn)/(mx+1)
  # teal glow intensity: green/blue over red, saturated
  teal=np.clip((g+b)/2-r,0,None)*(sat>0.25)
  t=cv2.resize(teal,(320,180),interpolation=cv2.INTER_AREA)
  ys,xs=np.mgrid[0:180,0:320]*4.0
  s=t.sum()+1e-6
  cx=(t*xs[1]).sum()/s if False else (t*np.mgrid[0:180,0:320][1]*4).sum()/s
  cy=(t*np.mgrid[0:180,0:320][0]*4).sum()/s
  sx=np.sqrt((t*(np.mgrid[0:180,0:320][1]*4-cx)**2).sum()/s); sy=np.sqrt((t*(np.mgrid[0:180,0:320][0]*4-cy)**2).sum()/s)
  # glow colour: median of top 5% teal pixels
  sel=teal>np.percentile(teal,97); col=np.median(im[sel],0)[::-1] if sel.any() else [0,0,0]
  # white text/objects: bright & low sat
  wm=((mn>150)&(sat<0.25)).astype(np.uint8)
  ys2,xs2=np.where(wm)
  wb=[int(xs2.min()),int(ys2.min()),int(xs2.max()),int(ys2.max())] if len(xs2)>20 else None
  meanlum=float(mx.mean())
  out.append(dict(f=i,glow=dict(cx=round(float(cx)),cy=round(float(cy)),sx=round(float(sx)),sy=round(float(sy)),mass=round(float(t.mean()),1),rgb=[int(v) for v in col]),white_bbox=wb,white_px=int(wm.sum()),lum=round(meanlum,1)))
json.dump(out,open('work/analysis.json','w'))
for o in out[::6]: print(o['f'],o['glow'],o['white_bbox'],o['white_px'],o['lum'])
