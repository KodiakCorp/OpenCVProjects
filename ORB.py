import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\PuppialPursuit.mp4')

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
        #
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #kernel = np.ones((3,3),np.uint8)

        #kernel = np.ones((3,3),np.uint8)
        #frame = cv2.erode(frame,kernel,iterations = 1)
        #frame = cv2.GaussianBlur(frame,(3,3),0)

       #frame = cv2.medianBlur(frame,3)


        #cv2.waitKey(30)
        #frame = cv2.Canny(frame,300,400)


        # Initiate STAR detector
        orb = cv2.ORB()
        # find the keypoints with ORB
        kp = orb.detect(frame,None)
        # compute the descriptors with ORB
        kp, des = orb.compute(frame, kp)
        # draw only keypoints location,not size and orientation
        frame = cv2.drawKeypoints(frame,kp,color=(0,255,0), flags=0)

        #frame = cv2.medianBlur(frame,3)
        out.write(frame)
        #print frame.shape
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
print 'done'
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()