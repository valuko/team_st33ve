import serial
import time


class MotorController:
    right_wheel = "1"
    left_wheel = "3"
    back_wheel = "2"
    speed_cmd = ':sd'
    baud_rate = 9600
    port = "COM7"

    def __init__(self):
        #self.baud_rate = 9600
        self.motor = serial.Serial(self.port, self.baud_rate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)  # , writeTimeout=0)

    # The ids for right, left and back wheel controllers are 1, 2 and 3 respectively
    def move_right_wheel(self, speed=40):
        self.motor.write(self.right_wheel + self.speed_cmd + str(speed) + '\n')
        time.sleep(0.1)

    def move_left_wheel(self, speed=40):
        self.motor.write(self.left_wheel + self.speed_cmd + str(speed) + '\n')
        time.sleep(0.1)


    def move_back_wheel(self, speed=40):
        self.motor.write(self.back_wheel + self.speed_cmd + str(speed) + '\n')
        time.sleep(0.1)


    def stop(self):
        stop_speed = "0"
        self.motor.write(self.right_wheel + self.speed_cmd + stop_speed + '\n')
        time.sleep(0.1)
        self.motor.write(self.left_wheel + self.speed_cmd + stop_speed + '\n')
        time.sleep(0.1)
        self.motor.write(self.back_wheel + self.speed_cmd + stop_speed + '\n')

