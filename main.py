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

input_key = ""
current_state = "idle"
ball_found = False
detect_attempts = 0
circle_speed = 10
max_attempts = 15
circle_threshold = 3
command = ""
own_goal_color = val_dict['own_goal_color']
opponent_goal_color = val_dict['opponent_goal_color']
game_on = False

STATE_CIRCLING = 'circling'
STATE_DRIVING = 'idle'
STATE_DRIVING_HOME = 'going_home'


def kick_action():
    print("About to kick")
    main_controller.kick()
    time.sleep(0.3)
    main_controller.release_kick()


try:
    # Start the referee module
    td1 = threading.Thread(target=referee_controller.listen)
    td2 = threading.Thread(target=main_controller.detect_ball_catch)
    td1.start()
    td2.start()

    while True:
        if referee_controller.game_status():
            main_controller.ping()
            main_controller.dribbler_start()
            main_controller.charge_kick()
            game_on = True

            while game_on:

                ret, frame = cap.read()

                if not ret:
                    print "Frame not ready for reading"
                    continue

                coordinate_data = coordinates.get_coordinates(frame)
                print "\nCoordinates", coordinate_data

                if coordinate_data['ball'] != -1 or main_controller.has_ball():
                    if main_controller.has_ball():
                        print("has ball")
                        if coordinate_data[opponent_goal_color] == -1:
                            drive_controller.around_ball(-5)
                            continue

                        # Goal now found
                        opponent_goal_coordinates = coordinates.parse_goal_coordinates(coordinate_data)
                        if opponent_goal_coordinates == -1:
                            # Continue
                            drive_controller.around_ball(-5)
                            continue

                        opponent_x = opponent_goal_coordinates[0]
                        width = opponent_goal_coordinates[2]

                        if opponent_x < 350 - width / 4:
                            drive_controller.around_ball(2)
                        elif opponent_x > 350 + width / 4:
                            drive_controller.around_ball(-2)
                        else:  # facing goal
                            print("facing!")
                            drive_controller.stop()
                            kick_action()
                            game_on = False
                            break

                    if current_state == STATE_CIRCLING:
                        drive_controller.stop()

                    current_state = STATE_DRIVING

                    # Drive to ball now
                    drive_controller.drive_to_coordinates(coordinate_data['ball'])

                    # Sleep until you have the ball
                    while not main_controller.has_ball():
                        print("Ball not yet found")
                        continue

                    # stop and look for the goal
                    drive_controller.stop()

                else:
                    detect_attempts += 1
                    print "Ball not found on attempt:", detect_attempts
                    # Drive in circle till you find ball
                    if detect_attempts == circle_threshold:
                        drive_controller.drive_in_circle(circle_speed)
                        current_state = "circling"
                        time.sleep(2)
                    # Drive to goal if after no ball still found after max_attempts, this will be a fail safe
                    if detect_attempts == max_attempts:
                        drive_controller.drive_to_coordinates(coordinate_data['black'])
                        detect_attempts = 0
                        current_state = "going_home"
                        time.sleep(5)

                #print "Current state:", current_state

                # cv2.imshow('Video', frame)
                key = cv2.waitKey(1)
                time.sleep(0.1)

except KeyboardInterrupt:
    #shutdown
    exit()

cap.release()
