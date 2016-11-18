from drive_controller import DriveController
from motor_controller import MotorController
from coordinates import Coordinates
from bolt_settings import BoltSettings
from mainboard_controller import MainBoardController
import time
from datetime import datetime
import numpy as np
import cv2
import serial

#port = "/dev/ttyACM1"
port = "COM6"
board_serial = serial.Serial(port, 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0)

cap = cv2.VideoCapture(1)
app_settings = BoltSettings()
val_dict = app_settings.read_dict()
motor_controller = MotorController(board_serial)
drive_controller = DriveController(motor_controller)
coordinates = Coordinates(val_dict)
main_controller = MainBoardController(board_serial)

own_goal_color = val_dict['own_goal_color']

opponent_goal_color = val_dict['opponent_goal_color']


def kick_action():
    print("About to kick")
    main_controller.kick()
    time.sleep(1)
    main_controller.release_kick()

try:
    main_controller.pre_dribbler()
    time.sleep(3)
    main_controller.dribbler_start()
    time.sleep(3)
    #exit()
    #main_controller.charge_kick()

    while True:
        for i in range(3):
            ret, frame = cap.read()

        # cv2.imshow('Video', frame)
        if not ret:
            print "Frame not ready for reading"
            continue

        coordinate_data = coordinates.get_coordinates(frame)
        print "\nCoordinates", coordinate_data

        if coordinate_data[opponent_goal_color] == -1:
            print "Goal not found. Adjust"
            #drive_controller.around_ball(7)
            drive_controller.drive_in_circle()
            continue

        # Goal now found
        opponent_goal_coordinates = coordinates.parse_goal_coordinates(coordinate_data)
        if opponent_goal_coordinates == -1:
            # Continue
            print "Adjusting further for goal"
            drive_controller.around_ball(7)
            continue

        opponent_x = opponent_goal_coordinates[0]
        width = opponent_goal_coordinates[2]

        if width > 90.0:
            print("facing!")
            #drive_controller.stop()
            drive_controller.around_ball(0)
            main_controller.dribbler_start()
            time.sleep(0.5)
            kick_action()
            exit()
        else:
            print ("Not enough width", width)
            drive_controller.around_ball(2)


        #if opponent_x < 350 - width / 4:
        #    print ("Too much width", width)
        #    drive_controller.around_ball(-1.5)
        #elif opponent_x > 350 + width / 4:
        #    print ("Too little width", width)
        #    drive_controller.around_ball(1.5)
        #else:  # facing goal
        #    print("facing!")
        #    drive_controller.stop()
        #    break

except KeyboardInterrupt:
    # shutdown
    drive_controller.stop()

cap.release()