import cv2

# 0: for inbuilt camera, 1: for external webcam
video = cv2.VideoCapture(0)

# detect faces using haar cascade classifier
face_detect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

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
    
    # convert the frame to gray scale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray_frame, 1.3, 5)

    # Take coordinates x, y and w, h for width and height
    for (x, y, w, h) in faces:
        # image, point1, point2, color of the frame, thickness 
        cv2.rectangle(frame, (x,y), (x+w, y+h), (143,143,255), 2)


    # to display an image we use imshow
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    # if 'q' is pressed, then break the loop
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()