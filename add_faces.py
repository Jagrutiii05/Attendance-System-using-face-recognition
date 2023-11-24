import cv2

# 0: for inbuilt camera, 1: for external webcam
video = cv2.VideoCapture(0)

while True:
    # video.read() method gives two values: 
    # 1. ret: boolean value to tell if the camera is ok
    # 2. frame 
    ret, frame = video.read()
    # print(frame.shape) 
    # if the camera is not working, then ret will be False
    if not ret:
        print("Camera is not working")
        break
    # to display an image we use imshow
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    # if 'q' is pressed, then break the loop
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()