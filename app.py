from flask import Flask, render_template, request, redirect, url_for, session
import os, csv
from flask import send_file
from datetime import datetime
import subprocess
import json
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from werkzeug.security import generate_password_hash




app = Flask(__name__)
app.secret_key = 'super_secret_key'
USER_FILE = 'users.csv'

# ---------------- LOGIN ----------------

users = [
    {"username": "admin1", "password": "admin123", "role": "admin"},
    {"username": "student1", "password": "student123", "role": "student"}
]

with open("users.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["username", "password", "role"])
    writer.writeheader()
    for user in users:
        user['password'] = generate_password_hash(user['password'])
        writer.writerow(user)

print("✅ users.csv created with hashed passwords.")
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', '').strip().lower()

        if not username or not password or not role:
            error = "All fields are required."
        elif os.path.exists(USER_FILE):
            with open(USER_FILE, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['username'] == username and row['role'] == role:
                        if check_password_hash(row['password'], password):
                            session['username'] = username
                            session['role'] = role
                            if role == 'student':
                                session['reg_no'] = username  # ✅ Required for student profile

                            return redirect(url_for('admin_dashboard') if role == 'admin' else url_for('student_dashboard'))
        error = "Invalid credentials"

    return render_template('login.html', error=error)


# ---------------- DASHBOARDS ----------------
@app.route('/admin')
def admin_dashboard():
    if 'username' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html', user=session['username'])
    return redirect(url_for('login'))




# ---------------- REGISTER STUDENT ----------------
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    message = None

    if request.method == 'POST':
        try:
            name = request.form['name']
            register_number = request.form['register_number']
            room = request.form['room']
        except KeyError as e:
            return f"❌ Missing field: {e.args[0]}. Check your HTML input `name=` attributes.", 400

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file_path = 'students.csv'
        exists = False

        if os.path.exists(file_path):
            with open(file_path, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['register_number'] == register_number:
                        exists = True
                        break

        if exists:
            message = "⚠️ Student already registered."
        else:
            with open(file_path, 'a', newline='') as f:
                fieldnames = ['name', 'register_number', 'room', 'registered_on']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if os.stat(file_path).st_size == 0:
                    writer.writeheader()
                writer.writerow({
                    'name': name,
                    'register_number': register_number,
                    'room': room,
                    'registered_on': date
                })

            # Launch face capture in terminal
            try:
                subprocess.Popen(f'start cmd /k python register.py "{register_number}" "{name}"', shell=True)

                message = f"✅ {name} registered successfully! Face capture launched in terminal."
            except Exception as e:
                message = f"❌ Student saved, but face capture failed: {e}"

        return render_template('add_student.html', message=message)

    return render_template('add_student.html')

# ---------------- VIEW STUDENTS ----------------
@app.route('/student_profile')
def student_profile():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('login'))

    reg_number = session['username']  # or session['reg_no'] if set

    student_info = None
    if os.path.exists('students.csv'):
        with open('students.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['register_number'] == reg_number:
                    student_info = row
                    break

    if student_info:
        return render_template('student_profile.html', student=student_info)
    else:
        return "❌ Student profile not found."



# ---------------- DELETE STUDENT ----------------
@app.route('/delete_student', methods=['POST'])
def delete_student():
    username = request.form['username']
    updated_students = []
    removed = False

    if os.path.exists(USER_FILE):
        with open(USER_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] != username:
                    updated_students.append(row)
                else:
                    removed = True

        if removed:
            with open(USER_FILE, 'w', newline='') as f:
                fieldnames = ['username', 'password', 'role', 'room', 'registered_on']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_students)

    return redirect(url_for('view_students'))

# ---------------- OTHER ROUTES ----------------

@app.route('/create_credentials', methods=['GET', 'POST'])
def create_credentials():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        room = request.form['room']  # Not stored in users.csv
        role = 'student'
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        hashed_pw = generate_password_hash(password)

        exists = False
        if os.path.exists(USER_FILE):
            with open(USER_FILE, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['username'] == username:
                        exists = True
                        break

        if exists:
            message = "⚠️ Username already exists!"
        else:
            file_exists = os.path.isfile(USER_FILE)
            with open(USER_FILE, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['username', 'password', 'role'])
                if not file_exists or os.stat(USER_FILE).st_size == 0:
                    writer.writeheader()
                writer.writerow({
                    'username': username,  # ✅ Fixed here
                    'password': hashed_pw,
                    'role': role
                })
            message = f"✅ Credentials created for {username}"

    return render_template('create_credentials.html', message=message)



@app.route('/view_students')
def view_students():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    student_file = 'students.csv'
    attendance_file = 'attendance.csv'
    students = []
    attendance_count = defaultdict(int)
    total_days = set()

    # Count attendance
    if os.path.exists(attendance_file):
        with open(attendance_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date_only = row['Time'].split()[0]
                reg_no = row['register_number']
                attendance_count[reg_no] += 1
                total_days.add(date_only)

    total_working_days = len(total_days)

    # Read students and add attendance percentage
    if os.path.exists(student_file):
        with open(student_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                reg_no = row['register_number']
                count = attendance_count.get(reg_no, 0)
                percentage = round((count / total_working_days) * 100, 2) if total_working_days else 0
                row['attendance_percentage'] = f"{percentage}%"
                students.append(row)

    return render_template('view_students.html', students=students)



@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', user=session['username'], role=session['role'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/capture_face/<register_number>/<name>')
def capture_face(register_number, name):
    subprocess.Popen(f'start cmd /k python register.py "{register_number}" "{name}"', shell=True)
    return f"🟢 Face capture launched for {name} (Reg: {register_number})."
#-- Take Attendance Route----
@app.route('/take_attendance')
def take_attendance():
    try:
        subprocess.Popen(['start', 'cmd', '/k', 'python face_attendance.py'], shell=True)
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        return f"❌ Failed to start attendance: {e}"
# ---------------- STUDENT DASHBOARD ----------------
@app.template_filter('zfill')
def zfill_filter(value, width=2):
    return str(value).zfill(width)
app.secret_key = 'your_secret_key_here'

@app.route('/student_dashboard')
def student_dashboard():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('login'))

    reg_no = session['username']
    logs = []
    present_days = set()
    all_dates = set()

    if os.path.exists('attendance.csv'):
        with open('attendance.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                time_str = row['Time']
                date_only = time_str.split()[0]
                all_dates.add(date_only)

                if row['register_number'] == reg_no:
                    logs.append({
                        'date': date_only,
                        'time': time_str.split()[1] if len(time_str.split()) > 1 else ''
                    })
                    present_days.add(date_only)

    total_present = len(present_days)
    total_days = len(all_dates)
    total_absent = total_days - total_present
    attendance_percentage = round((total_present / total_days) * 100, 2) if total_days > 0 else 0
    alert = attendance_percentage < 75

    return render_template("student_dashboard.html",
                           user=session['username'],
                           logs=logs,
                           total_present=total_present,
                           total_absent=total_absent,
                           percentage=attendance_percentage,
                           alert=alert,
                           calendar_data=json.dumps(list(present_days)))

    

# ---------------- DOWNLOAD ATTENDANCE ----------------
@app.route('/download_attendance')
def download_attendance():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('login'))

    reg_no = session['username']
    temp_file = f"temp_{reg_no}_attendance.csv"

    with open("attendance.csv", newline='') as infile, open(temp_file, "w", newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row['register_number'] == reg_no:
                writer.writerow(row)

    return send_file(temp_file, as_attachment=True, download_name="My_Attendance.csv")


@app.route('/view_all_attendance')
def view_all_attendance():
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    records = []
    if os.path.exists('attendance.csv'):
        with open('attendance.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    return render_template('view_all_attendance.html', records=records)
                


@app.route('/admin_attendance', methods=['GET', 'POST'])
def admin_attendance():
    attendance_file = 'attendance.csv'
    student_file = 'students.csv'
    records = []
    selected_date = ''
    total_days_set = set()
    attendance_count = defaultdict(int)

    # Date filter
    if request.method == 'POST':
        raw_date = request.form.get('date')
        try:
            selected_date = datetime.strptime(raw_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            selected_date = ''

    # Read attendance.csv
    if os.path.exists(attendance_file):
        with open(attendance_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                reg_no = row['register_number']
                time_val = row['Time']
                date_only = time_val.split()[0]

                total_days_set.add(date_only)

                if not selected_date or selected_date == date_only:
                    records.append(row)

                attendance_count[reg_no] += 1

    total_working_days = len(total_days_set)

    # Read student info + calculate attendance %
    student_data = []
    if os.path.exists(student_file):
        with open(student_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                reg = row['register_number']
                count = attendance_count.get(reg, 0)
                percentage = round((count / total_working_days) * 100, 2) if total_working_days else 0
                row['attendance_percentage'] = f"{percentage}%"
                student_data.append(row)

    return render_template('admin_attendance.html',
                           records=records,
                           selected_date=selected_date,
                           students=student_data,
                           total_days=total_working_days)

@app.route('/export_csv')
def export_csv():
    from flask import send_file
    file_path = 'attendance.csv'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "⚠️ Attendance file not found.", 404




# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)
