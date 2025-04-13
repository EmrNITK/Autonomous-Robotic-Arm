import cv2
import numpy as np


cap = cv2.VideoCapture(1)

def onChange(x):
    pass

while True:
    ret, frame = cap.read()
    if not ret:
        break


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    cv2.namedWindow("Win1")
    cv2.createTrackbar("thres1","Win1",10,200,onChange)
    cv2.createTrackbar("thres2","Win1",20,200,onChange)

    canny  = cv2.Canny(gray,184,14)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_OTSU)
    cv2.imshow("Circle", thresh)
    cv2.imshow("Canny",canny)
    # while True:
    #     th1 = cv2.getTrackbarPos("thres1","Win1")
    #     th2 = cv2.getTrackbarPos("thres2","Win1")
    #     canny = cv2.Canny(gray,th1,th2)
    #     cv2.imshow("Canny",canny)
    #     k = cv2.waitKey(1)
    #     if k==ord('q'):
    #         break
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))

        if area > 100:
            # Draw the contour
            cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)

            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])


                cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)


                coord_text = f"({cx}, {cy})"
                cv2.putText(frame, coord_text, (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)


    cv2.imshow("Circle Contour Detection", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
