import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width=640
cap.set(4, 480)  # height=480

if cap.isOpened():
    _, frame = cap.read()
    cap.release()  # releasing camera immediately after capturing picture
    if _ and frame is not None:
        cv2.imwrite('me.jpg', frame)
