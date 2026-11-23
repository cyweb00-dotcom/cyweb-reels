# Display-referred screen film -> how the desk camera sees the screen (measured levels, SHOT.md)
import numpy as np, cv2
BLACK=np.array([20,18,13],np.float32)   # BGR, measured screen black
WHITE=np.array([252,245,225],np.float32)  # BGR, measured text white
def xfer(img, soft=1.2):
  x=img.astype(np.float32)/255.0
  y=BLACK+(WHITE-BLACK)*(x**1.15)
  if soft>0: y=cv2.GaussianBlur(y,(0,0),soft)
  return y
