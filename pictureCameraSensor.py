import os
import picamera
import p3Picam
import storageFirebase
import cloudFirestore
from datetime import datetime
from subprocess import call

picturesURI = "/home/pi/AppPyCharm/Pictures/"
diskSpaceToReserve = 7.08 * 1024 * 1024 * 1024  # Keep 7Gb free on disk
filenamePrefix = "IOT"


def captureImage(currentTime, picturesURI):
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
def keepDiskSpaceFree(bytesToReserve, path):
    if getFreeSpace() < bytesToReserve:
        os.chdir(path)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        oldest = files[0]
        os.remove(oldest)
        storageFirebase.delete_blob(oldest)
        cloudFirestore.delete_cloud_firestore(oldest)
        print("File %s deleted to to avoid filling disk" % oldest)
        if getFreeSpace() > bytesToReserve:
            return


# Get available disk space at Raspberry Pi
def getFreeSpace():
    st = os.statvfs(picturesURI)
    du = st.f_bavail * st.f_frsize
    print("%i MB FREE" % ((du/1024)/1024))
    return du


motionState = False
while True:
    #Collecting the state of the camera sensor from P3Picam
    motionState = p3Picam.motion()

    print(motionState)
    if motionState:
        keepDiskSpaceFree(diskSpaceToReserve, picturesURI)
        #Collecting the current time
        currentTime = getTime()
        #Executing the captureImage where take the picture to be manipulated with timeStamp function
        pictureName, filePath = captureImage(currentTime, picturesURI)
        timeStamp(currentTime, filePath)
        # Upload to Firebase
        fileUrl = storageFirebase.upload_blob(pictureName, filePath)
        cloudFirestore.add_cloud_firestore(pictureName, fileUrl)



