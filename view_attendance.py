import os
import csv

attendance_dir = "attendance"

def list_attendance_files():
    print("\n📅 Available Attendance Files:")
    files = [f for f in os.listdir(attendance_dir) if f.endswith(".csv")]
    if not files:
        print("❌ No attendance records found.")
        return []
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    return files

def view_file(file_path):
    print(f"\n📄 Attendance in: {file_path}")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            print(f"ID: {row[0]}  |  Name: {row[1]}  |  Time: {row[2]}")

def view_by_student_id():
    student_id = input("Enter Student ID: ").strip()
    print(f"\n📘 Attendance for ID: {student_id}")
    found = False
    for filename in os.listdir(attendance_dir):
        if filename.endswith(".csv"):
            with open(os.path.join(attendance_dir, filename), "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if row[0] == student_id:
                        print(f"✔ {filename} | Name: {row[1]} | Time: {row[2]}")
                        found = True
    if not found:
        print("❌ No attendance found for this ID.")

def menu():
    print("\n📊 ATTENDANCE VIEWER")
    print("===========================")
    print("1. View attendance by date")
    print("2. View attendance by student ID")
    print("3. Exit")
    print("===========================")

while True:
    menu()
    choice = input("Choose option (1–3): ").strip()

    if choice == "1":
        files = list_attendance_files()
        if files:
            sel = input("Enter file number to view: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(files):
                view_file(os.path.join(attendance_dir, files[int(sel)-1]))
            else:
                print("❌ Invalid selection.")
    elif choice == "2":
        view_by_student_id()
    elif choice == "3":
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid option.")
