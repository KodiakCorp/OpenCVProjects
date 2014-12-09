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

    Lvname = 'MINI0001.MOV'
    Rvname = 'MINI0002.MOV'
    capL = cv2.VideoCapture('C:\\Users\\chris.nelson\\Desktop\\Vid Captures\\'+Lvname)
    capR = cv2.VideoCapture('C:\\Users\\chris.nelson\\Desktop\\Vid Captures\\'+Rvname)

    window_size = 2
    min_disp = -5
    #num_disp = 112-min_disp
    num_disp = 128
    stereo = cv2.StereoSGBM(minDisparity = min_disp,
        numDisparities = num_disp,
        SADWindowSize = window_size,
        uniquenessRatio = 2,
        #uniquenessRatio = 10,
        speckleWindowSize = 150,
        preFilterCap = 1,
        #speckleWindowSize = 100,
        speckleRange = 50     ,
        disp12MaxDiff = 5,
        #disp12MaxDiff = 10,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        fullDP = True
    )

    capL.set(4, 640)
    capL.set(3, 480)
    capR.set(4, 640)
    capR.set(3, 480)
    while(capL.isOpened() and capR.isOpened()):
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        if (retL==True)and (retR==True):
            #frame = frame[5:475,115:735,:]
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #print 'computing disparity...'

            frameL = cv2.pyrDown(frameL)
            frameR = cv2.pyrDown(frameR)

            disp = stereo.compute(frameL, frameR).astype(np.float32) / 16.0




            #print 'generating 3d point cloud...',



            h, w = frameL.shape[:2]
            f =  0.8*w #0.001*w                         # guess for focal length
            Q = np.float32([[1, 0, 0, -0.5*w],
                            [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
                            [0, 0, 0,     -f], # so that y-axis looks up
                            [0, 0, 1,      0]])
            points = cv2.reprojectImageTo3D(disp, Q)


            #colors = cv2.cvtColor(frameL, cv2.COLOR_BGR2RGB)
            #mask = disp > disp.min()
            #out_points = points[mask]
            #out_colors = colors[mask]
            #out_fn = 'out.ply'
            #write_ply('out.ply', out_points, out_colors)
            #print '%s saved' % 'out.ply'

            cv2.imshow('right',frameR)
            cv2.imshow('left', frameL)

            cv2.imshow('disparity', (disp-min_disp)/num_disp)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.waitKey()
    capL.release()
    capR.release()
    cv2.destroyAllWindows()
