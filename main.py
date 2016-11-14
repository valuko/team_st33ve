from drive_controller import DriveController
from motor_controller import MotorController
from coordinates import Coordinates
from bolt_settings import BoltSettings
from referee_controller import RefereeController
import time
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

input_key = ""
current_state = "static"
detect_attempts = 0
circle_speed = 10
max_attempts = 15
circle_threshold = 3
command = ""

try:
    # Start the referee module
    td1 = threading.Thread(target=referee_controller.listen)
    td1.start()

    while True:
        if referee_controller.game_status():
            ret, frame = cap.read()

            if not ret:
                print "Frame not ready for readying"
                continue

            ball_found = input_key == "b"
            coordinate_data = coordinates.get_coordinates(frame)
            print "\nCoordinates", coordinate_data

            if coordinate_data['ball'] != -1:
                # Stop first if its circling to avoid sudden jerked movement
                if current_state == "circling":
                    drive_controller.stop()

                detect_attempts = 0
                command = "drivetoball"
                current_state = "driving"
            else:
                detect_attempts += 1
                print "Ball not found on attempt:", detect_attempts
                # Drive in circle till you find ball
                if detect_attempts == circle_threshold:
                    command = "circle"
                    current_state = "circling"
                # Drive to goal if after no ball still found after max_attempts, this will be a fail safe
                if detect_attempts == max_attempts:
                    command = "gohome"
                    detect_attempts = 0
                    current_state = "going_home"

            print "Current state:", current_state

            if command == "circle":
                drive_controller.drive_in_circle(circle_speed)
            elif command == "drivetoball":
                drive_controller.drive_to_coordinates(coordinate_data['ball'])
            elif command == "gohome":
                drive_controller.drive_to_coordinates(coordinate_data['black'])

            # cv2.imshow('Video', frame)
            key = cv2.waitKey(1)
            time.sleep(0.1)

except KeyboardInterrupt:
    #shutdown
    exit()

cap.release()
