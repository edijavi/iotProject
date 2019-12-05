import picamera
from time import sleep
from subprocess import call

# Setup the camera
with picamera.PiCamera() as camera:
    # Start recording
    camera.start_recording("/home/pi/AppPyCharm/Video/pythonVideo.h264")
    sleep(5)
    # Stop recording
    camera.stop_recording()

# The camera is now closed.

print("We are going to convert the video.")
# Define the command we want to execute.
command = " MP4Box -add /home/pi/AppPyCharm/Video/pythonVideo.h264 /home/pi/AppPyCharm/Video/convertedVideo.mp4 "
# Execute our command
call([command], shell=True)
# Video converted.
print("Video converted.")
