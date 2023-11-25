from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

# Audio Function for confirmation
def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load pre-trained model
with open('data/names.pkl', 'rb') as w:
    labels = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    faces = pickle.load(f)

# create KNN classifier and fit the model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(faces, labels)

# attendance CSV file columns
col_names = ['Name', 'Time']

while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)

    # processing detected faces
    for (x,y,w,h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)

        # predict the label using trained KNN model
        output = knn.predict(resized_img)

        # current timestamp
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

        # to check if attendance CSV file for current date exists
        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

        # Rectangles and text on the frame
        cv2.rectangle(frame, (x,y), (x+w, y+h), (143,143,255), 2)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(143,143,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(143,143,255),-1)
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_ITALIC, 1, (255,255,255), 2)

        # create an attendance record
        attendance=[str(output[0]), str(timestamp)]
    
    # display frame
    cv2.imshow("Frame",frame)

    # wait for user input to confirm attendance(Y/y) or quit (Q/q)
    k = cv2.waitKey(1)
    if k == ord('Y') or k == ord('y'):
        speak("Attendance Taken..")
        time.sleep(1)
        if exist:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(col_names)
                writer.writerow(attendance)
            csvfile.close()
    if k==ord('q') or k==ord('Q'):
        break

video.release()
cv2.destroyAllWindows()