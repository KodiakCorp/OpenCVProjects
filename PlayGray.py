import numpy as np
import cv2
print cv2.__version__
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()
    print ret
    print cap.get(3)
    #cv2.waitKey(15)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print frame.shape
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()