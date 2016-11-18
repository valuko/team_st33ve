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

#port = "/dev/ttyACM1"
port = "COM7"
board_serial = serial.Serial(port, 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=0)

cap = cv2.VideoCapture(1)
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

main_controller.pre_dribbler()
time.sleep(3)
print ("Scanning for ball")
main_controller.dribbler_start()
time.sleep(0.5)

motor_controller.move(70, -70, 0)

main_controller.detect_ball_catch()
print ("ball found")
main_controller.charge_kick()
time.sleep(2)
main_controller.dribbler_stop()

time.sleep(1)
main_controller.kick()
time.sleep(1)
main_controller.release_kick()

