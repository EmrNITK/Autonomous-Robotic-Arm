import cv2

# Your cx and cy from calibration
cx = 353
cy = 271

# Open the webcam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Could not open webcam")
    exit()

while True:
    ret, frame = cap.read()
    img = frame.copy()
    if not ret:
        print("Failed to grab frame")
        break

    # Draw a red circle at the optical center
    cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)

    # Display the frame
    cv2.imshow("Webcam with cx, cy dot", frame)

    k = cv2.waitKey(1)
    # Press 'q' to quit

    if k==ord('c'):
        cv2.imwrite("./9_circle.jpg",img)

    if k & 0xFF == ord('q'):
        break

# Release and cleanup
cap.release()
cv2.destroyAllWindows()
