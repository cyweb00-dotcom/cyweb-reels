# Per-frame glow track from the reference (flat 1280x720) -> film px (1920x1080).
import json,numpy as np
a=json.load(open('work/analysis.json'))
k=np.array([1,2,1],float);k/=k.sum()
def sm(v):
  v=np.array(v,float); p=np.pad(v,1,mode='edge'); return np.convolve(p,k,'valid')
cx=sm([o['glow']['cx'] for o in a]);cy=sm([o['glow']['cy'] for o in a])
sx=sm([o['glow']['sx'] for o in a]);sy=sm([o['glow']['sy'] for o in a]);ms=sm([o['glow']['mass'] for o in a])
A=ms*1280*720/(2*np.pi*sx*sy)/100.0
out=[dict(f=i+1,cx=round(cx[i]*1.5,1),cy=round(cy[i]*1.5,1),sx=round(sx[i]*1.5,1),sy=round(sy[i]*1.5,1),a=round(float(min(A[i],1.6)),3)) for i in range(len(a))]
json.dump(out,open('film/glow.json','w'));open('film/glow.js','w').write('window.GLOW_DATA='+json.dumps(out)+';')
print([ (o['f'],o['a']) for o in out[::12]])
