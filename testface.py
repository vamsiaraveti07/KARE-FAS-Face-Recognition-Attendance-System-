import face_recognition
import cv2

cam = cv2.VideoCapture(0)
print("[INFO] Press Q to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        print("[ERROR] Camera issue.")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)

    for (top, right, bottom, left) in boxes:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Face Detection Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
