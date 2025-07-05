# 🎓 Face Recognition Attendance System

A modern web-based **Face Recognition Attendance System** using **Flask, OpenCV, and face_recognition**, built for both Admins and Students. This system allows automatic student attendance using facial recognition with full dashboard functionality.

---

## 📸 Project Overview

This system uses a webcam to capture and recognize student faces and log attendance. Admins can register students, manage credentials, and generate attendance reports. Students can view their personal attendance data with calendar visualization, stats, and download options.

---

## 🔑 Features

### ✅ Admin
- 🔐 Login securely
- 🧍‍♂️ Add new student (with facial capture)
- 🔑 Create student credentials
- 👀 View all students
- 📅 Take face-based attendance
- 📊 View all attendance logs with filters
- 📁 Export attendance to CSV

### 🎓 Student
- 🔐 Login securely
- 👤 View personal profile
- 📆 Dashboard showing:
  - Calendar view of attendance
  - Total present/absent days
  - Attendance percentage
  - Low-attendance alerts
  - Filter by month/week
  - 📄 Download attendance report (PDF)

---

## 🧰 Technologies Used

| Component            | Technology       |
|---------------------|------------------|
| Backend             | Flask (Python)   |
| Face Detection      | OpenCV, face_recognition |
| Frontend UI         | HTML, CSS, JavaScript |
| Data Storage        | CSV files        |
| PDF Export          | jsPDF            |

---

## 📂 CSV Files

### `users.csv`
Stores login credentials.
### Student.csv
Stores student details
### attendance.csv
stores students daily attendance 

## 📸 Face Registration & Attendance
Uses face_register.py to capture student face data and encode it using face_recognition.
face_attendance.py matches live webcam input with stored encodings to log attendance.

# 👨‍💻 Author
## Vamsi Araveti

💼 Final year B.Tech Student

💡 Built this project to showcase skills in computer vision, Python, Flask, and real-world software deployment.
