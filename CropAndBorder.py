import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\PuppialPursuit.mp4')

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#fourcc = cv2.cv.CV_FOURCC(*'WMV1')
#out = cv2.VideoWriter('output.wmv',fourcc, 20.0, (640,480))
out = cv2.VideoWriter('output.avi',-1, 20.0, (620,470))
print out.isOpened()
while(cap.isOpened()):
    ret, frame = cap.read()
    #print cap.get(3)#h
    #print cap.get(4)#w
    if ret==True:
        frame = frame[5:475,115:735,:]
        frame = cv2.flip(frame,0)
        frame = cv2.copyMakeBorder(frame,200,120,450,450,cv2.BORDER_REFLECT_101)
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