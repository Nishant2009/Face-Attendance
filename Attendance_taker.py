import face_recognition
import cv2
import csv
import json
import numpy as np
import os
import fileinput
import time
import random
import cvzone
from cvzone.HandTrackingModule import HandDetector
import datetime
from numpy import array
from tkinter import messagebox
from dotenv import dotenv_values

# Initialize locations of the csv file and face_data directories from the .env file
env_vars = dotenv_values(".env")
attendance_csv = env_vars.get("ATTENDANCE_CSV")
face_data = env_vars.get("FACE_DATA_LOCATION")

# Reading the names by roll number from the attendance.csv file
names_by_roll_number = {}
with open(attendance_csv, "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row if there is one
    for row in reader:
        registration_no, name = row[0], row[1]
        names_by_roll_number[registration_no] = name

# The Hand Gesture Window
def gesturefunction(NAME):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    detector = HandDetector(maxHands=1)
    inTime = time.time()
    timer = 0
    stateResult = False
    startCheck = False
    present = False
    Wrong_Right = [0, 0]
    randomNumber = random.randint(1, 300) % 3
    totalmoves = 0

    while True:
        imgBG = cv2.imread("./Resources/BG.png")
        success, img = cap.read()
        imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
        imgScaled = imgScaled[:, 80:480]
        # Find Hands
        hands, img = detector.findHands(imgScaled)  # with draw
        if startCheck :
            if totalmoves < 2 or Wrong_Right[1] < 2:
                imgAI = cv2.imread(f'./Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
            if present :
                cv2.putText(imgBG, f"{names_by_roll_number[NAME]} {NAME}: Present", (310, 110), cv2.QT_FONT_NORMAL, 1.5, (0, 255, 0), 2)
            else:
                cv2.putText(imgBG, f"{names_by_roll_number[NAME]} {NAME}", (310, 110), cv2.QT_FONT_NORMAL, 1.5, (0, 255, 0), 2)
            if stateResult is False:
                timer = time.time() - initialTime
                cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
                if timer > 3 :
                    stateResult = True
                    timer = 0

                    if hands:
                        hand_movement = None
                        hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        totalmoves += 1
                        if fingers == [0, 0, 0, 0, 0]:
                            hand_movement = 1
                        elif fingers == [1, 1, 1, 1, 1]:
                            hand_movement = 2
                        elif fingers == [0, 1, 1, 0, 0]:
                            hand_movement = 3
                        else :
                            hand_movement = 4

                        if (hand_movement == randomNumber):
                            Wrong_Right[1] += 1
                        else:
                            Wrong_Right[0] +=1
                        randomNumber = random.randint(1, 300) % 3
                        if randomNumber == 0 :
                            randomNumber = 3

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if totalmoves >= 2 and Wrong_Right[1] >= 2 :
            present = True
            time.sleep(1)
            cv2.destroyAllWindows()
            return present            

        imgBG[234:654, 795:1195] = imgScaled

        if stateResult:
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

        cv2.putText(imgBG, str(Wrong_Right[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        if Wrong_Right[1] < 2:
            cv2.putText(imgBG, str(Wrong_Right[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        else:
            cv2.putText(imgBG, "P", (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

        cv2.imshow("BG", imgBG)
        key = cv2.waitKey(1)
        if datetime.datetime.now().second % 5 == 0 :
            startCheck = True
            initialTime = time.time()
            stateResult = False

# Load the known faces and embeddings saved in the file
known_faces = []
known_names = []

with open(face_data,"r") as r:
    d = r.read()
    b = json.loads(d)
    c = list(b.keys())
    for l in c:
        known_faces.append(array(b[l]))
        known_names.append(l)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
present_names = []
time_record = []

now = datetime.datetime.now()
date= now.strftime("%d/%m/%Y")

# Load the attendance file or SHOW ERROR if it doesn't exist
if os.path.exists(attendance_csv):
    # Modify the first line to add the current date
    with fileinput.FileInput(attendance_csv, inplace=True) as file:
        for i, line in enumerate(file):
            if i == 0 and date not in line.rstrip():
                modified_line = line.rstrip() + f', {date}\n'
                print(modified_line, end='')
            else:
                print(line, end='')
else:
    messagebox.showerror("ERROR", "Attendance CSV NOT FOUND !!!")
    exit()

# Open the camera and capture the video stream
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a single frame from the camera
    ret, frame = video_capture.read()
    if not ret:
        video_capture = cv2.VideoCapture(0)
        continue
    # Resize the frame for faster face detection
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Find all the faces and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    # Loop through each face in this frame and compare with the known faces
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known faces
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"
        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]
        face_names.append(name)
        
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        if name == "Unknown":
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        else:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255,0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.9, (255 ,255, 255), 1)
    # Add the recognized person to the attendance list
    for name in face_names:
        if name not in present_names and name != "Unknown":
            time.sleep(2)
            if gesturefunction(name):
                present_names.append(name)
                now = datetime.datetime.now()
                time_now= now.strftime(f"%I:%M:%S %p")
                time_record.append(time_now)
                continue

    # Display the resulting image
    cv2.imshow('Attendance', frame)
    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

with fileinput.FileInput(attendance_csv, inplace=True) as file:
    # Loop over the lines in the file
    for i, line in enumerate(file):
        name = line.rsplit(",")[0]
        # Add the string to the end of the first line
        if i != 0:
            if len(line.rsplit(",")) <= n-1 :
                if name in present_names:
                    print(line.rstrip()+f", {time_record[present_names.index(name)]}\n", end='')
                else:
                    print(line.rstrip()+", A\n", end='')
            else:
                print(line.rstrip()+"\n", end='')
        else:
            n = len(line.rsplit(","))
            print(line.rstrip()+"\n", end='')

# Close video frame
video_capture.release()
cv2.destroyAllWindows()