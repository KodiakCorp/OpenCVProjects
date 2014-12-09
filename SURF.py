import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\PuppialPursuit.mp4')

#cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\DogeChaseRoundDeux.avi')

#cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fourcc = cv2.cv.CV_FOURCC(*'DIVX')
out = cv2.VideoWriter('contourOut2.avi',fourcc, 20.0, (640,480))
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

        #ret,frame = cv2.threshold(frame,127,255,0)

        surf = cv2.SURF(10000)
        kp,des = surf.detectAndCompute(frame,None)
        print len(kp)
        frame = cv2.drawKeypoints(frame,kp,None,(255,0,0),4)

        #frame = cv2.medianBlur(frame,3)
        out.write(frame)
        print frame.shape
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