#!/usr/bin/env python

import sys
import os

DIRNAME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(DIRNAME+'/../../')

import argparse
import numpy as np
import cv2
import cv_experiments.shared.utils as su

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gamma", 
    required=False, 
    default='1', 
    help="Gamma correction value (default = 1)")
args = vars(ap.parse_args())
mygamma = float(args["gamma"])


def main(argv):
    #cap = cv2.VideoCapture(DIRNAME +'/../data/car-overhead-1.avi')
    cap = cv2.VideoCapture(DIRNAME +'/../data/scaled.mp4')
    printed = False

    if su.isCv2():
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    elif su.isCv3():
        fps = cap.get(cv2.CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)


    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = su.adjustGamma(frame,mygamma)

        if frame is not None:
            contours = su.getContours(frame)
            for contour in contours:
                peri = cv2.arcLength(contour, True)
                if peri >= 200 and peri <= 350:
                    approx = cv2.approxPolyDP(contour, 16, True)
                    print len(approx)
                    print peri
                    cv2.drawContours(frame, approx,  -1, (255,0,0), 3)
                    #cv2.drawContours(frame, [contour],  -1, (255,0,0), 3)
    	    cv2.imshow('frame',frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        elif printed is False:
            print "the end"
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])





