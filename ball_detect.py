import numpy as np
from settings import UserSettings
import cv2

# Load Global Settings
user_settings = UserSettings()
settingsDict = user_settings.read_settings()
opg = "ball"


def nothing(x):
    pass


cap = cv2.VideoCapture(0)

cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H_low','image',int(settingsDict['H_low_' + opg]),255,nothing)
cv2.createTrackbar('H_high','image',int(settingsDict['H_high_' + opg]),255,nothing)
cv2.createTrackbar('S_low','image',int(settingsDict['S_low_' + opg]),255,nothing)
cv2.createTrackbar('S_high','image',int(settingsDict['S_high_' + opg]),255,nothing)
cv2.createTrackbar('V_low','image',int(settingsDict['V_low_' + opg]),255,nothing)
cv2.createTrackbar('V_high','image',int(settingsDict['V_high_' + opg]),255,nothing)

#cv2.resizeWindow("image", 600, 300)

kernel = np.ones((5, 5), np.uint8)

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    H_low = cv2.getTrackbarPos('H_low', 'image')
    H_high = cv2.getTrackbarPos('H_high', 'image')
    S_low = cv2.getTrackbarPos('S_low', 'image')
    S_high = cv2.getTrackbarPos('S_high', 'image')
    V_low = cv2.getTrackbarPos('V_low', 'image')
    V_high = cv2.getTrackbarPos('V_high', 'image')

    lower = np.array([H_low, S_low, V_low])
    upper = np.array([H_high, S_high, V_high])

    mask = cv2.inRange(hsv, lower, upper)

    # making edges of the two different colours to be less fuzzy
    mask = cv2.erode(mask, kernel, iterations=2)
    dilation = cv2.dilate(mask, kernel, iterations=2)
    res = cv2.bitwise_and(frame, frame, mask=dilation)

    # Detect blobs.
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
            # print("error: divided by zero")
            continue

        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (0,165,255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

    cv2.imshow('Video', frame)
    #cv2.imshow('mask', mask)
    cv2.imshow('image', dilation)
    #cv2.drawContours(res, contours, -1, (0,255,255), 2)
    cv2.imshow('result', res)

    key = cv2.waitKey(1)

    if key & 0xFF == 27:
        break

    if key & 0xFF == ord('q'):
        hsvDict = {'H_low_'+opg : H_low, 'S_low_'+opg: S_low, 'V_low_'+opg: V_low,
                   'H_high_' + opg: H_high, 'S_high_'+opg: S_high, 'V_high_'+opg: V_high}
        user_settings.save_settings(hsvDict)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
