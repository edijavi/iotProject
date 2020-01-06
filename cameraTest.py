import os
from datetime import datetime
import picamera
import saveCloud

picturesURI = "/home/pi/AppPyCharm/Pictures/"


# Setup the camera such that it closes when we are done with it.
def captureImage(currentTime, picturesURI):
    # Generate the picture's name
    pictureName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.jpg'
    filePath = picturesURI + pictureName

    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(filePath)
    print("Picture Taken")
    return pictureName, filePath


def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime


currentTime = getTime()
pictureName, filePath = captureImage(currentTime, picturesURI)
print("%s %s" % (filePath, pictureName))
saveCloud.saveToFirebase(pictureName, filePath)
