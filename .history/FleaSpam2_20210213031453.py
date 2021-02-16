import acapture
import cv2

cap = acapture.open(-1)
while True:
    check, frame = cap.read()  # blocking
    if check:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("test", frame)
        cv2.waitKey(1)
