# Mark a task as completed for a user
def mark_task_completed(user_id, task_id):
    global cursor, conn
    create_cursor()
    cursor.execute("INSERT OR IGNORE INTO COMPLETED_TASKS (USER_ID, TASK_ID) VALUES (?, ?)", (user_id, task_id))
    conn.commit()
    close_cursor()
def add_question(task_id, question_text, option_a, option_b, option_c, option_d, correct_option):
    global cursor, conn
    create_cursor()
    cursor.execute("""
        INSERT INTO QUESTIONS (TASK_ID, QUESTION_TEXT, OPTION_A, OPTION_B, OPTION_C, OPTION_D, CORRECT_OPTION)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (task_id, question_text, option_a, option_b, option_c, option_d, correct_option))
    conn.commit()
    close_cursor()

def get_questions_by_task(task_id):
    global cursor, conn
    create_cursor()
    cursor.execute("""
        SELECT ID, QUESTION_TEXT, OPTION_A, OPTION_B, OPTION_C, OPTION_D, CORRECT_OPTION
        FROM QUESTIONS
        WHERE TASK_ID = ?
    """, (task_id,))
    questions = cursor.fetchall()
    close_cursor()
    return questions
import sqlite3
import hashlib

cursor = None
db_name = "scripts/problems_db.sql"
conn = None

def create_cursor():
    global cursor, conn
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close_cursor():
    global cursor, conn
    cursor.close()
    conn.close()


def create_user_table():
    global cursor, conn
    create_cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS USER_TABLE (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    USERNAME TEXT UNIQUE NOT NULL,
                    PASSWORD NVARCHAR NOT NULL,
                    NAME TEXT NOT NULL,
                    GRADE INTEGER  CHECK(GRADE IN (10, 11, 12)) NOT NULL
                   )""")
    conn.commit()
    close_cursor()

def create_subjects_table():
    global cursor, conn
    create_cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS SUBJECTS (
                   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   NAME TEXT UNIQUE NOT NULL)""")
    
    subjects =['Trigonometry', 'Algebra', 'Physics', "Chemistrys", 'Computer Science']
    cursor.executemany("INSERT OR IGNORE INTO SUBJECTS (NAME) VALUES (?)", [(s,) for s in subjects])
    conn.commit()
    close_cursor()


def create_tasks_table():
    global cursor, conn
    create_cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS TASKS (
                   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   TITLE TEXT NOT NULL,
                   DESCRIPTION TEXT,
                   GRADE INTEGER CHECK(GRADE IN (10, 11, 12)) NOT NULL,
                   SUBJECT_ID INTEGER NOT NULL,
                   FOREIGN KEY(SUBJECT_ID) REFERENCES SUBJECTS(ID))""")
    conn.commit()
    close_cursor()

def create_completed_tasks_table():
    global cursor, conn
    create_cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS COMPLETED_TASKS (
                   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   USER_ID INTEGER NOT NULL,
                   TASK_ID INTEGER NOT NULL,
                   COMPLETED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(USER_ID) REFERENCES USER_TABLE(ID),
                   FOREIGN KEY(TASK_ID) REFERENCES TASKS(ID))""")

    conn.commit()
    close_cursor()

def create_questions_table():
    global cursor, conn
    create_cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS QUESTIONS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TASK_ID INTEGER NOT NULL,
        QUESTION_TEXT TEXT NOT NULL,
        OPTION_A TEXT NOT NULL,
        OPTION_B TEXT NOT NULL,
        OPTION_C TEXT NOT NULL,
        OPTION_D TEXT NOT NULL,
        CORRECT_OPTION TEXT NOT NULL,
        FOREIGN KEY(TASK_ID) REFERENCES TASKS(ID)
    )""")
    conn.commit()
    close_cursor()

def init_db():
    create_user_table()
    create_subjects_table()
    create_tasks_table()
    create_completed_tasks_table()
    create_questions_table()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, name, grade):
    global cursor, conn
    create_cursor()
    try:
        cursor.execute("INSERT INTO USER_TABLE (USERNAME, PASSWORD, NAME, GRADE) VALUES (?, ?, ?, ?)",
                       (username, hash_password(password), name, grade))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        close_cursor()

def login_user(username, password):
    global cursor, conn
    create_cursor()
    cursor.execute("SELECT ID, PASSWORD, USERNAME, GRADE FROM USER_TABLE WHERE USERNAME =?", (username,))
    row = cursor.fetchone()
    close_cursor()
    if row and row[1] == hash_password(password):
        return {"user_id" : row[0], "name" : row[2], "grade" : row[3]}
    return None

def add_problems(title, description, grade, subject_name):
    global cursor, conn
    create_cursor()

    cursor.execute("SELECT ID FROM SUBJECTS WHERE NAME = ?", (subject_name,))
    row = cursor.fetchone()

    if not row:
        close_cursor()
        return False
    subject_id = row[0]
    cursor.execute("INSERT INTO TASKS (TITLE, DESCRIPTION, GRADE, SUBJECT_ID) VALUES (?, ? ,?, ?)", (title, description, grade, subject_id))

    conn.commit()
    close_cursor()
    return True

def seed_data():
    global cursor, conn
    create_cursor()
    # This to help stop the seed data from getting add into the db again and again
    cursor.execute("SELECT COUNT(*) FROM TASKS")
    count = cursor.fetchone()[0]
    if count > 0:
        close_cursor()
        return

    # ---- Users ----
    users = [
        ("alice", hash_password("password123"), "Alice Johnson", 10),
        ("bob", hash_password("mypassword"), "Bob Smith", 11),
        ("charlie", hash_password("secretpass"), "Charlie Brown", 12),
    ]
    cursor.executemany("INSERT OR IGNORE INTO USER_TABLE (USERNAME, PASSWORD, NAME, GRADE) VALUES (?, ?, ?, ?)", users)

    # ---- Subjects (already added in create_subjects_table, but we ensure they exist) ----
    subjects = ['Trigonometry', 'Algebra', 'Physics', 'Chemistry', 'Computer Science']
    cursor.executemany("INSERT OR IGNORE INTO SUBJECTS (NAME) VALUES (?)", [(s,) for s in subjects])

    # ---- Tasks ----
    tasks = [
        # Grade 10
        ("Basic Trigonometric Ratios", "Learn sine, cosine, and tangent.", 10, "Trigonometry"),
        ("Graphing Trigonometric Functions", "Plot sine, cosine, and tangent graphs.", 10, "Trigonometry"),
        ("Quadratic Equations", "Solve quadratic equations using formula and factoring.", 10, "Algebra"),
        ("Linear Equations", "Solve and graph linear equations.", 10, "Algebra"),
        ("Newton’s Laws", "Understand the three laws of motion.", 10, "Physics"),
        ("Atomic Structure", "Learn protons, neutrons, and electrons.", 10, "Chemistry"),
        ("Basic Programming Concepts", "Understand variables, loops, and conditions.", 10, "Computer Science"),

        # Grade 11
        ("Trigonometric Identities", "Use fundamental identities to simplify expressions.", 11, "Trigonometry"),
        ("Complex Numbers", "Understand imaginary numbers and operations.", 11, "Algebra"),
        ("Projectile Motion", "Calculate range, height, and time of flight.", 11, "Physics"),
        ("Periodic Table", "Memorize groups and periods.", 11, "Chemistry"),
        ("Chemical Bonding", "Learn ionic, covalent, and metallic bonding.", 11, "Chemistry"),
        ("Data Structures", "Learn about arrays, stacks, and queues.", 11, "Computer Science"),

        # Grade 12
        ("Inverse Trigonometric Functions", "Understand and graph inverse trig functions.", 12, "Trigonometry"),
        ("Differentiation Basics", "Introduction to derivatives and slopes.", 12, "Algebra"),
        ("Electromagnetism", "Study magnetic fields and Faraday’s law.", 12, "Physics"),
        ("Organic Chemistry Basics", "Learn about hydrocarbons and functional groups.", 12, "Chemistry"),
        ("Sorting Algorithms", "Implement bubble sort and quicksort.", 12, "Computer Science"),
        ("Database Concepts", "Introduction to SQL and relational databases.", 12, "Computer Science"),
    ]


    for title, description, grade, subject in tasks:
        cursor.execute("SELECT ID FROM SUBJECTS WHERE NAME = ?", (subject,))
        row = cursor.fetchone()
        if row:
            subject_id = row[0]
            cursor.execute("INSERT OR IGNORE INTO TASKS (TITLE, DESCRIPTION, GRADE, SUBJECT_ID) VALUES (?, ?, ?, ?)",
                           (title, description, grade, subject_id))

    # ---- Completed Tasks ----
    completed = [
        (1, 1),  # Alice completed Trigonometry task
        (2, 3),  # Bob completed Physics task
        (3, 5),  # Charlie completed Sorting Algorithms task
    ]
    cursor.executemany("INSERT OR IGNORE INTO COMPLETED_TASKS (USER_ID, TASK_ID) VALUES (?, ?)", completed)

    conn.commit()
    close_cursor()


def get_tasks_by_grade(grade):
    global cursor, conn
    create_cursor()

    cursor.execute("""
        SELECT T.ID, T.TITLE, T.DESCRIPTION, S.NAME as SUBJECT
        FROM TASKS T
        JOIN SUBJECTS S ON T.SUBJECT_ID = S.ID
        WHERE T.GRADE = ?
        ORDER BY S.NAME ASC
        """, (int(grade),))
    tasks = cursor.fetchall()
    close_cursor()
    return tasks

def debug_show_all_tasks():
    create_cursor()
    cursor.execute("SELECT ID, TITLE, GRADE FROM TASKS")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    close_cursor()

# debug_show_all_tasks()

def get_completed_task_ids(user_id):
    global conn, cursor
    create_cursor()
    cursor.execute("""SELECT TASK_ID FROM COMPLETED_TASKS WHERE USER_ID = ?""", (user_id,))
    rows = cursor.fetchall()
    close_cursor()
    # Return a flat list of task IDs
    return [row[0] for row in rows]