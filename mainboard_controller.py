import serial
import time
from datetime import datetime


class MainBoardController:
    port = "COM5"
    baud_rate = 9600
    ball_catch_cmd = "<bl:1>"
    ball_release_cmd = "<bl:0>"
    dribbler_prefix = 'd'

    def __init__(self, boarder):
        self.mainboard = boarder
        self.is_ball = False

    def has_ball(self):
        return self.is_ball

    def ping(self):
        self.mainboard.write("p\n")

    def pre_dribbler(self):
        pf = self.dribbler_prefix
        self.mainboard.write(pf+"0.1\n")

    def dribbler_start(self):
        pf = self.dribbler_prefix
        #self.mainboard.write(pf+"0.1\n")
        #time.sleep(3)
        self.mainboard.write(pf+"6\n")

    def dribbler_stop(self):
        pf = self.dribbler_prefix
        self.mainboard.write(pf+"0\n")

    def charge_kick(self):
        print(str(datetime.now()) + " | charge")
        self.mainboard.write("n\n")

    def kick(self):
        print(str(datetime.now()) + " | kick")
        self.mainboard.write("j\n")

    def release_kick(self):
        print(str(datetime.now()) + " | release_kick")
        self.mainboard.write("k\n")

    def detect_ball_catch(self):
        self.is_ball = False
        start = datetime.now()
        while True:
            #print ("Reading IR...")
            delta = datetime.now() - start
            line = self.mainboard.readline().strip()
            if line == self.ball_catch_cmd or delta.seconds > 3:
                self.is_ball = True
                break
            if line == self.ball_release_cmd:
                self.is_ball = False

