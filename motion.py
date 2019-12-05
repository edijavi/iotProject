# Project 13 - Burglar Detector With Photo Capture
# latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
# project updates at: https://nostarch.com/RaspberryPiProject
# import the necessary packages
import exit as exit
import sys
from gpiozero import Button
from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
from time import sleep
from signal import pause

# create objects that refer to a button,
# a motion sensor and the PiCamera
button = Button(2)
pir = MotionSensor(4)
camera = PiCamera()

# start the camera
camera.rotation = 180
camera.start_preview()

# image image names
i = 0


# take photo when motion is detected
def take_photo():
    global i
    i = i + 1
    timestamp = datetime.now().isoformat()
    camera.capture('/home/pi/Desktop/Pictures/image_%s_%s.jpg' % (i, timestamp))
    print('A photo has been taken')
    sleep(10)


# stop the camera when the pushbutton is pressed
def stop_camera():
    camera.stop_preview()
    # exit the program
    exit()


# assign a function that runs when motion is detected
pir.when_motion = take_photo

# assign a function that runs when the button is pressed
button.when_pressed = stop_camera

pause()
