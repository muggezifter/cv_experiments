import numpy as np
import cv2
import sys
sys.path.append('../../')
import cv_experiments.shared.utils as su

def main(argv):
    cap = cv2.VideoCapture('../data/car-overhead-1.avi')
    printed = False

    if su.isCv2():
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    elif su.isCv3():
        fps = cap.get(cv2.CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)


    while(cap.isOpened()):
        ret, frame = cap.read()

        if frame is not None:
    	    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    	    cv2.imshow('frame',frame)
    	elif printed is False:
    		print "the end"
    		printed = True
    	if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])





