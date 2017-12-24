import numpy as np
import cv2

cap = cv2.VideoCapture('../data/car-overhead-1.avi')
printed = False

while(cap.isOpened()):
    ret, frame = cap.read()

    if frame is None:
    	print "the end"
    	break
    else:
    	#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    	cv2.imshow('frame',frame)
    	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break

cap.release()
cv2.destroyAllWindows()



