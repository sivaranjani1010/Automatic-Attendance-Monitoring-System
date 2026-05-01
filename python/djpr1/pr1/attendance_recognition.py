import cv2
import face_recognition
import numpy as np
import os
import django
import sys
import pytz  # <-- added for timezone conversion

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pr1.settings")
django.setup()

from myapp.models import Student, Attendance  # ✅ change "myapp" if needed
from django.utils import timezone

# ----------------------------
# Load dataset
# ----------------------------
dataset_path = os.path.join("media", "dataset")
print(f"📂 Loading dataset images from: {dataset_path}")

encoded_faces = []
roll_numbers = []

for file in os.listdir(dataset_path):
    if file.endswith((".jpg", ".png", ".jpeg")):
        rollno = os.path.splitext(file)[0]
        filepath = os.path.join(dataset_path, file)

        print(f"🔍 Processing {file} for rollno {rollno}...")

        img = cv2.imread(filepath)
        if img is None:
            print(f"❌ Could not read {file}, skipping...")
            continue

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        small_img = cv2.resize(rgb_img, (0, 0), fx=0.25, fy=0.25)
        encodings = face_recognition.face_encodings(small_img)

        if len(encodings) > 0:
            encoded_faces.append(encodings[0])
            roll_numbers.append(rollno)
            print(f"✅ Added encoding for {rollno}")
        else:
            print(f"⚠️ No face detected in {file}, skipping...")

print(f"➡️ Finished processing dataset.")
print(f"✅ {len(encoded_faces)} images loaded.")

# ----------------------------
# Mark everyone absent first
# ----------------------------
today = timezone.now().date()
for student in Student.objects.all():
    Attendance.objects.update_or_create(
        student=student,
        date=today,
        defaults={"status": "Absent"}
    )
print(f"🗓️ All students marked Absent by default.")

# ----------------------------
# Start camera
# ----------------------------
print("🚀 Camera starting now... Press 'q' to quit.")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not accessible. Exiting...")
    sys.exit()

recognized_set = set()
ist = pytz.timezone('Asia/Kolkata')  # ✅ IST timezone object created once

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(rgb_frame)
    encodings_in_frame = face_recognition.face_encodings(rgb_frame, faces_in_frame)

    for encoding, location in zip(encodings_in_frame, faces_in_frame):
        matches = face_recognition.compare_faces(encoded_faces, encoding)
        face_distances = face_recognition.face_distance(encoded_faces, encoding)

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                rollno = roll_numbers[best_match_index]

                if rollno not in recognized_set:
                    recognized_set.add(rollno)
                    print(f"✅ Recognized: {rollno}")

                    student = Student.objects.filter(student_rollno=rollno).first()
                    if student:
                        # ✅ Get current IST time
                        current_time_ist = timezone.now().astimezone(ist).time()

                        Attendance.objects.update_or_create(
                            student=student,
                            date=today,
                            defaults={"status": "Present", "time": current_time_ist}
                        )
                        print(f"📌 Attendance updated for {rollno}")

                # Draw box + name
                top, right, bottom, left = location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, rollno, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Attendance Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("📹 Attendance recognition ended.")




# pip install numpy==1.26.4
