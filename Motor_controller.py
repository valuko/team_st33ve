mainboard=''

import time
from datetime import datetime

class Motor:
    def __init__(self,mainboard):
        self.mainboard=mainboard

    def movetoball(self, balldetails):

        self.mainboard.dribbler_on()

        if balldetails[0] > 340:
            self.mainboard.turnleft()
        elif balldetails[0] < 290:
            self.mainboard.turnright()
        elif (balldetails[0] > 290 and balldetails[0] < 350):
            self.mainboard.backwheel(0)
            self.mainboard.forwardspeed()