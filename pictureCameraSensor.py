import os
import picamera
import p3Picam
from datetime import datetime
from subprocess import call

from google.cloud import storage
from firebase import firebase

picturesURI = "/home/pi/AppPyCharm/Pictures/"
diskSpaceToReserve = 40 * 1024 * 1024  # Keep 40 mb free on disk
filenamePrefix = "IOT"



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/AppPyCharm/iotmotionsensor-e737c-firebase-adminsdk-byfm4-2183495c4a.json"
firebase = firebase.FirebaseApplication('https://iotmotionsensor-e737c.firebaseio.com')
client = storage.Client()
bucket = client.get_bucket('iotmotionsensor-e737c.appspot.com')


def captureImage(currentTime, picturesURI, diskSpaceToReserve):
    keepDiskSpaceFree(diskSpaceToReserve)
    # Generate the picture's name
    pictureName = filenamePrefix + currentTime.strftime("%Y.%m.%d-%H%M%S") + '.png'
    # Variable for file path
    filePath = picturesURI + pictureName
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(filePath)
    print("We have taken a picture.")
    return pictureName, filePath


def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime


def timeStamp(currentTime, filePath):
    # Create message to stamp on picture
    message = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
    # Create command to execute
    timestampCommand = "/usr/bin/convert " + filePath + " -pointsize 36 \
    -fill green -annotate +700+650 '" + message + "' " + filePath
    # Execute the command
    call([timestampCommand], shell=True)
    print("We have timestamped the picture.")


# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if getFreeSpace() < bytesToReserve:
        for pictureName in sorted(os.listdir(picturesURI)):
            if pictureName.startswith(filenamePrefix) and pictureName.endswith(".png"):
                os.remove(filePath)
                print("Deleted %s to avoid filling disk" % filePath)
                if getFreeSpace() > bytesToReserve:
                    return


# Get available disk space
def getFreeSpace():
    st = os.statvfs(picturesURI)
    du = st.f_bavail * st.f_frsize
    print("%i MB FREE" % ((du/1024)/1024))
    return du

motionState = False
while True:
    motionState = p3Picam.motion()
    print(motionState)
    if motionState:
        currentTime = getTime()
        pictureName, filePath = captureImage(currentTime, picturesURI, diskSpaceToReserve)
        timeStamp(currentTime, filePath)
        # Upload to Firebase
        imageBlob = bucket.blob("images/%s" % pictureName)
        imageBlob.upload_from_filename(filePath)
