__author__ = 'Ikechukwu Ofodile -- ikechukwu.ofodile@estcube.eu'

import cv2
import numpy as np
import math
import serial
import time
from time import sleep

from Detect import Detector as Detect
from Motor_controller import Motor
from Mainboard_Commands import MainboardController
mainboard = MainboardController()
motor = Motor(mainboard)

camera = cv2.VideoCapture(0)
detect = Detect()
ballseen = False
state = "ballseen"


#mainboard.dribbler_on()

while True:
    (frameready, frame) = camera.read()
    if frameready:
        balldetails = detect.ball_coordinates(frame)

        if balldetails == [0,0,0]:
            mainboard.motor_shut_down()


        else:
            ballseen = True
            mainboard.dribbler_init()
            print ('ball seen')
            motor.movetoball(balldetails)
            print('moving to ball')

            # sleep(0.05)
            # mainboard.circlearound()





    keypress = cv2.waitKey(50) & 0xFF
    if keypress == 27:
        camera.release()
        mainboard.motor_shut_down()
        mainboard.dribbler_shut_down()
        cv2.destroyAllWindows()
        break