Face Recognition Attendance System

This is a Django + Python based project for automatic attendance marking using **Face Recognition** with period-wise tracking and live dashboard.

Features

 -Student face registration with image upload
 -Real-time face recognition using webcam
 -Liveness detection (blink + head movement)
 -Period-wise attendance tracking (P1 - P7)
 -Default status: Absent for all students
 -Auto mark Present when face detected
 -Date-wise attendance records
 -Export attendance to Excel
 -Dashboard with filters (date-wise view)

Tech Stack

- Python 
- Django 
- OpenCV 
- face_recognition library 
- Mediapipe 
- NumPy 
- Pandas
- SQLite / MySQL 

 Project Modules

- Student Management (Add / Delete / Image Upload)
- Attendance Recognition Engine
- Dashboard UI (Bootstrap)
- Period-wise Attendance System
- Excel Export Feature
  
 How It Works

1. Admin adds student with image
2. System stores face encoding
3. Camera detects face in real-time
4. Matching face → mark "Present"
5. If not detected → remains "Absent"
6. Dashboard shows full report

 Status

Project is under development  
New features like performance analytics and alerts will be added soon.

 Author

sivaranjani sivakumar
