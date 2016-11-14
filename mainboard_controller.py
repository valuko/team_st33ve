import serial
from datetime import datetime


class MainBoardController:
    port = "COM5"
    baud_rate = 9600
    ball_catch_cmd = "<bl:1>"
    ball_release_cmd = "<bl:0>"

    def __init__(self):
        self.mainboard = serial.Serial(self.port, self.baud_rate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 3)
        self.is_ball = False

    def has_ball(self):
        return self.is_ball

    def dribbler_state(self):
        self.mainboard.write("d700\n")

    def dribbler_stop(self):
        self.mainboard.write("d0\n")

    def charge(self):
        print(str(datetime.now()) + " | charge")
        self.mainboard.write("j\n")

    def kick(self):
        print(str(datetime.now()) + " | kick")
        self.mainboard.write("k\n")

    def detect_ball_catch(self):
        self.is_ball = False
        while True:
            line = self.mainboard.readline().strip()
            if line == self.ball_catch_cmd:
                self.is_ball = True
            if line == self.ball_release_cmd:
                self.is_ball = False

