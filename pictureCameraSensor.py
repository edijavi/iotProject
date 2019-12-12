import os
import picamera
import p3Picam
from datetime import datetime
from subprocess import call

from google.cloud import storage
from firebase import firebase

picturesURI = "/home/pi/AppPyCharm/Pictures/"

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/AppPyCharm/iotmotionsensor-e737c-firebase-adminsdk-byfm4-2183495c4a.json"
firebase = firebase.FirebaseApplication('https://iotmotionsensor-e737c.firebaseio.com')
client = storage.Client()
bucket = client.get_bucket('iotmotionsensor-e737c.appspot.com')


def captureImage(currentTime, picturesURI):
    # Generate the picture's name
    pictureName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.png'
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(picturesURI + pictureName)
    print("We have taken a picture.")
    return pictureName


def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime


def timeStamp(currentTime, picturesURI, pictureName):
    # Variable for file path
    filePath = picturesURI + pictureName
    # Create message to stamp on picture
    message = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
    # Create command to execute
    timestampCommand = "/usr/bin/convert " + filePath + " -pointsize 36 \
    -fill green -annotate +700+650 '" + message + "' " + filePath
    # Execute the command
    call([timestampCommand], shell=True)
    print("We have timestamped the picture.")
    imageBlob = bucket.blob("images/%s" % pictureName)
    imageBlob.upload_from_filename(filePath)


motionState = False
while True:
    motionState = p3Picam.motion()
    print(motionState)
    if motionState:
        currentTime = getTime()
        pictureName = captureImage(currentTime, picturesURI)
        timeStamp(currentTime, picturesURI, pictureName)
