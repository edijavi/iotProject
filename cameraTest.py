import os
from datetime import datetime
import picamera
from google.cloud import storage
from firebase import firebase

picturesURI = "/home/pi/AppPyCharm/Pictures/"


# Setup the camera such that it closes when we are done with it.
def captureImage(currentTime, picturesURI):
    # Generate the picture's name
    pictureName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.jpg'
    filePath = picturesURI + pictureName
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(picturesURI + pictureName)
    print("Picture Taken")
    return pictureName, filePath


def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime


currentTime = getTime()
pictureName, filePath = captureImage(currentTime, picturesURI)
print("%s %s" % (filePath, pictureName))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/AppPyCharm/iotmotionsensor-e737c-firebase-adminsdk-byfm4-2183495c4a.json"
firebase = firebase.FirebaseApplication('https://iotmotionsensor-e737c.firebaseio.com')
client = storage.Client()
bucket = client.get_bucket('iotmotionsensor-e737c.appspot.com')
imageBlob = bucket.blob("images/%s" % pictureName)
imageBlob.upload_from_filename(filePath)
