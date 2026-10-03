import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "bss-v2-super-secret-key-2026-aoun-ali")
    DATABASE = os.environ.get("DATABASE_PATH", "banbhan.db")
    
    # SYSTEM LIMITS
    MAX_DEVICES = 25
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_MINUTES = 15
    SESSION_TIMEOUT_HOURS = 12
    
    # DEFAULT SCHOOL TIMINGS
    STUDENT_LATE_CUTOFF = "08:30"
    TEACHER_LATE_CUTOFF = "08:00"
    TEACHER_HALF_DAY_CUTOFF = "12:00"
    TEACHER_FULL_DAY_CUTOFF = "13:30"
    
    CLASSES = ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", 
               "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "KG-1", "KG-2", "Nursery"]
    SECTIONS = ["A", "B", "C", "D"]