import sqlite3
import bcrypt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "banbhan.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, father_name TEXT NOT NULL, class_name TEXT NOT NULL, section TEXT NOT NULL, gr_number TEXT UNIQUE NOT NULL, phone TEXT, sibling_of TEXT, face_embedding BLOB, photo_b64 TEXT, is_active INTEGER DEFAULT 1, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, father_name TEXT NOT NULL, employee_id TEXT UNIQUE NOT NULL, subject TEXT, designation TEXT, department TEXT, joining_date TEXT, phone TEXT, email TEXT, face_embedding BLOB, photo_b64 TEXT, is_active INTEGER DEFAULT 1, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS student_attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, date TEXT NOT NULL, scan_time TEXT NOT NULL, status TEXT NOT NULL, FOREIGN KEY(student_id) REFERENCES students(id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS teacher_attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher_id INTEGER NOT NULL, date TEXT NOT NULL, check_in TEXT NOT NULL, check_out TEXT, duty_hours TEXT, status TEXT NOT NULL, FOREIGN KEY(teacher_id) REFERENCES teachers(id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS teacher_absences (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher_id INTEGER, teacher_name TEXT, date TEXT, day_name TEXT, reason TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS holidays (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT UNIQUE NOT NULL, reason TEXT NOT NULL, created_by TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS authorized_devices (id INTEGER PRIMARY KEY AUTOINCREMENT, device_fingerprint TEXT UNIQUE NOT NULL, device_label TEXT, authorized_at DATETIME DEFAULT CURRENT_TIMESTAMP, last_seen DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, ip_address TEXT, success INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, target_type TEXT, target_id INTEGER, details TEXT, admin_user TEXT, ip_address TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")

    admin = cursor.execute("SELECT * FROM users WHERE username=?", ("Muhammad Ali",)).fetchone()
    if not admin:
        pw_hash = bcrypt.hashpw("mali00".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("Muhammad Ali", pw_hash))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database Initialized Successfully!")