#!/usr/bin/env python

import sys
import os

DIRNAME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(DIRNAME+'/../../')

import argparse
import numpy as np
import cv2
import cv_experiments.shared.utils as su


def restricted_float(x):
    x = float(x)
    if x < 1.0 or x > 10.0:
        raise argparse.ArgumentTypeError("%r not in range [1.0, 10.0]"%(x,))
    return x

def cannyCenterChange(val):
    updateCannyParameters("center",val)

def cannySpreadChange(val):
    updateCannyParameters("spread",val)

def updateCannyParameters(key, val):
    global canny, parameters_changed
    canny[key] = val
    canny["lower"] = int(max(0, (1.0 - 0.01*canny["spread"])* canny["center"]))
    canny["upper"] = int(min(255, (1.0 + 0.01*canny["spread"]) * canny["center"]))
    parameters_changed = True

def gammaChange(val):
    global mygamma, parameters_changed
    mygamma = 0.1 * (float(val)+10)
    parameters_changed = True


def main(argv):
    global canny
    global mygamma
    global parameters_changed 

    canny = { 'center' : 100, 'spread' : 33, 'upper' : 133.0, 'lower' : 67.0 }
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gamma", 
        type=restricted_float,
        required=False, 
        default='1', 
        help="Gamma correction value (between 1.0 and 10.0, default = 1.0)")
    args = vars(ap.parse_args())
    mygamma = float(args["gamma"])

    parameters_changed = True
    #cap = cv2.VideoCapture(DIRNAME +'/../data/car-overhead-1.avi')
    cap = cv2.VideoCapture(DIRNAME +'/../data/scaled.mp4')

    cv2.namedWindow("frame")
    cv2.namedWindow("parameters")
    
    
    cv2.createTrackbar("Gamma","parameters",int(mygamma * 10),90,gammaChange)
    cv2.createTrackbar("Canny: center","parameters",100,255,cannyCenterChange)
    cv2.createTrackbar("Canny: spread","parameters",33,100,cannySpreadChange)


    feedback_bg = np.zeros((300,600,3), np.uint8)
    feedback_bg[:] = (200,200,200)
    cv2.imshow("parameters",feedback_bg)

    if su.isCv2():
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    elif su.isCv3():
        fps = cap.get(cv2.CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)


    while(cap.isOpened()):
        ret, frame = cap.read()
        if frame is not None:
            frame = su.adjustGamma(frame,mygamma)
            contours = su.getContours(frame,["edged"],canny)
            for contour in contours:
                peri = cv2.arcLength(contour, True)
                if peri >= 200 and peri <= 350:
                    approx = cv2.approxPolyDP(contour, 16, True)
                    #print len(approx)
                    #print peri
                    cv2.drawContours(frame, [contour],  -1, (0,255,0), 3)
                    cv2.drawContours(frame, approx,  -1, (255,0,0), 5)
                    

            
            cv2.imshow('frame',frame)

            if parameters_changed == True: # update feedback
                text_y = 30
                feedback_bg[:] = (127,127,127)
                status = "gamma: " + str(mygamma) 
                cv2.putText(feedback_bg, status, (22, text_y), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
                text_y +=15
                for item in canny.items():
                    status = "canny " + item[0] + ": " + str(item[1]) 
                    cv2.putText(feedback_bg, status, (22, text_y), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
                    text_y = text_y + 15
    	    
                cv2.imshow('parameters',feedback_bg)
                parameters_changed = False

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            print "the end"
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])





