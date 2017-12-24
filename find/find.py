import sys
import cv2
import numpy as np

#  Global Variables



frame = None
window_name = 'Smoothing Demo'


def main(argv):
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    # Load the source image
    imageName = argv[0] if len(argv) > 0 else "../data/circle_square.jpg"

    global frame
    frame = cv2.imread(imageName, 1)
    if frame is None:
        print ('Error opening image')
        print ('Usage: find.py [image_name -- default ../data/circle_square] \n')
        return -1

    # find square   
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (ret,thresh) = cv2.threshold(imgray,127,255,0)
    # in copencv 3 you need 3 return parameters!
    (im, contours, hierarchy) = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    #find circle
    circles = []
    triangles = []
    squares = []

    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
        if ((len(approx) == 3) & (area > 6000) & (area < 20000)):
            print (len(approx),area)
            triangles.append(contour)
        if ((len(approx) == 4) & (area > 10000) & (area < 20000)):
            print (len(approx),area)
            squares.append(contour)
        if ((len(approx) > 8) & (area > 10000) & (area < 20000)):
            print (len(approx),area)
            circles.append(contour)
            
    cv2.drawContours(frame, squares,  -1, (255,0,0), 3)
    cv2.drawContours(frame, circles,  -1, (0,255,0), 3)
    cv2.drawContours(frame, triangles,  -1, (0,0,255), 3)

    #print contours
    cv2.imshow(window_name, frame)

    while(True):
        if cv2.waitKey(1) & 0xFF == ord('q'):
        	break

    return 0

cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv[1:])
