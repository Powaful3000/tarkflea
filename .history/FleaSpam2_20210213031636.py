import acapture
import cv2
import time

cap = acapture.open(-1)
while True:
    now = time.time()
    check, frame = cap.read()  # blocking
    print(time.time() - now)
    if check:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("test", frame)
