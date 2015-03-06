import numpy as np
import cv2
from SimpleCV import *

import sys
sys.path.append(r'C:\Users\chris.nelson\Desktop\NNet')
from sobol_lib_NoNumpy import *



def generateSobolCharacterizationPoints(numDims,numPts,starts,stops,resolution,startSeed = 0):
    dim_num = numDims

    seed = 0
    while seed < startSeed:
        qs = prime_ge ( dim_num )

        [ r, seed_out ] = i4_sobol ( dim_num, seed )
        seed = seed_out


    qs = prime_ge ( dim_num )
    pts=[]
    for pt in range( 0, numPts):
        newPt = False
        while newPt == False:

            [ r, seed_out ] = i4_sobol ( dim_num, seed )
            nxtPt = []
            for i in range(len(r)):
                rng = stops[i]-starts[i]


                newVal = float(round(starts[i]+rng*r[i],resolution[i]))
                #newVal = r[i]

                nxtPt.append(newVal)
            if nxtPt not in pts:
                pts.append(nxtPt)
                newPt = True
            seed = seed_out

    return pts





cap = cv2.VideoCapture(0)

#bgnd.resize(cap.get(4), cap.get(3),3)
frameCount = 10
frameList=[]
distList = []

colorsToTest=1000
mins = [0,0,0]
maxs = [255,255,255]
resolution=[0,0,0]
testPoints = generateSobolCharacterizationPoints(3,colorsToTest,mins,maxs,resolution,0)


print 'Acquiring background...'
while len(frameList)<frameCount:
    ret, frame = cap.read()
    frameList.append(Image(frame.transpose(1,0,2)[:,:,::-1]))
#frameList[-1].show()
adds=frameList[0]/len(frameList)
for i in range(1,len(frameList)):
    adds+=frameList[i]/len(frameList)
gs = adds


gsnump= gs.getNumpy()
##avgDivider = (gsnump.shape[0]*gsnump.shape[1]*255)
##r = np.sum(gsnump[:,:,0])*(1/avgDivider)
##g = np.sum(gsnump[:,:,1])*(1/avgDivider)
##b =np.sum(gsnump[:,:,2])*(1/avgDivider)
r = int(np.average(gsnump[:,:,0]))
g = int(np.average(gsnump[:,:,1]))
b = int(np.average(gsnump[:,:,2]))
print (r,g,b)

cap.release()
cv2.destroyAllWindows()

print 'Comparing colors...'
maxDist = 1e10
for pt in testPoints:
    col= (pt[0],pt[1],pt[2])
    matte = gs.hueDistance(col).binarize()
    point = [col,np.sum(matte.getNumpy())]
    distList.append([col,point])
    if point[1] < maxDist:
        maxDist = point[1]
        maxCol = point[0]

'''
maxDist = distList[0][1]
maxCol = distList[0][0]

for point in distList:
    if point[1] < maxDist:
        maxDist = point[1]
        maxCol = point[0]
'''
print 'Closet color found:'
print maxCol,maxDist