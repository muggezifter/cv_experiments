#!/usr/bin/env python

import sys
import os
import cv2
import numpy as np

DIRNAME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(DIRNAME+'/../../')
import cv_experiments.shared.utils as su

#  Global Variables
frame = None
window_name = 'detect square and circle'

def main(argv):
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    # Load the source image
    imageName = argv[0] if len(argv) > 0 else DIRNAME + "/../data/circle_square.jpg"

    frame = cv2.imread(imageName, 1)
    if frame is None:
        print ('Error opening image')
        print ('Usage: find.py [image_name -- default ../data/circle_square] \n')
        return -1

    # find square   
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (ret,thresh) = cv2.threshold(imgray,127,255,0)

    # in copencv 3 you need 3 return parameters!
    if su.isCv2():
        (contours, hierarchy) = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    elif su.isCv3():
        (im, contours, hierarchy) = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    #find circle
    circles = []
    triangles = []
    squares = []

    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        (x, y, w, h) = cv2.boundingRect(approx)
        aspectRatio = w / float(h)

        area = cv2.contourArea(contour)
        M = cv2.moments(approx)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # square   
        if ((len(approx) == 4) and np.isclose(area,15000,0,2000) and np.isclose(aspectRatio,1,0,0.1)): 
            squares.append((contour,center))

        # circle
        if ((len(approx) > 8) and np.isclose(area,15000,1,2000) and np.isclose(aspectRatio,1,0,0.1)):
            circles.append((contour,center))
     
    for square in squares:       
        cv2.drawContours(frame, [square[0]],  -1, (255,0,0), 3)
        drawCross(frame,square[1], (255,0,0))
        break # only use the first one
    for circle in circles:
        cv2.drawContours(frame, [circle[0]],  -1, (0,255,0), 3)
        drawCross(frame,circle[1], (0,255,0))
        break # only use the first one
    #print contours
    cv2.imshow(window_name, frame)

    while(True):
        if cv2.waitKey(1) & 0xFF == ord('q'):
        	break

    cv2.destroyAllWindows()
    return 0


def drawCross(img, center, color):    
    (cX,cY) = center
    (startX, endX) = (int(cX - 15), int(cX + 15))
    (startY, endY) = (int(cY - 15), int(cY + 15))
    cv2.line(img, (startX, cY), (endX, cY), color, 3)
    cv2.line(img, (cX, startY), (cX, endY), color, 3)

if __name__ == "__main__":
    main(sys.argv[1:])





