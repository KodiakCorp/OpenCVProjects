import numpy as np
import time
print 'np'
import cv2
print 'cv2'
from SimpleCV import *
print 'simple cv'
import Tkinter, tkFileDialog
print 'tkinter'
Tkinter.Tk().withdraw()
print 'tk root'
img_file_path = str(tkFileDialog.askopenfilename())
import sys
sys.path.append(img_file_path)

cap = cv2.VideoCapture(0)
#bgnd = cv2.imread('TIDE_PVT_icon.png')
#background = Image('TIDE_PVT_icon.png')
print img_file_path
background = Image(img_file_path)
background=background.resize(int(cap.get(3)), int(cap.get(4)))

col = (107.0, 125.0, 181.0) #(94.0, 221.0, 233.0)
blurAmount = 1
picsToSave = 5
thresh = 200
resultHist=[]
for r in range(picsToSave): resultHist.append([])
frameList=[]
display = Display()
while display.isNotDone():

    ret, frame = cap.read()
    if len(frameList)<blurAmount:
        frameList.append(Image(frame.transpose(1,0,2)[:,:,::-1]))
    else:
        frameList=frameList[1:-1]
        frameList.append(Image(frame.transpose(1,0,2)[:,:,::-1]))

##        adds=frameList[0]/len(frameList)
##        for i in range(1,len(frameList)):
##            adds+=frameList[i]/len(frameList)
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
        matte = gs.hueDistance(col, minsaturation = 20, minvalue = 10) #10,20
        matte = matte.erode(3)
        matte = matte.dilate(3)
        #matte = matte.smooth(aperature=(11,11))
        matte = matte.binarize(thresh).invert()  #220

        edger = matte.edges(t1=100, t2=500)
        #edger.show()
        edger = edger.dilate(8)
        edger = edger.erode(7)
        #matte = matte.erode(0)
        #matte = matte.dilate(0)
        #matte = matte.smooth(aperature=(5,5))
        #matte = matte.morphOpen()

        matte = matte & edger.invert()
        matte = matte.erode()
        matte = matte.smooth(aperature=(5,5))

        #print np.sum(matte.getNumpy())
        #matte.show()
        result = (gs-matte)+(background-matte.invert())
        result.show()

        if display.mouseRight:
            matteList = []
            threshOffs = [-8,-4,-1,0,1,4,8]
            for threshOff in threshOffs:
                matte = gs.hueDistance(col, minsaturation = 20, minvalue = 10) #10,20
                matte = matte.erode(3)
                matte = matte.dilate(3)
                matte = matte.binarize(thresh+threshOff).invert()  #220

                edger = matte.edges(t1=100, t2=500)
                edger = edger.dilate(8)
                edger = edger.erode(7)
                matte = matte & edger.invert()
                matte = matte.erode()
                #matte = matte.smooth(aperature=(5,5))
                matteList.append(matte)
                result = (gs-matte)+(background-matte.invert())
                result.save("Demo_"+str(threshOff)+".png")

            #avgMatte = np.average(matteList)
            for m in matteList:
                if matteList.index(m)==0:
                    avgMatte = m/len(matteList)
                else:
                    avgMatte+=m/len(matteList)



            invMatte = avgMatte.binarize()
            avgMatte = invMatte.invert()

            blobs = invMatte.findBlobs()
            for blob in blobs:
                if blob.area() < 1000:
                    blob.drawHull(color=Color.RED,width=-1,alpha=255)
                    bhm =blob.getFullHullMask()
                    invMatte+=bhm
                    avgMatte -= bhm
            blobs2 = invMatte.findBlobs()
            for blob in blobs2:
                if blob.area() < 1000:
                    blob.drawHull(color=Color.RED,width=-1,alpha=255)
                    bhm =blob.getFullHullMask()
                    invMatte-=bhm
                    avgMatte += bhm

            result = (gs-avgMatte)+(background-invMatte)
            result.save("Demo_Avg.png")

            display.done = True

display.quit()
cap.release()
cv2.destroyAllWindows()
