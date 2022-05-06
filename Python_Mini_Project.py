import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
import pandas as pd


def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        # calculating the RGB values which are close to the RGB values in the CSV file.
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


index = ["color", "color_name", "hex", "R", "G", "B"]
# reading the CSV file for reading the color name
csv = pd.read_csv('colors.csv', names=index, header=None)
# https://github.com/codebrainz/color-names/blob/master/output/colors.csv

# starting the camera and reading video stream.
cap = VideoStream(src=0).start()


while True:
    # Reading the video stream frame by frame.
    frame = cap.read()
    frame = np.flip(frame, axis=1)
    frame = imutils.resize(frame, width=640)
    frame = imutils.resize(frame, height=480)

    height, width, _ = frame.shape

    # calculating the center of the frame.
    cx = int(width / 2)
    cy = int(height / 2)

    # taking the center BGR values of frame.
    pixel_center_bgr = frame[cy, cx]
    print(pixel_center_bgr)
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

    # putting rectangle on frame for showing the color name.
    cv2.rectangle(frame, (20, 20), (750, 60), (b, g, r), -1)

    # getting color color name from get_color_name() function.
    text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
    cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    # putting black text on rectangle if the colors are light.
    if r + g + b >= 600:
        cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    # finally showing the whole video frame by frame.
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 113:
        break

cv2.destroyAllWindows()
