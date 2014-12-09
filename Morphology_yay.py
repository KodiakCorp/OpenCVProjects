import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\PuppialPursuit.mp4')

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fourcc = cv2.cv.CV_FOURCC(*'DIVX')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
i=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = frame[5:475,115:735,:]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #kernel = np.ones((3,3),np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))

        ero = cv2.erode(frame,kernel,iterations = 1)
        dil = cv2.dilate(frame,kernel,iterations = 1)
        frame = dil-ero
        #frame2 = cv2.morphologyEx(frame,cv2.MORPH_GRADIENT,kernel)
        out.write(frame)
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