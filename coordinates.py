import numpy as np
import cv2
from bolt_settings import BoltSettings


class Coordinates:
    cam_num = 1

    def __init__(self, values_dict):
        #app_settings = BoltSettings()
        #self.values_dict = app_settings.read_dict()
        #self.cap = cap
        self.values_dict = values_dict

    def parse_goal_coordinates(self, coordinates):
        opponent_goal_coord = coordinates[self.values_dict["opponent_goal_color"]]
        own_goal_coord = coordinates[self.values_dict["own_goal_color"]]

        if own_goal_coord != -1 and opponent_goal_coord != -1:
            self_x = own_goal_coord[0]
            opponent_x = opponent_goal_coord[0]

            if opponent_x + 10 > self_x > 10 - opponent_x:  # The colours are of a robot not of a gate
                opponent_goal_coord = -1

        return opponent_goal_coord

    def get_coordinates(self, frame):
        coordinates_dict = {"ball": -1, "blue": -1, "yellow": -1, "black": -1}

        colours = ["black", "blue", "yellow", "ball"]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for i in range(4):
            colour = colours[i]
            h_low = int(self.values_dict['H_low_' + colour])
            h_top = int(self.values_dict['H_high_' + colour])
            s_low = int(self.values_dict['S_low_' + colour])
            s_top = int(self.values_dict['S_high_' + colour])
            v_low = int(self.values_dict['V_low_' + colour])
            v_top = int(self.values_dict['V_high_' + colour])

            # masking
            lower_colour = np.array([h_low, s_low, v_low])
            upper_colour = np.array([h_top, s_top, v_top])
            mask = cv2.inRange(hsv, lower_colour, upper_colour)

            kernel = np.ones((5, 5), np.uint8)

            mask = cv2.erode(mask, kernel, iterations=2)
            # combining smaller blobs
            mask = cv2.dilate(mask, kernel, iterations=2)

            # Detect blobs.
            _, contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # Getting the biggest blob's coordinates (that is probably the closest object)
            biggest_area = 0
            coordinates = -1
            if len(contours) > 0:
                for cnt in contours:
                    # width = cv2.contourArea(cnt)
                    rect = cv2.minAreaRect(cnt)
                    width = rect[1][0]
                    height = rect[1][1]
                    area = width * height

                    if width < 5 and (colour == "yellow" or colour == "blue"):
                        continue

                    if area > biggest_area:
                        moment = cv2.moments(cnt)
                        try:
                            cx = int(moment['m10'] / moment['m00'])
                            cy = int(moment['m01'] / moment['m00'])
                        except ZeroDivisionError:
                            print("zero division")
                            continue
                        biggest_area = area
                        if colour == "ball":
                            black = coordinates_dict["black"]
                            # print("black: " + str(black))
                            # print("ball: " + str(cx) + ", " + str(cy))
                            if black != -1:
                                black_x = black[0]
                                black_y = black[1]
                                black_width = black[2]
                                if black_y > cy and black_x + black_width / 2 > cx > black_width / 2 - black_x:  # ball is out of the field
                                    print("ball out of field")
                                    continue

                        coordinates = (cx, cy, width, height)
                coordinates_dict[colour] = coordinates

                # cv2.imshow('Video', frame)
        #key = cv2.waitKey(1)

        return coordinates_dict

        '''
        if should_pass:
            coordinates_dict = {"ball": [23, 25, 256.34, 234.56],
                                "blue": [23, 25, 256.34, 234.56],
                                "yellow": [23, 25, 256.34, 234.56],
                                "black": [23, 25, 256.34, 234.56]}
        else:
            coordinates_dict = {"ball": -1, "blue": -1, "yellow": -1, "black": -1}
        '''
