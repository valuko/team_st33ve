import numpy as np
import cv2
from bolt_settings import BoltSettings


class Coordinates:
    def __init__(self):
        pass

    @staticmethod
    def get_coordinates(should_pass):
        if should_pass:
            coordinates_dict = {"ball": [23, 25, 256.34, 234.56],
                                "blue": [23, 25, 256.34, 234.56],
                                "yellow": [23, 25, 256.34, 234.56],
                                "black": [23, 25, 256.34, 234.56]}
        else:
            coordinates_dict = {"ball": -1, "blue": -1, "yellow": -1, "black": -1}
        return coordinates_dict

