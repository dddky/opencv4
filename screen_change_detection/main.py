import cv2
import numpy as np
from mss import mss

def screen_change_detection():
    monitor = {"top": 0, "left": 0, "width": 800, "height": 600}

    cv2.namedWindow("Screen Change Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Screen Change Detection", 1600, 900)

    with mss() as sct:
        print("按'q'键退出，'r'键重置背景...")

        screenshot = sct.grab(monitor)
        background = np.array(screenshot)
        background = cv2.cvtColor(background, cv2.COLOR_BGRA2BGR)
        background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        background_gray = cv2.GaussianBlur(background_gray, (21, 21), 0)

        while True:
            screenshot = sct.grab(monitor)
            current = np.array(screenshot)
            current = cv2.cvtColor(current, cv2.COLOR_BGRA2BGR)
            current_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
            current_gray = cv2.GaussianBlur(current_gray, (21, 21), 0)

            diff = cv2.absdiff(background_gray, current_gray)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

            dilated = cv2.dilate(thresh, None, iterations=2)

            contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) < 500:
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(current, (x, y), (x + w, y + h), (0, 0, 255), 2)

            diff_colored = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
            thresh_colored = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
            combined = np.hstack((current, diff_colored, thresh_colored))

            cv2.imshow("Screen Change Detection", combined)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                background_gray = current_gray.copy()
                print("背景已重置")

    cv2.destroyAllWindows()

screen_change_detection()
