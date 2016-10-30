import time


class DriveController:
    def __init__(self):
        pass

    @staticmethod
    def drive_to_coordinates(coordinate_set):
        target_coordinates = coordinate_set
        print "Driving to coordinates",target_coordinates
        return True

    @staticmethod
    def drive_in_circle(speed):
        circle_speed = speed
        print "Driving round in circle now at speed:",circle_speed
        return True

    @staticmethod
    def stop():
        print "Stopping now"
        return True


