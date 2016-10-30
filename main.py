from drive_controller import DriveController
from motor_controller import MotorController
from coordinates import Coordinates


motor_controller = MotorController()
drive_controller = DriveController()
coordinates = Coordinates()

input_key = ""

while input_key != "q":
    ball_found = input_key == "b"
    coordinate_data = coordinates.get_coordinates(ball_found)
    print "Coordinates",coordinate_data
    input_key = raw_input("Enter q to break, b to detect ball: ")