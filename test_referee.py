from referee_controller import RefereeController
from motor_controller import MotorController
from bolt_settings import BoltSettings
import time


app_settings = BoltSettings()
val_dict = app_settings.read_dict()

motor_controller = MotorController()
referee = RefereeController(motor_controller, val_dict, game_status=True)

# Listen for input
try:
    print "Listening for input now..."
    referee.listen()
except KeyboardInterrupt:
    print "shutting down now"