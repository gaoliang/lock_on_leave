import subprocess
import time

import cv2
import pync
import Quartz

import face_recognition

picture_of_me = face_recognition.load_image_file("me.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]


def lock():
    subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend',
                    shell=True)


def is_locked():
    d = Quartz.CGSessionCopyCurrentDictionary()
    return d.get("CGSSessionScreenIsLocked", 0) == 0 and d.get("kCGSSessionOnConsoleKey", 0) == 0


def is_me():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # width=640
    cap.set(4, 480)  # height=480

    if not cap.isOpened():
        pync.notify("⚠️ Unable to open camera. Please check", title="🔐 Lock on leave")
        return True

    _, frame = cap.read()
    cap.release()  # releasing camera immediately after capturing picture

    if not _ or frame is None:
        pync.notify("⚠️ Unable to capture image. Please check", title="🔐 Lock on leave")
        return True

    cv2.imwrite('unknown.jpg', frame)
    unknown_picture = face_recognition.load_image_file('unknown.jpg')
    unknown_face_encodings = face_recognition.face_encodings(unknown_picture)
    for unknown_face_encoding in unknown_face_encodings:
        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
        if results[0]:
            return True

    return False


if __name__ == "__main__":
    while True:
        if is_locked() or is_me():
            time.sleep(10)
            continue
        else:
            will_lock = True
            for i in range(5, 0, -1):
                pync.notify("⚠️ Can not find you, Going to Lock in {} second".format(i), title="🔐 Lock on leave")
                time.sleep(1)
                if is_me():
                    pync.notify("✅ Find you! Cancel lock", title="🔐 Lock on leave")
                    will_lock = False
                    break
            if will_lock:
                lock()
