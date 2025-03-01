# FOR DATABASE

import pandas as pd
import os

# File paths
STUDENTS_FILE = "database/studentsinfoGUIfinal.csv"
PROGRAMS_FILE = "database/programsinfoGUIfinal.csv"
COLLEGES_FILE = "database/collegesinfoGUIfinal.csv"

# Ensure CSV files exist
if not os.path.exists(STUDENTS_FILE):
    pd.DataFrame(columns=["Student ID", "First Name", "Last Name", "Age", "Sex", "Program", "Year Level", "College"]).to_csv(STUDENTS_FILE, index=False)

if not os.path.exists(PROGRAMS_FILE):
    programs_data = {
        "Program Code": ["BSBIO-BOT", "BSBIO-ZOO", "BSMATH", "BSCS", "BSIT", "BSCE", "BSECE", "BAPOLSCI", "BSPSY", "BSEDBIO", "BPED", "BSA", "BSHM", "BSN"],
        "Program Name": [
            "BS Biology (Botany)", "BS Biology (Zoology)", "BS Mathematics", "BS Computer Science", "BS Information Technology",
            "BS Civil Engineering", "BS Electronics and Communication Engineering", "BA Political Science", "BS Psychology",
            "BSED Biology", "Bachelor of Physical Education", "BS Accountancy", "BS Hospitality Management", "BS Nursing"
        ],
        "College Code": ["CSM", "CSM", "CSM", "CCS", "CCS", "COE", "COE", "CASS", "CASS", "CED", "CED", "CEBA", "CEBA", "CHS"],
        "College Name": [
            "College of Science and Mathematics", "College of Science and Mathematics", "College of Science and Mathematics",
            "College of Computer Sciences", "College of Computer Sciences", "College of Engineering", "College of Engineering",
            "College of Arts and Social Sciences", "College of Arts and Social Sciences", "College of Education", "College of Education",
            "College of Economics and Business Administration", "College of Economics and Business Administration", "College of Health Sciences"
        ]
    }
    pd.DataFrame(programs_data).to_csv(PROGRAMS_FILE, index=False)

if not os.path.exists(COLLEGES_FILE):
    colleges_data = {
        "College Code": ["CSM", "CCS", "COE", "CASS", "CED", "CEBA", "CHS"],
        "College Name": [
            "College of Science and Mathematics", "College of Computer Sciences", "College of Engineering",
            "College of Arts and Social Sciences", "College of Education", "College of Economics and Business Administration",
            "College of Health Sciences"
        ]
    }
    pd.DataFrame(colleges_data).to_csv(COLLEGES_FILE, index=False)

def load_students():
    return pd.read_csv(STUDENTS_FILE)

def save_students(df):
    df.to_csv(STUDENTS_FILE, index=False)

def add_student(student_data):
    df = load_students()
    df = df.append(student_data, ignore_index=True)
    save_students(df)

def update_student(student_id, updated_data):
    df = load_students()
    df.loc[df["Student ID"] == student_id, list(updated_data.keys())] = list(updated_data.values())
    save_students(df)

def delete_student(student_id):
    df = load_students()
    df = df[df["Student ID"] != student_id]
    save_students(df)

def get_student(student_id):
    df = load_students()
    return df[df["Student ID"] == student_id].to_dict("records")[0]

def list_students():
    return load_students()

def load_programs():
    return pd.read_csv(PROGRAMS_FILE)

def load_colleges():
    return pd.read_csv(COLLEGES_FILE)
