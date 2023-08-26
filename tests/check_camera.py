import cv2 as cv
import sys

index = sys.argv[1]
print(f'camera index {index}')
cap = cv.VideoCapture(int(index))

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)

    if cv.waitKey(1) == ord('q'):
        break

    cap.release()
    cv.destroyAllWindows()
