import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\PuppialPursuit.mp4')

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#fourcc = cv2.cv.CV_FOURCC(*'DIVX')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
w=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH ))
h=int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))
# video recorder
fourcc = cv2.cv.CV_FOURCC(*'DIVX')  # cv2.VideoWriter_fourcc() does not exist
out = cv2.VideoWriter("output.avi", fourcc, 20, (w, h),1)
print out.isOpened()

#out = cv2.VideoWriter('tester.avi',1,1,(1520,720))
i=0
while(cap.isOpened()):
    i=i+1
    ret, frame = cap.read()
    if ret==True:
        frame = frame[5:475,115:735,:]

        rows = int(len(frame[:,0]))
        cols = int(len(frame[0,:]))
        if i == 360:
            i=0

        #z=i/360+1
        z=1
        M = cv2.getRotationMatrix2D((cols/2,rows/2),i*2,z)
        frame = cv2.warpAffine(frame,M,(cols,rows))
        frame = cv2.copyMakeBorder(frame,200,120,450,450,cv2.BORDER_REFLECT_101)
        #print frame.shape
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