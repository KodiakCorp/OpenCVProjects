import numpy as np
import cv2

from SimpleCV import *

cap = cv2.VideoCapture(0)
bgnd = cv2.imread('TIDE_PVT_icon.png')
background = Image('TIDE_PVT_icon.png')

#bgnd.resize(cap.get(4), cap.get(3),3)
col = (94.0, 221.0, 233.0)
blurAmount =1
frameList=[]
display = Display()
while display.isNotDone():

    ret, frame = cap.read()
    if len(frameList)<blurAmount:
        frameList.append(Image(frame.transpose(1,0,2)[:,:,::-1]))
    else:
        frameList=frameList[1:-1]
        frameList.append(Image(frame.transpose(1,0,2)[:,:,::-1]))

        adds=frameList[0]/len(frameList)
        for i in range(1,len(frameList)):
            adds+=frameList[i]/len(frameList)
        gs = frameList[-1]


    #cv2.waitKey(15)
    #h = cap.get(4)
    #w = cap.get(3)

    #color = scv.Color.RED
    #hdImg = hueDistance(frame, color, minsaturation = 20, minvalue = 10, maxvalue=255)

##    frame = cv2.cvtColor(frame, 41) #41 = CV_RGB2HSV
##    outputImage = np.where((frame[0] in range(20, 100)) & (frame[1] in range(30, 100)) & (frame[2] in range(200, 250)), bgnd, frame)

        #gs = scv.Image(frame,cv2image=True)
        #gs=Image(frame.transpose(1,0,2)[:,:,::-1])
        matte = gs.hueDistance(col, minsaturation = 15, minvalue = 10).equalize() #10,20
        #matte = matte.erode(1)
        #matte = matte.dilate(1)
        #matte = matte.smooth(aperature=(11,11))
        matte = matte.binarize(100).invert()  #220
        #matte.show()
        can = matte.edges(t1=100, t2=500)
        #can.show()
        ero = matte.erode(1)
        dil = matte.dilate(1)
        morphEdge = (dil - ero)#.dilate(2)
        #morphEdge.show()
        pastMEdge = morphEdge|can
        #pastMEdge.show()

        #edger.show()
        #edger = edger.dilate(8)
        #edger = edger.erode(7)
        #matte = matte.erode(0)
        #matte = matte.dilate(0)
        #matte = matte.smooth(aperature=(3,3))
        #matte = matte.morphOpen()
        #edger.show()
        matte = matte - pastMEdge
        #matte.smooth(aperature=(11,11))
        #matte.erode()
        #matte.show()
        #matte = matte.erode()
        #matte.smooth(aperature=(5,5))


        #bothMatte = invMatte.sideBySide(matte)
        invMatte = matte.invert()
        blobs = matte.findBlobs()
        for blob in blobs:
            if blob.area() < 980:
                #blob.drawHull(color=Color.RED,width=-1,alpha=255)
                bhm =blob.getFullHullMask()
                invMatte+=bhm
                matte -= bhm
            else:
                blobs.remove(blob)
        #bothMatte.show()
        blobs2 = invMatte.findBlobs()
        for blob in blobs2:
            if blob.area() < 980:
                bhm =blob.getFullHullMask()
                invMatte-=bhm
                matte += bhm
            else:
                blobs2.remove(blob)
        #invMatte.show()
        #print np.sum(matte.getNumpy())
        #invMatte.sideBySide(matte).show()
        result = (gs-matte)+(background-invMatte)
        result.show()

        if display.mouseRight: display.done = True

display.quit()
cap.release()
cv2.destroyAllWindows()
