import cv2
import pickle
import numpy as np
import os

# 0: for inbuilt camera, 1: for external webcam
video = cv2.VideoCapture(0)

# detect faces using haar cascade classifier
face_detect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []

i=0
name = input("Enter your name: ")

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

# convert data into numPy array
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)

# store it into pickle file so that we can use it later

# if names.pkl file is not available will create new file
if 'names.pkl' not in os.listdir('data/'):
    # all the 100 data captured will be named
    names = [name]*100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    names += [name]*100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)