import numpy as np
import cv2

from SimpleCV import *

'''


def hueDistance(frame,color = scv.Color.BLACK, minsaturation = 20, minvalue = 20, maxvalue=255):

    if isinstance(color,  (float,int,long,complex)):
        color_hue = color
    else:
        color_hue = scv.Color.hsv(color)[0]

    hsvFrame = cv2.cvtColor(frame, 41) #41 = CV_RGB2HSV
    npFrame = getNumpy(frame).reshape(-1,3)

    #vsh_matrix = self.toHSV().getNumpy().reshape(-1,3) #again, gets transposed to vsh

    hue_channel = np.cast['int'](npFrame[:,2])

    if color_hue < 90:
        hue_loop = 180
    else:
        hue_loop = -180
    #set whether we need to move back or forward on the hue circle

    distances = np.minimum( np.abs(hue_channel - color_hue), np.abs(hue_channel - (color_hue + hue_loop)))
    #take the minimum distance for each pixel


    distances = np.where(
        np.logical_and(npFrame[:,0] > minvalue, npFrame[:,1] > minsaturation),
        distances * (255.0 / 90.0), #normalize 0 - 90 -> 0 - 255
        255.0) #use the maxvalue if it false outside of our value/saturation tolerances
    return distances.reshape(frame.shape[0], frame.shape[1])



def getNumpy(frame):
    npFrame = (np.array((frame))[:, :, ::-1]).transpose([1, 0, 2])
    return npFrame

def getMatrix(frame):
    return cv2.GetMat(frame)

def getBitmap(frame):
    return cv2.GetImage(frame)

'''
'''
def transpose(frame,h,w):
    retVal = cv2.CreateImage((h, w), cv2.IPL_DEPTH_8U, 3)
    cv2.Transpose(frame, retVal)
    return retVal
'''

cap = cv2.VideoCapture(0)
bgnd = cv2.imread('TIDE_PVT_icon.png')
background = Image('TIDE_PVT_icon.png')

#bgnd.resize(cap.get(4), cap.get(3),3)
col = (94.0, 221.0, 233.0)
blurAmount = 2
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
        matte = gs.hueDistance(col, minsaturation = 15, minvalue = 10) #10,20
        #matte = matte.erode(1)
        #matte = matte.dilate(1)
        #matte = matte.smooth(aperature=(11,11))
        matte = matte.binarize(222).invert()  #220

        can = matte.edges(t1=100, t2=500)

        ero = matte.erode(1)
        dil = matte.dilate(1)
        morphEdge = (dil - ero)#.dilate(2)


        #edger.show()
##        edger = edger.dilate(8)
##        edger = edger.erode(7)


        matte2 = frameList[0].hueDistance(col, minsaturation = 15, minvalue = 10).equalize() #10,20
        matte2.show()
        matte2 = matte2.binarize(222).invert()  #220
        can2 = matte.edges(t1=100, t2=500)

        ero2 = matte2.erode(1)
        dil2 = matte2.dilate(1)
        morphEdge2 = (dil2 - ero2)#.dilate(2)
        pastMEdge = morphEdge | morphEdge2|can|can2
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
        #result.show()

        if display.mouseRight: display.done = True

display.quit()
cap.release()
cv2.destroyAllWindows()
