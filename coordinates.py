import numpy as np
import cv2
from bolt_settings import BoltSettings


class Coordinates:
    def __init__(self):
        pass

    @staticmethod
    def get_coordinates():
        coordinates_dict = {"ball": -1, "blue": -1, "yellow": -1, "black": -1}
        return coordinates_dict

