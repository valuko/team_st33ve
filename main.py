from drive_controller import DriveController
from motor_controller import MotorController
from coordinates import Coordinates


motor_controller = MotorController()
drive_controller = DriveController()
coordinates = Coordinates()

coordinate_data = coordinates.get_coordinates()
print "Coordinates ",coordinate_data
