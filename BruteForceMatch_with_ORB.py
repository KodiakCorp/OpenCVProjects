import numpy as np
import cv2
from matplotlib import pyplot as plt
from drawMatches import *

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\PuppialPursuit.mp4')
kodiak = cv2.imread('KodiakCutout.png')
#cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\DogeChaseRoundDeux.avi')

#cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fourcc = cv2.cv.CV_FOURCC(*'DIVX')
out = cv2.VideoWriter('FASTOut2.avi',fourcc, 20.0, (640,480))
i=0
cap.set(4, 640);
cap.set(3, 480)
while(cap.isOpened()):
    ret, frame = cap.read()
    print
    if ret==True:
        frame = frame[5:475,115:735,:]
        '''if i == 0:
            of = frame
            of2 = frame
            i=i+1
        elif i == 1:
            of2 = of
            i=i+1
        '''
        # Initiate SIFT detector
        orb = cv2.ORB()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = orb.detectAndCompute(frame,None)
        kp2, des2 = orb.detectAndCompute(kodiak,None)
        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # Match descriptors.
        matches = bf.match(des1,des2)
        # Sort them in the order of their distance.
        matches = sorted(matches, key = lambda x:x.distance)
        # Draw first 10 matches.
        BFM = drawMatches(frame,kp1,kodiak,kp2,matches[:15])



        #frame = cv2.medianBlur(frame,3)
        #of2 = of
        #of = frame
        out.write(frame)
        #print frame.shape
        cv2.imshow('frame',BFM)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
print 'done'
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()