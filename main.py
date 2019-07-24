import subprocess
import time
from io import BytesIO

import Quartz
import cv2
import face_recognition
import pync
from PIL import Image

picture_of_me = face_recognition.load_image_file("me.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
my_face_encodings = [my_face_encoding]

# If you want, you can use multiple images at different angles to improve accuracy.
# 
# picture_of_me = face_recognition.load_image_file("me.jpg")
# my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
# picture_of_me = face_recognition.load_image_file("me2.jpg")
# my_face_encoding2 = face_recognition.face_encodings(picture_of_me)[0]
# picture_of_me = face_recognition.load_image_file("me3.jpg")
# my_face_encoding3 = face_recognition.face_encodings(picture_of_me)[0]
# my_face_encodings = [my_face_encoding, my_face_encoding2, my_face_encoding3]



def notify(message):
    pync.notify(message, title="🔐 Lock on leave", group='lock_on_leave')


def lock():
    subprocess.call("open -a /System/Library/CoreServices/ScreenSaverEngine.app", shell=True)

    # old method.
    # loginPF = CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
    # result = loginPF.SACLockScreenImmediate()


def is_locked():
    d = Quartz.CGSessionCopyCurrentDictionary()
    return "CGSSessionScreenIsLocked" in d


def is_me():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # width=640
    cap.set(4, 480)  # height=480

    if not cap.isOpened():
        notify("⚠️ Unable to open camera. Please check")
        return True

    _, frame = cap.read()
    cap.release()  # releasing camera immediately after capturing picture

    if not _ or frame is None:
        notify("⚠️ Unable to capture image. Please check")
        return True
    img = Image.fromarray(frame)
    output = BytesIO()
    img.save(output, format='JPEG')
    unknown_picture = face_recognition.load_image_file(output)
    unknown_face_encodings = face_recognition.face_encodings(unknown_picture)
    for unknown_face_encoding in unknown_face_encodings:
        results = face_recognition.compare_faces(my_face_encodings, unknown_face_encoding)
        if any(results):
            return True

    return False


if __name__ == "__main__":
    while True:
        time.sleep(10)
        if is_locked() or is_me():
            continue

        will_lock = True
        for i in range(10, 0, -1):
            time.sleep(1)
            # Silence for the first five seconds
            if i <= 5:
                notify("⚠️ Can not find you, Going to Lock in {} second".format(i))
            if is_me():
                if i <= 5:
                    notify("✅ Find you! Cancel lock")
                will_lock = False
                break
        if will_lock:
            lock()
