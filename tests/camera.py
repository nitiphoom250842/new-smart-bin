import cv2
import time
import sys

count = 0

index = sys.argv[1]
print(f'camera index {index}')
cap = cv2.VideoCapture(int(index))

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

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
