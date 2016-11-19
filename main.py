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
import serial

port = "/dev/ttyACM1"
#port = "COM6"
board_serial = serial.Serial(port, 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0)

cap = cv2.VideoCapture(0)
app_settings = BoltSettings()
val_dict = app_settings.read_dict()
motor_controller = MotorController(board_serial)
drive_controller = DriveController(motor_controller)
coordinates = Coordinates(val_dict)
#referee_controller = RefereeController(motor_controller, val_dict)
main_controller = MainBoardController(board_serial)

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
frame_read_tries = 3

STATE_CIRCLING = 'circling'
STATE_DRIVING = 'idle'
STATE_DRIVING_HOME = 'going_home'
STATE_TRAP_BALL = 'awaiting_ball'
STATE_DRIVING_STRAIGHT = 'stt'


def kick_action():
    print("About to kick")
    main_controller.kick()
    time.sleep(0.3)
    main_controller.release_kick()


try:
    # Start the referee module
    # td1 = threading.Thread(target=referee_controller.listen)
    # td2 = threading.Thread(target=main_controller.detect_ball_catch)
    # td1.start()
    # td2.start()

    while True:
        # if referee_controller.game_status():
        if True:
            # main_controller.ping()
            main_controller.pre_dribbler()
            time.sleep(3)
            #main_controller.dribbler_start()
            #time.sleep(2)
            print("game on")
            #main_controller.charge_kick()
            game_on = True

            while game_on:

                for i in range(3):
                    ret, frame = cap.read()

                #cv2.imshow('Video', frame)
                if not ret:
                    print "Frame not ready for reading"
                    continue

                coordinate_data = coordinates.get_coordinates(frame)
                print "\nCoordinates", coordinate_data['ball']

                if coordinate_data['ball'] != -1 or main_controller.has_ball() or current_state == STATE_DRIVING_STRAIGHT:
                    if main_controller.has_ball():
                        print("has ball")

                        if coordinate_data[opponent_goal_color] == -1:
                            print "Goal not found. Adjust"
                            drive_controller.around_ball(7)
                            continue

                        # Goal now found
                        opponent_goal_coordinates = coordinates.parse_goal_coordinates(coordinate_data)
                        if opponent_goal_coordinates == -1:
                            # Continue
                            drive_controller.around_ball(5)
                            print "Adjusting for goal"
                            continue

                        opponent_x = opponent_goal_coordinates[0]
                        width = opponent_goal_coordinates[2]

                        #if opponent_x < 350 - width / 4:
                        #    drive_controller.around_ball(2)
                        #elif opponent_x > 350 + width / 4:
                        #    drive_controller.around_ball(-2)
                        if width > 90.0:
                            print("facing!")
                            drive_controller.stop()
                            kick_action()
                            game_on = False
                            break
                        else:  # facing goal
                            print ("Not enough width", width)
                            drive_controller.around_ball(2)

                    if current_state == STATE_CIRCLING:
                        drive_controller.stop()
                        current_state = STATE_DRIVING
                    elif current_state == STATE_TRAP_BALL:
                        print "starting dribbler"
                        main_controller.dribbler_start()
                        time.sleep(2)
                        print("Waiting to catch ball")
                        #main_controller.detect_ball_catch()
                        #drive_controller.stop()
                    elif coordinate_data['ball'][1] >= 450 and coordinate_data['ball'][0] > 320:
                        motor_controller.move(20, -20, 0)
                        print "start dribbler"
                        main_controller.dribbler_start()
                        time.sleep(1)
                        print("Wait to catch ball")
                        main_controller.detect_ball_catch()
                        drive_controller.stop()
                        #exit()
                    else:
                        almost_at_ball = drive_controller.drive_to_coordinates(coordinate_data['ball'])
                        current_state = STATE_DRIVING
                    #time.sleep(1)
                    # main_controller.dribbler_start()
                        if almost_at_ball:
                            #current_state = STATE_DRIVING_STRAIGHT
                            print("Driving straight")
                        # activate dribbler

                        #main_controller.pre_dribbler()
                        #main_controller.dribbler_start()
                        #time.sleep(0.5)


                    # stop and look for the goal
                    #drive_controller.stop()

                else:
                    detect_attempts += 1
                    print "Ball not found on attempt:", detect_attempts
                    # Drive in circle till you find ball
                    if detect_attempts == circle_threshold:
                        # drive_controller.drive_in_circle(circle_speed)
                        current_state = "circling"
                        time.sleep(2)
                    # Drive to goal if after no ball still found after max_attempts, this will be a fail safe
                    if detect_attempts == max_attempts:
                        # drive_controller.drive_to_coordinates(coordinate_data['black'])
                        detect_attempts = 0
                        current_state = "going_home"
                        time.sleep(5)

                # print "Current state:", current_state

                # cv2.imshow('Video', frame)
                key = cv2.waitKey(1)
                #time.sleep(0.1)

            break

except KeyboardInterrupt:
    # shutdown
    drive_controller.stop()
    time.sleep(0.5)
    main_controller.dribbler_stop()
    exit()

cap.release()
