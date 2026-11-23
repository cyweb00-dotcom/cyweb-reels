# Read sub-frame stream from render_film.js, average sub-frames, write film/out/NNNN.png (0-based frame)
import sys,struct,numpy as np,cv2,os
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
r=sys.stdin.buffer; acc=None; cur=None
while True:
  h=r.read(16)
  if len(h)<16: break
  k,s,n,L=struct.unpack('<4I',h); im=cv2.imdecode(np.frombuffer(r.read(L),np.uint8),cv2.IMREAD_COLOR).astype(np.float32)
  # average in linear light so blur looks like a real exposure
  lin=(im/255.0)**2.2
  acc=lin if s==0 else acc+lin
  if s==n-1:
    cv2.imwrite(f'{out}/{k:04d}.png',np.clip(((acc/n)**(1/2.2))*255+0.5,0,255).astype(np.uint8))
