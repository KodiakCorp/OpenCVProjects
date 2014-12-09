import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\Vid Captures\Quad\PuppialPursuit.mp4')

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fourcc = cv2.cv.CV_FOURCC(*'DIVX')
out = cv2.VideoWriter('OtsuThreshOutput.avi',fourcc, 20.0, (640,480))
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
        #mini = np.array([0,0,0])
        #maxi = np.array([250,250,250])
        #mask = cv2.inRange(frame,mini,maxi)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame,(5,5),0)
        #mask = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        #frame = cv2.cvtcolor(frame,cv2.COLOR_BGR2HSV)

        #plt.imshow(mask,'gray')
        #plt.show()
        #frame = cv2.bitwisqe_and(tframe,tframe,mask=mask)
        img = frame
        ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                    cv2.THRESH_BINARY,11,2)
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)

        titles = ['Original Image', 'Global Thresholding (v = 127)',
                    'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
        images = [img, th1, th2, th3]

        for i in xrange(4):
            plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])
        plt.show()

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