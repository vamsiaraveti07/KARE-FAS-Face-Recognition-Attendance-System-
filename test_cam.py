import cv2

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cam.isOpened():
    print("❌ Webcam not accessible")
else:
    print("✅ Webcam opened successfully")

while True:
    ret, frame = cam.read()
    if not ret:
        print("❌ Failed to grab frame")
        break
    cv2.imshow("Webcam Test", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
