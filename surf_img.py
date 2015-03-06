import sys
print sys.path
import cv2
from matplotlib import pyplot as plt
print cv2.__version__
img = cv2.imread('Denali-flipped.jpeg')
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Create SURF object. You can specify params here or later.
# Here I set Hessian Threshold to 400
surf = cv2.SURF(400)

surf.hessianThreshold = 5000
# Find keypoints and descriptors directly
kp, des = surf.detectAndCompute(img,None)
print len(kp)

img2 = cv2.drawKeypoints(img,kp,None,(255,255,0),4)
plt.imshow(img2),plt.show()
