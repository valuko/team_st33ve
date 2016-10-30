from drive_controller import DriveController
from motor_controller import MotorController
from coordinates import Coordinates


motor_controller = MotorController()
drive_controller = DriveController()
coordinates = Coordinates()

input_key = ""
current_state = "static"

while input_key != "q":
    ball_found = input_key == "b"
    coordinate_data = coordinates.get_coordinates(ball_found)
    print "Coordinates",coordinate_data
    if coordinate_data['ball'] != -1:
        current_state = "driving"
        drive_controller.drive_to_coordinates(coordinate_data['ball'])

    print "Current state:",current_state
    input_key = raw_input("Enter q to break, b to detect ball: ")
