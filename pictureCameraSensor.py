import p3Picam
import picamera
from google.cloud import storage
from datetime import datetime
from subprocess import call

picturesURI = "/home/pi/AppPyCharm/Pictures/"


def captureImage(currentTime, picturesURI):
    # Generate the picture's name
    pictureName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.jpg'
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


motionState = False
while True:
    motionState = p3Picam.motion()
    print(motionState)
    if motionState:
        currentTime = getTime()
        pictureName = captureImage(currentTime, picturesURI)
        timeStamp(currentTime, picturesURI, pictureName)

        client = storage.Client().from_service_account_json('/home/pi/AppPyCharm/appKey')
        bucket = client.get_bucket('iot-easv2019.appspot.com')
        zebraBlob = bucket.get_blob('pictureName')
        zebraBlob.upload_from_filename(filename='/%s%s' % (picturesURI, pictureName))


