import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\chris.nelson\Desktop\OpenCV Programs\cannyoutput3.avi')

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.waitKey(15)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print frame.shape
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()