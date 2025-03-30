import cv2
import depthai as dai

pipeline = dai.Pipeline()
cam = pipeline.create(dai.node.ColorCamera)
xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("rgb")

cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam.setVideoSize(1080,720)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam.initialControl.setSaturation(2)

cam.video.link(xout.input)
device = dai.Device(pipeline)
num = 1
CHESSBOARD_SIZE = (9,6)
while True:

    frame = device.getOutputQueue(name="rgb",maxSize = 1,blocking=False)
    if frame is not None:
        videoIn = frame.get()
        img = videoIn.getCvFrame()
        img_1 = cv2.resize(img,(1080,720))
        gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
        
        # Find chessboard corners
        ret_chess, corners = cv2.findChessboardCorners(gray, CHESSBOARD_SIZE, None)
        print(ret_chess)
        
        # Draw corners if found
        if ret_chess:
            # Draw and display the corners
            cv2.drawChessboardCorners(img_1, CHESSBOARD_SIZE, corners, ret_chess)
            cv2.putText(img_1, "Chessboard detected!", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display capture counter
        cv2.putText(img_1, f"Captured: {num}", (50, 720 - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow('Camera Calibration', img_1)
        
        # Wait for key press
        k = cv2.waitKey(1)
        if k==ord('s'):
            cv2.imwrite(filename = "D:\Opencv_projects\codes\Robotic_Arm_DIP\images\cal"+str(num)+".jpg",img = img)
            num = num + 1
            print("image saved!!")
        elif k==ord('q'):
            break
cv2.destroyAllWindows()