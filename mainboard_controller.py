import serial
from datetime import datetime


class MainBoardController:
    def __init__(self):
        self.is_ball = False

    def has_ball(self):
        return self.is_ball
