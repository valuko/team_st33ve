from drive_controller import DriveController
from motor_controller import MotorController
from coordinates import Coordinates
from bolt_settings import BoltSettings
from referee_controller import RefereeController
from mainboard_controller import MainBoardController
import time
from datetime import datetime
import numpy as np
import cv2
import threading

cap = cv2.VideoCapture(1)
app_settings = BoltSettings()
val_dict = app_settings.read_dict()
motor_controller = MotorController()
serial_motor = motor_controller.get_motor()
drive_controller = DriveController(motor_controller)
coordinates = Coordinates(val_dict)
#referee_controller = RefereeController(motor_controller, val_dict)
main_controller = MainBoardController(serial_motor)

try:
    # Start the referee module
    td2 = threading.Thread(target=main_controller.detect_ball_catch)
    td2.start()

    while True:
        main_controller.ping()
        #main_controller.charge_kick()

        ret, frame = cap.read()
        coordinate_data = coordinates.get_coordinates(frame)

        if not main_controller.has_ball():
            print ("Ball not picked")
            # Drive to ball
            if coordinate_data['ball'] != -1:
                print ("Driving to ball coordinates",coordinate_data['ball'])
                drive_controller.drive_to_coordinates(coordinate_data['ball'])
                main_controller.dribbler_start()
            else:
                print ("Ball not found")

        if main_controller.has_ball():
            drive_controller.stop()
            print("has ball")
            drive_controller.around_ball(-5)
            #continue
            time.sleep(10)
            main_controller.dribbler_stop()
            break

        print ("Loop end")
        #cv2.imshow('Video', frame)
        key = cv2.waitKey(1)
        time.sleep(0.1)


except KeyboardInterrupt:
    #shutdown
    exit()

cap.release()