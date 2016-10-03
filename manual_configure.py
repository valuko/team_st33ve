import numpy as np
from settings import UserSettings
import cv2

def nothing(x):
    pass

tag = "ball"
#tag = "own_goal"
#tag = "opp_goal"
#tag = "ref"
user_settings = UserSettings()
settingsDict = user_settings.read_json_settings(tag)
if (not settingsDict):
    settingsDict = {'h_high': 0, 'h_low': 0, 's_high': 0, 's_low': 0, 'v_high': 0, 'v_low': 0}

cap = cv2.VideoCapture(0)

# Define the config window
cv2.namedWindow('configure')
cv2.createTrackbar('h_low','configure',int(settingsDict['h_low']),255,nothing)
cv2.createTrackbar('h_high','configure',int(settingsDict['h_high']),255,nothing)
cv2.createTrackbar('s_low','configure',int(settingsDict['s_low']),255,nothing)
cv2.createTrackbar('s_high','configure',int(settingsDict['s_high']),255,nothing)
cv2.createTrackbar('v_low','configure',int(settingsDict['v_low']),255,nothing)
cv2.createTrackbar('v_high','configure',int(settingsDict['v_high']),255,nothing)

kernel = np.ones((10, 10), np.uint8)
mark_color = (0,165,255)

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    H_low = cv2.getTrackbarPos('h_low', 'configure')
    H_high = cv2.getTrackbarPos('h_high', 'configure')
    S_low = cv2.getTrackbarPos('s_low', 'configure')
    S_high = cv2.getTrackbarPos('s_high', 'configure')
    V_low = cv2.getTrackbarPos('v_low', 'configure')
    V_high = cv2.getTrackbarPos('v_high', 'configure')

    lower = np.array([H_low, S_low, V_low])
    upper = np.array([H_high, S_high, V_high])

    mask = cv2.inRange(hsv, lower, upper)

    mask = cv2.erode(mask, kernel, iterations=2)
    dilation = cv2.dilate(mask, kernel, iterations=2)
    res = cv2.bitwise_and(frame, frame, mask=dilation)
    blur = cv2.GaussianBlur(res, (15, 15), 0)


    _, contours, _ = cv2.findContours(dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        #cnt = contours[0]
        cnt = max(contours, key=cv2.contourArea)
        mmt = cv2.moments(cnt)
        rect = cv2.minAreaRect(cnt)
        try:
            cx = int(mmt['m10']/mmt['m00'])
            cy = int(mmt['m01']/mmt['m00'])
        except ZeroDivisionError:
            print("error: divided by zero")
            continue

        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        #cv2.drawContours(res, contours, -1, (0,255,255), 1)
        cv2.circle(frame, center, int(radius), mark_color, 2)

    cv2.imshow('Output', frame)
    cv2.imshow('configure', res)
    #cv2.imshow('Gaussian Blurring', blur)

    key = cv2.waitKey(1)

    if key & 0xFF == 27:
        break

    if key & 0xFF == ord('q'):
        user_settings.save_json_settings({
            'h_low': H_low, 's_low': S_low, 'v_low': V_low,
            'h_high': H_high, 's_high': S_high, 'v_high': V_high
        }, tag)
        break


cap.release()
cv2.destroyAllWindows()