import os
import pickle
import shutil

def menu():
    print("\n🎓 FACE RECOGNITION ATTENDANCE SYSTEM")
    print("========================================")
    print("1. Register a new student")
    print("2. View registered students")
    print("3. Start face attendance")
    print("4. Delete a student by ID")
    print("5. Reset system (Delete all)")
    print("6. Exit")
    print("========================================")

def run_command(cmd):
    os.system(f'python {cmd}')

def delete_student_by_id():
    target_id = input("Enter the Student ID to delete: ").strip()
    if not os.path.exists("encodings.pkl"):
        print("❌ No data to delete.")
        return

    with open("encodings.pkl", "rb") as f:
        data = pickle.load(f)

    if target_id not in data["ids"]:
        print("❌ Student ID not found.")
        return

    # Get all matching indexes
    indexes_to_delete = [i for i, sid in enumerate(data["ids"]) if sid == target_id]
    for i in sorted(indexes_to_delete, reverse=True):
        del data["ids"][i]
        del data["names"][i]
        del data["encodings"][i]

    # Save updated encodings
    with open("encodings.pkl", "wb") as f:
        pickle.dump(data, f)

    # Try deleting dataset folder
    folders = os.listdir("dataset")
    for folder in folders:
        if folder.startswith(target_id + "_"):
            shutil.rmtree(os.path.join("dataset", folder))
            break

    print(f"✅ Deleted student ID {target_id} and related data.")

while True:
    menu()
    choice = input("Choose an option (1-6): ").strip()

    if choice == "1":
        run_command("register.py")
    elif choice == "2":
        run_command("view_registered_students.py")
    elif choice == "3":
        run_command("face_attendance.py")
    elif choice == "4":
        delete_student_by_id()
    elif choice == "5":
        confirm = input("⚠️ Are you sure? This will delete ALL data (y/n): ")
        if confirm.lower() == 'y':
            if os.path.exists("encodings.pkl"):
                os.remove("encodings.pkl")
            if os.path.exists("dataset"):
                shutil.rmtree("dataset")
            print("✅ System reset successfully.")
    elif choice == "6":
        print("👋 Exiting. Goodbye!")
        break
    else:
        print("❌ Invalid option. Please choose between 1–6.")
