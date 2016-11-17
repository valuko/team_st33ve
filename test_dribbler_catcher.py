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
drive_controller = DriveController(motor_controller)
coordinates = Coordinates(val_dict)
referee_controller = RefereeController(motor_controller, val_dict)
main_controller = MainBoardController()

try:
    # Start the referee module
    td2 = threading.Thread(target=main_controller.detect_ball_catch)
    td2.start()

    while True:
        main_controller.ping()
        main_controller.dribbler_start()
        main_controller.charge_kick()

        ret, frame = cap.read()
        coordinate_data = coordinates.get_coordinates(frame)

        while not main_controller.has_ball():
            print ("Ball not found")
            # Drive to ball
            if coordinate_data['ball'] != -1:
                drive_controller.drive_to_coordinates(coordinate_data['ball'])

        if main_controller.has_ball():
            drive_controller.stop()
            print("has ball")
            drive_controller.around_ball(-5)
            #continue
            time.sleep(10)
            main_controller.dribbler_stop()
            break


except KeyboardInterrupt:
    #shutdown
    exit()

cap.release()