import track_hand as htm
import time

import pyautogui
import cv2
import argparse
from pythonosc import udp_client

CAMERA_WIDTH, CAMERA_HEIGHT = 1280, 720
FRAME_RATE = 100
SMOOTHENING = 7

PLOCX, PLOCKY = 0, 0
CLOCX, CLOCKY = 0, 0

def handle_connection(cap, p_time = 0):
    while True:
        fingers = [0, 0, 0, 0, 0]
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList, bbox = detector.findPosition(img, draw=True)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            # this detects the fingers through ai camera detection

        cv2.rectangle(
            img,
            (FRAME_RATE, FRAME_RATE),
            (CAMERA_WIDTH - FRAME_RATE, CAMERA_HEIGHT - FRAME_RATE),
            (48, 96, 108),
            2,
        )

        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - p_time)

        p_time = cTime
        cv2.putText(
            img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
        ) 
        # 12. Display

        cv2.imshow("Image", img)
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        client.send_message(
            "/filter", fingers
        )  # this sends whichever finger is up as a list to MAX
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument(
        "--port", type=int, default=5005, help="The port the OSC server is listening on"
    )
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)
    cap = cv2.VideoCapture(0)
    cap.set(3, CAMERA_WIDTH)
    cap.set(4, CAMERA_HEIGHT)
    detector = htm.handDetector(maxHands=1)  # change how many hands can be detected
    wScr, hScr = pyautogui.size()
    handle_connection(cap)