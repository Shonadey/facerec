##pip install face_recognition#
##import face_recognition#
import cv2
import numpy as np
import csv
import os
from datetime import datetime

video_capture = cv2.VideoCapture(0)

jobs_image = cv2.load_image_file("photos/jobs.jpg")
jobs_encoding = cv2.face_encodings(jobs_image)[0]

mitali_dey_image = cv2.load_image_file("C://Users//jet//Pictures//Saved Pictures.jpg")
mitali_dey_encoding = cv2.face_encodings(mitali_dey_image)[0]

known_face_encoding = [
    jobs_encoding,
    mitali_dey_encoding
    #ratan_tata_encoding,
    #sadmona_encoding,
    #tesla_encoding
]

known_faces_names = [
    "jobs",
    "mitali_dey"
    #"ratan tata",
    #"sadmona",
    #"tesla"
]

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + '.csv', 'w+', newline='')
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    if s:
        face_locations = cv2.face_locations(rgb_small_frame)
        face_encodings = cv2.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = cv2.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = cv2.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor = (255, 0, 0)
                thickness = 3
                lineType = 2

                cv2.putText(frame, name + ' Present',
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            thickness,
                            lineType)

                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name, current_time])
    cv2.imshow("attendence system", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()