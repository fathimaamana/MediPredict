import sqlite3

def create_table():
    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        dob TEXT,
        email TEXT,
        glucose REAL,
        haemoglobin REAL,
        cholesterol REAL,
        remarks TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_patient(data):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients
    (fullname,dob,email,glucose,haemoglobin,cholesterol,remarks)
    VALUES(?,?,?,?,?,?,?)
    """, data)

    conn.commit()
    conn.close()


def view_all():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_patient(id):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()


def update_patient(data):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE patients
    SET fullname=?,
        dob=?,
        email=?,
        glucose=?,
        haemoglobin=?,
        cholesterol=?,
        remarks=?
    WHERE id=?
    """, data)

    conn.commit()
    conn.close()


def get_next_patient_id():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT MAX(id) FROM patients")

    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return 1

    return result + 1

def get_patients():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, fullname FROM patients"
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_patient_by_id(patient_id):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE id=?",
        (patient_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row