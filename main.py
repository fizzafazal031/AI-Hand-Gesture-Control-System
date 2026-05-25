import cv2
import mediapipe as mp
import pyautogui
import time
import subprocess

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

last_action_time = 0
delay = 1.0

gesture_text = "No Gesture"

def fingers_up(lm):

    fingers = []

    # Thumb
    fingers.append(1 if lm[4].x < lm[3].x else 0)

    # Index
    fingers.append(1 if lm[8].y < lm[6].y else 0)

    # Middle
    fingers.append(1 if lm[12].y < lm[10].y else 0)

    # Ring
    fingers.append(1 if lm[16].y < lm[14].y else 0)

    # Pinky
    fingers.append(1 if lm[20].y < lm[18].y else 0)

    return fingers

    # MAIN LOOP
while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    current_time = time.time()

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            lm = handLms.landmark

            f = fingers_up(lm)

            #  Volume Up
            if f == [1,0,0,0,0]:

                gesture_text = "Volume Up"

                if current_time - last_action_time > delay:

                    pyautogui.press("volumeup")

                    last_action_time = current_time

            #  Volume Down
            elif f == [0,0,0,0,0]:

                gesture_text = "Volume Down"

                if current_time - last_action_time > delay:

                    pyautogui.press("volumedown")

                    last_action_time = current_time

            #  Next
            elif f == [0,1,0,0,0]:

                gesture_text = "Next"

                if current_time - last_action_time > delay:

                    pyautogui.press("right")

                    last_action_time = current_time

            #  Previous
            elif f == [0,1,1,0,0]:

                gesture_text = "Previous"

                if current_time - last_action_time > delay:

                    pyautogui.press("left")

                    last_action_time = current_time

            #  Play / Pause
            elif f == [0,1,1,1,0]:

                gesture_text = "Play / Pause"

                if current_time - last_action_time > delay:

                    pyautogui.press("playpause")

                    last_action_time = current_time

            #  Screenshot
            elif f == [1,1,1,1,1]:

                gesture_text = "Screenshot"

                if current_time - last_action_time > delay:

                    filename = f"screenshot_{int(time.time())}.png"

                    pyautogui.screenshot(filename)

                    last_action_time = current_time

            #  Scroll Up
            elif f == [0,0,1,1,1]:

                gesture_text = "Scroll Up"

                pyautogui.scroll(60)

            #  Scroll Down
            elif f == [0,0,0,1,1]:

                gesture_text = "Scroll Down"

                pyautogui.scroll(-60)

            #  Open Chrome
            elif f == [1,1,0,0,0]:

                gesture_text = "Open Chrome"

                if current_time - last_action_time > delay:

                    subprocess.Popen("start chrome", shell=True)

                    last_action_time = current_time

            #  Open Calculator
            elif f == [1,1,1,0,0]:

                gesture_text = "Open Calculator"

                if current_time - last_action_time > delay:

                    subprocess.Popen("calc")

                    last_action_time = current_time

            #  Open Notepad
            elif f == [1,1,1,1,0]:

                gesture_text = "Open Notepad"

                if current_time - last_action_time > delay:

                    subprocess.Popen("notepad")

                    last_action_time = current_time

            # Close Active Window
            elif f == [1,0,0,0,1]:

                gesture_text = "Close Window"

                if current_time - last_action_time > delay:

                    pyautogui.hotkey("alt", "f4")

                    last_action_time = current_time

            mp_draw.draw_landmarks(
                img,
                handLms,
                mp_hands.HAND_CONNECTIONS
            )

    else:
        gesture_text = "No Hand Detected"

    # UI
    cv2.rectangle(img, (0,0), (750,100), (0,0,0), -1)

    cv2.putText(
        img,
        f"Gesture: {gesture_text}",
        (10,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    cv2.putText(
        img,
        "System: Running",
        (10,75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    cv2.imshow("Gesture Control System", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
