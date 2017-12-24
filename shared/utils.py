import cv2

cv_version_major = cv2.__version__.split(".")[0]

def isCv2():
    return (cv_version_major == '2')

def isCv3():
    return (cv_version_major == '3')
