import cv2
import numpy as np

cv_version_major = cv2.__version__.split(".")[0]

def isCv2():
    return (cv_version_major == '2')

def isCv3():
    return (cv_version_major == '3')

def adjustGamma(image, gamma=1):
    # apply gamma correction using the lookup table
    return cv2.LUT(image, getTable(gamma))

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:        
            memo[x] = f(x)
        return memo[x]
    return helper

@memoize
def getTable(gamma):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return table

def getContours(img,show=(),canny_params = None):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if 'gray' in show: cv2.imshow('gray',gray)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    if 'blurred' in show: cv2.imshow('blurred',blurred)
    edged = cv2.Canny(blurred,  
        canny_params["lower"] if canny_params else 50,
        canny_params["upper"] if canny_params else 150)
    if 'edged' in show: cv2.imshow('edged',edged)
    # find contours in the edge map
    if isCv2():
        contours,hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    elif isCv3():
        im,contours,hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    return contours  
