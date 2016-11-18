import time


class DriveController:
    current_vals = ""
    motor_controller = ""

    def __init__(self, motor_controller):
        self.motor_controller = motor_controller

    def drive_to_coordinates(self, coordinates):

        print "Driving to coordinates",coordinates

        if coordinates == -1:
            return

        x = coordinates[0]
        y = coordinates[1]

        #actualX = 320 - x

        # the closer the ball the smaller the speed
        if y < 150:
            speed = 20
        elif y > 500:
            speed = 70
        else:
            speed = 50

        if x > 340:
            # print("move right")
            ls = speed + 8
            rs = (speed - 8) * -1
            bs = 8
            self.motor_controller.move(ls, rs, bs)
        elif x < 310:
            # print("move left")
            ls = speed - 8
            rs = (speed - 8) * -1
            bs = 8
            self.motor_controller.move(ls, rs, bs)
        else:
            # print("move straight")
            rs = speed + 20
            ls = (speed + 20) * -1
            bs = 0
            self.motor_controller.move(ls, rs, bs)

    def drive_in_circle(self, multiplier=1):
        circle_speed = 14 * multiplier
        print "Driving round in circle now at speed:", circle_speed
        self.motor_controller.circlearound(circle_speed)
        time.sleep(0.1)

    def around_ball(self, multiplier=1):
        self.motor_controller.move_back_wheel(10 * multiplier)

    def stop(self):
        print "Stopping now"
        self.motor_controller.stop()

    def pause(self):
        print "Pausing now..."
        time.sleep(0.1)
