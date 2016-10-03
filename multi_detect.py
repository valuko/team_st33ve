import numpy as np
from settings import UserSettings
import cv2

def nothing(x):
    pass

tags = ['ball', 'own_goal', 'ref']
tag_coordinates = {'ball': -1, 'own_goal': -1, 'ref': -1}

marking_colours = {'ball': (0, 165, 255), 'own_goal': (0, 255, 0), 'ref': (0, 0, 255)}
kernel = np.ones((5, 5), np.uint8)

user_settings = UserSettings()
settings = user_settings.read_json_settings()

cap = cv2.VideoCapture(0)

kernel = np.ones((5, 5), np.uint8)

minimumWidth = 5

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for i in range(3):
        current_tag = tags[i]

        tag_settings = settings[current_tag]
        lower_range = [tag_settings['h_low'], tag_settings['s_low'], tag_settings['v_low']]
        upper_range = [tag_settings['h_high'], tag_settings['s_high'], tag_settings['v_high']]

        mask = cv2.inRange(hsv, np.array(lower_range), np.array(upper_range))

        mask = cv2.erode(mask, kernel, iterations=2)
        dilation = cv2.dilate(mask, kernel, iterations=2)

        _, contours, _ = cv2.findContours(dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        biggest_area = 0
        coordinates = -1
        for cnt in contours:
            cnt = max(contours, key=cv2.contourArea)
            mmt = cv2.moments(cnt)
            rectangle = cv2.minAreaRect(cnt)
            width = rectangle[1][0]
            height = rectangle[1][1]

            try:
                cx = int(mmt['m10'] / mmt['m00'])
                cy = int(mmt['m01'] / mmt['m00'])
            except ZeroDivisionError:
                print("error: divided by zero")
                continue

            if current_tag == 'ball':

                (x, y), radius = cv2.minEnclosingCircle(cnt)
                center = (int(x), int(y))
                # cv2.drawContours(res, contours, -1, (0,255,255), 1)
                cv2.circle(frame, center, int(radius), marking_colours[current_tag], 2)
                coordinates = (cx, cy, width, height)
            else:
                area = width * height

                if width < minimumWidth and (current_tag == "opp_goal" or current_tag == "own_goal"):
                    continue

                #box = cv2.boxPoints(rectangle)
                #box = np.int0(box)
                #cv2.drawContours(frame, [box], 0, marking_colours[current_tag], 2)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), marking_colours[current_tag], 2)
                biggest_area = area
                coordinates = (cx, cy, width, height)

    # tag_coordinates[current_tag] = coordinates
    # Save the coordinates at this point

    cv2.imshow('Output', frame)

    key = cv2.waitKey(1)

    if key & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
