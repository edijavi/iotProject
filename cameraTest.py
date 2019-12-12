from datetime import datetime
from google.cloud import storage

import picamera

from firebase import firebase


# Setup the camera such that it closes when we are done with it.
def captureImage(currentTime, picturesURI):
    # Generate the picture's name
    pictureName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(picturesURI + pictureName)
    print("Picture Taken")
    return pictureName


def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime


def main():
    picturesURI = "/home/pi/AppPyCharm/Pictures/"
    currentTime = getTime()
    pictureName = captureImage(currentTime, picturesURI)

    client = storage.Client()
    bucket = client.get_bucket('iot-easv2019.appspot.com')
    zebraBlob = bucket.get_blob('pictureName')
    zebraBlob.upload_from_filename(filename='/%s%s' % (picturesURI, pictureName))


# Run the Program
if __name__ == "__main__":
    main()
