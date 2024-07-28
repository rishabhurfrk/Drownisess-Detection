# Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
# face_utils for basic operations of conversion
from imutils import face_utils

import time

import serial

from twilio.rest import Client

account_sid = 'AC4237e5d3b7c7c194191970e97d4d8a68'
auth_token = '7a34f7c1070fa1b1baaabe1d340142c3'
client = Client(account_sid, auth_token)


# message = client.messages.create(
#   from_='+17865743020',
#   body='drowsy',
#   to='+916372083316'
# )

# print(message.sid)

arduino = serial.Serial(port='COM8', baudrate=9600, timeout=0.1)

def write(x):
    arduino.write(bytes(x, 'utf-8'))

# Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)

# Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# status marking for current state
sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)

def compute(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    # Checking if it is blinked
    if ratio > 0.25:
        return 2
    elif 0.21 < ratio <= 0.25:
        return 1
    else:
        return 0

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    # detected face in faces array
    face_frame = frame.copy()
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # The numbers are actually the landmarks which will show the eye
        left_blink = blinked(landmarks[36], landmarks[37],
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43],
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Now judge what to do for the eye blinks
        data=arduino.readline()
        if data==1:
            print("drunk")
            print(data)
            message = client.messages.create(
            from_='+13368951829',
            body='Driver is drunk',
            to='+919508465840'
            )


            print(message.sid)
            #twillio function
        
        elif left_blink == 0 or right_blink == 0:
            sleep += 1
            drowsy = 0
            active = 0
            if sleep > 6:
                status = "SLEEPING !!!"
                print(status)
                write("2")
                print(data)
                color = (255, 0, 0)
                message = client.messages.create(
                from_='+13368951829',
                body='Driver is sleeping',
                to='+919508465840'
                )
                print(message.sid)

        elif 1 <= left_blink <= 1 or 1 <= right_blink <= 1:
            sleep = 0
            active = 0
            drowsy += 1
            if drowsy > 6:
                status = "Drowsy !"
                print(status)
                write("3")
                print(data)
                color = (0, 0, 255)
                
                message = client.messages.create(
                from_='+13368951829',
                body='Driver is drowsy',
                to='+919508465840'
                )

    
                print(message.sid)

        else:
            drowsy = 0
            sleep = 0
            active += 1
            if active > 6:
                status = "Active :)"
                print(status)
                write("4")
                print(data)
                color = (0, 255, 0)
        

        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break   