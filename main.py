from drive_controller import DriveController
from motor_controller import MotorController
from coordinates import Coordinates
from bolt_settings import BoltSettings
import time
import numpy as np
import cv2

cap = cv2.VideoCapture(1)
app_settings = BoltSettings()
val_dict = app_settings.read_dict()
motor_controller = MotorController()
drive_controller = DriveController(motor_controller)
coordinates = Coordinates(val_dict)

input_key = ""
current_state = "static"
detect_attempts = 0
circle_speed = 10
max_attempts = 15
circle_threshold = 3

while True:
    try:
        ret, frame = cap.read()

        if not ret:
            print "Frame not ready for readying"
            continue

        ball_found = input_key == "b"
        coordinate_data = coordinates.get_coordinates(frame)
        print "\nCoordinates", coordinate_data

        if coordinate_data['ball'] != -1:
            # Stop first if its circling to avoid sudden jerked movement
            # if current_state == "circling":
            # drive_controller.stop()

            detect_attempts = 0
            drive_controller.drive_to_coordinates(coordinate_data['ball'])
            current_state = "driving"
        else:
            detect_attempts += 1
            print "Ball not found on attempt:", detect_attempts
            # Drive in circle till you find ball
            if detect_attempts == circle_threshold:
                drive_controller.drive_in_circle(circle_speed)
                current_state = "circling"

            # Drive to goal if after no ball still found after max_attempts, this will be a fail safe
            if detect_attempts == max_attempts:
                drive_controller.drive_to_coordinates(coordinate_data['black'])
                detect_attempts = 0
                current_state = "going_home"

        print "Current state:", current_state
        time.sleep(1)

        cv2.imshow('Video', frame)
        key = cv2.waitKey(1)
        time.sleep(1)
    except KeyboardInterrupt:
        break

cap.release()
