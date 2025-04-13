import cv2
import numpy as np

def onChange(x):
    pass
# Load the image
image = cv2.imread('./9_circle.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
cv2.namedWindow("Win1")
cv2.createTrackbar("thres1","Win1",82,300,onChange)
cv2.createTrackbar("thres2","Win1",12,300,onChange)
# (82,12) -> 5
#(53,6) -> 7
# Blur to reduce noise

canny  = cv2.Canny(blur,82,12)
# cv2.imshow("canny",canny)
_, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
# while True:
#         th1 = cv2.getTrackbarPos("thres1","Win1")
#         th2 = cv2.getTrackbarPos("thres2","Win1")
#         canny = cv2.Canny(blur,th1,th2)
#         cv2.imshow("Canny",canny)
#         k = cv2.waitKey(1)
#         if k==ord('q'):
#             break

contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    # Filter by area to ignore noise
    area = cv2.contourArea(contour)
    if area < 100:
        continue

    # Draw contour
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    # Calculate moments and center
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Draw the center point
        cv2.circle(image, (cx, cy), 4, (0, 0, 255), -1)

        # Put text with coordinates
        coord_text = f"({cx}, {cy})"
        cv2.putText(image, coord_text, (cx + 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    else:
        continue

# Show the result
cv2.imshow("Circles with Centers", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
