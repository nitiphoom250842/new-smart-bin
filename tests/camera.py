import cv2
import time
import sys

count = 0

index = sys.argv[1]
print(f'camera index {index}')

cap = cv2.VideoCapture(int(index))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_EXPOSURE, 25)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    cnt = 0
    while cnt < 5:
        ret, frame = cap.read()
        cnt += 1

    if not ret:
        count += 1
        print(f'Can\'t receive frame (stream end?). Exiting ... {count}')
        time.sleep(3)
        continue

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

    cap.release()
    cv2.destroyAllWindows()
