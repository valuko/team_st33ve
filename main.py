from drive_controller import DriveController
from motor_controller import MotorController
from coordinates import Coordinates


motor_controller = MotorController()
drive_controller = DriveController()
coordinates = Coordinates()

input_key = ""
current_state = "static"
detect_attempts = 0

while input_key != "q":
    ball_found = input_key == "b"
    coordinate_data = coordinates.get_coordinates(ball_found)
    print "\nCoordinates",coordinate_data

    if coordinate_data['ball'] != -1:
        current_state = "driving"
        detect_attempts = 0
        drive_controller.drive_to_coordinates(coordinate_data['ball'])
    else:
        detect_attempts += 1
        print "Ball not found on attempt:",detect_attempts

    print "Current state:",current_state
    input_key = raw_input("Enter q to break, b to detect ball: ")
