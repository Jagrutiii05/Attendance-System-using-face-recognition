import cv2

# 0: for inbuilt camera, 1: for external webcam
video = cv2.VideoCapture(0)

# detect faces using haar cascade classifier
face_detect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []

i=0

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
        # crop the image and resize every image to same dimension. frame[y:y+h, x:x+w, :] --> crop
        crop_resized_img = cv2.resize(frame[y:y+h, x:x+w, :], (50,50))
        if len(faces_data) <= 100 and i%10 == 0:
            faces_data.append(crop_resized_img)
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50,50), cv2.FONT_ITALIC, 1, (143,143,255), 2)
        # draw rectangle around the face
        # image, point1, point2, color of the frame, thickness 
        cv2.rectangle(frame, (x,y), (x+w, y+h), (143,143,255), 2)


    # to display an image we use imshow
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    # if 'q' is pressed, then break the loop
    if key == ord('q') or key == ord('Q') or len(faces_data) == 100:
        break
video.release()
cv2.destroyAllWindows()