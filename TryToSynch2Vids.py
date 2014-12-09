#!/usr/bin/env python

'''
Simple example of stereo image matching and point cloud generation.

Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )
'''

import sys
sys.path.append(r'C:\OpenCV 2.4.10\opencv\sources\samples\python2')
import numpy as np
import cv2
ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'w') as f:
        f.write(ply_header % dict(vert_num=len(verts)))
        np.savetxt(f, verts, '%f %f %f %d %d %d')


if __name__ == '__main__':
    print 'loading images...'
    #imgL = cv2.pyrDown( cv2.imread('../gpu/aloeL.jpg') )  # downscale images for faster processing
    #imgR = cv2.pyrDown( cv2.imread('../gpu/aloeR.jpg') )
    #imgL = cv2.pyrDown( cv2.imread('C:\Users\chris.nelson\Desktop\OpenCV Programs\IMAG0224.jpg') )  # downscale images for faster processing
    #imgR = cv2.pyrDown( cv2.imread('C:\Users\chris.nelson\Desktop\OpenCV Programs\IMAG0223.jpg') )

    Lvname = 'L1.avi'
    Rvname = 'R1.avi'
    capL = cv2.VideoCapture('C:\\Users\\chris.nelson\\Desktop\\Vid Captures\\Quad\\LEFT_2in_AndTilt\\'+Lvname)
    capR = cv2.VideoCapture('C:\\Users\\chris.nelson\\Desktop\\Vid Captures\\Quad\\RIGHT_2in_AndTilt\\'+Rvname)
    capL.set(4, 640)
    capL.set(3, 480)
    capR.set(4, 640)
    capR.set(3, 480)
    while(capR.isOpened() & capL.isOpened()):
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        #LuS = capL.get(CV_CAP_PROP_POS_MSEC)
        #RuS = capR.get(CV_CAP_PROP_POS_MSEC)
        cv2.waitKey(40)

        #print str(LuS)+','+str(RuS)
        if retR==True:
            cv2.imshow('right',frameR)
        if retL==True:
            cv2.imshow('left', frameL)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.waitKey()
    capL.release()
    capR.release()
    cv2.destroyAllWindows()
