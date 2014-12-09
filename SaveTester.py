import cv2

img1 = cv2.imread('Denali-flipped.jpeg')
img2 = cv2.imread('Denali-flipped.jpeg')
img3 = cv2.imread('Denali-flipped.jpeg')

height , width , layers =  img1.shape

video = cv2.VideoWriter('videoRLE.avi',-1,1,(width,height))

video.write(img1)
video.write(img2)
video.write(img3)

cv2.destroyAllWindows()
video.release()