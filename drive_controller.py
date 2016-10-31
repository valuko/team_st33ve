import time


class DriveController:
    def __init__(self, motor_controller):
        self.motor_controller = motor_controller

    def drive_to_coordinates(self, coordinates):

        print "Driving to coordinates",coordinates

        if coordinates == -1:
            return

        x = coordinates[0]
        y = coordinates[1]

        # the closer the ball the smaller the speed
        if y < 150:
            speed = 70
        elif y > 500:
            speed = 20
        else:
            speed = 40

        if x > 340:
            # print("move right")
            self.motor_controller.move_left_wheel((speed + 8) * -1)
            self.motor_controller.move_right_wheel(speed - 8)
            self.motor_controller.move_back_wheel(8)
        elif x < 310:
            # print("move left")
            self.motor_controller.move_right_wheel(speed + 8)
            self.motor_controller.move_left_wheel((speed - 8) * -1)
            self.motor_controller.move_back_wheel(8)
        else:
            # print("move straght")
            self.motor_controller.move_right_wheel(speed + 20)
            self.motor_controller.move_left_wheel((speed + 20) * -1)

    def drive_in_circle(self, multiplier=1):
        circle_speed = 14 * multiplier
        print "Driving round in circle now at speed:", circle_speed
        self.motor_controller.move_left_wheel(circle_speed)
        self.motor_controller.move_right_wheel(circle_speed)
        self.motor_controller.move_back_wheel(circle_speed)

    def stop(self):
        print "Stopping now"
        self.motor_controller.stop()



