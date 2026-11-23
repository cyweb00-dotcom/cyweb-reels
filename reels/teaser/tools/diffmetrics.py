# per-beat difference vs the reference: flat screen (mine through the screen transfer) and full desk frame
import cv2,numpy as np,sys,json
sys.path.insert(0,'tools'); from screen_xfer import xfer
beats={'title':(1,32),'icon':(33,67),'push-in':(68,88),'panel':(89,124),'invite':(125,157),'tunnel':(158,206),'whip':(207,240),'bar':(241,288),'closing':(289,328),'logo':(329,348),'end':(349,357)}
res={}
for n,(a,b) in beats.items():
  sc=[];dk=[]
  for f in range(a,b+1):
    r=cv2.imread('ref/flat/%04d.png'%f).astype(np.float32); m=xfer(cv2.resize(cv2.imread('film/out/%04d.png'%(f-1)),(1280,720),interpolation=cv2.INTER_AREA))
    sc.append(np.abs(cv2.resize(r,(160,90),interpolation=cv2.INTER_AREA)-cv2.resize(m,(160,90),interpolation=cv2.INTER_AREA)).mean())
    R=cv2.resize(cv2.imread('ref/frames/%04d.png'%f),(90,160),interpolation=cv2.INTER_AREA).astype(np.float32); M=cv2.resize(cv2.imread('out/desk/%04d.png'%(f-1)),(90,160),interpolation=cv2.INTER_AREA).astype(np.float32)
    dk.append(np.abs(R-M).mean())
  res[n]=dict(screen_mean_abs_diff=round(float(np.mean(sc)),1),whole_frame_mean_abs_diff=round(float(np.mean(dk)),1))
json.dump(res,open('out/diff_metrics.json','w'),indent=1)
for k,v in sorted(res.items(),key=lambda kv:-kv[1]['screen_mean_abs_diff']): print(k,v)
