import picamera
from time import sleep
from datetime import datetime
from subprocess import call

import p3Picam


def recordVideo(currentTime, videosURI):
    videoName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.h264'
    filePath = videosURI + videoName
    with picamera.PiCamera() as camera:
        # Start recording
        camera.start_recording(filePath)
        sleep(5)
        # Stop recording
        camera.stop_recording()
    return filePath


# The camera is now closed.
def getTime():
    # Fetch the current time
    currentTime = datetime.now()
    return currentTime


def videoConverter(filePath):
    filePathConverted = filePath.replace(".h264", ".MP4")

    print("We are going to convert the video.")
    # Define the command we want to execute.
    command = "MP4Box -add %s %s" % (filePath, filePathConverted)
    # Execute our command
    call([command], shell=True)
    # Video converted.
    print("Video converted.")


def main():
    videosURI = "/home/pi/AppPyCharm/Video/"
    while True:
        motionState = p3Picam.motion()
        print(motionState)
        if motionState:
            currentTime = getTime()
            filePath = recordVideo(currentTime, videosURI)
            videoConverter(filePath)


# Run the Program
if __name__ == "__main__":
    main()
