import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\PuppialPursuit.mp4')

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fourcc = cv2.cv.CV_FOURCC(*'DIVX')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
i=0
while(cap.isOpened()):
    i=i+1
    ret, frame = cap.read()
    if ret==True:
        frame = frame[5:475,115:735,:]
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if i == 1:
            oldframe = frame

        tframe = frame
        #frame = oldframe - frame
        frame = cv2.addWeighted(frame,-1,oldframe,1,0)
         frame = cv2.bitwise_not(frame)
        mini = np.array([0,0,0])
        maxi = np.array([250,250,250])
        mask = cv2.inRange(frame,mini,maxi)
        #frame = cv2.cvtcolor(frame,cv2.COLOR_BGR2HSV)
        frame = cv2.bitwise_and(tframe,tframe,mask=mask)


        oldframe = tframe
        #frame = cv2.copyMakeBorder(frame,200,120,450,450,cv2.BORDER_REFLECT_101)
        # write the flipped frame
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