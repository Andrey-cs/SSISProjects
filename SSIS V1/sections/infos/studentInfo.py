import tkinter as tk
import ttkbootstrap as ttk
from ..database import database

class StudentInfo(tk.Toplevel):
    def __init__(self, master, mode: str, data: dict = None):
        super().__init__(master=master)
        self.mode = mode
        self.data = data
        self.title('New Student' if mode == 'new' else 'Student Information')
        self.geometry('350x500')
        self.resizable(False, False)

        # Widgets
        fields = [
            ("ID NUMBER", 'id_entry'),
            ("FIRST NAME", 'first_name_entry'),
            ("LAST NAME", 'last_name_entry'),
            ("SEX", 'sex_combo', ["Male", "Female"]),
            ("AGE", 'age_entry'),
            ("PROGRAM", 'program_combo', [p['Program Code'] for p in database.programs.get_all()]),
            ("YEAR LEVEL", 'year_combo', ["1", "2", "3", "4"])
        ]

        for field in fields:
            ttk.Label(self, text=field[0]).pack(pady=(10, 0))
            if len(field) == 2:
                entry = ttk.Entry(self, name=field[1])
                entry.pack(fill='x', padx=10, pady=5)
            else:
                combo = ttk.Combobox(self, values=field[2], name=field[1])
                combo.pack(fill='x', padx=10, pady=5)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(
            btn_frame, 
            text="Save" if mode == 'edit' else "Create",
            command=self.save,
            bootstyle='success'
        ).pack(side='left', padx=5)
        ttk.Button(
            btn_frame, 
            text="Cancel",
            command=self.destroy,
            bootstyle='danger'
        ).pack(side='right', padx=5)

        # Pre-fill if editing
        if self.data:
            self.children['id_entry'].insert(0, self.data['ID'])
            if mode == 'edit':
                self.children['id_entry'].config(state='disabled')
            self.children['first_name_entry'].insert(0, self.data['First Name'])
            self.children['last_name_entry'].insert(0, self.data['Last Name'])
            self.children['sex_combo'].set(self.data['Sex'])
            self.children['age_entry'].insert(0, self.data['Age'])
            self.children['program_combo'].set(self.data['Program Code'])
            self.children['year_combo'].set(self.data['Year Level'])

    def save(self):
        data = {
            'ID': self.children['id_entry'].get().strip(),
            'First Name': self.children['first_name_entry'].get().strip(),
            'Last Name': self.children['last_name_entry'].get().strip(),
            'Sex': self.children['sex_combo'].get().strip(),
            'Age': self.children['age_entry'].get().strip(),
            'Program Code': self.children['program_combo'].get().strip(),
            'Year Level': self.children['year_combo'].get().strip()
        }

        if not all(data.values()):
            self.show_error("All fields are required!")
            return

        if not database.validate_student_id(data['ID']):
            self.show_error("Invalid ID format (YYYY-NNNN required)!")
            return

        if self.mode == 'new':
            if database.students.exists(data['ID']):
                self.show_error("Student ID already exists!")
                return
            database.students.add(data)
        else:
            database.students.update(data['ID'], data)

        if self.master and hasattr(self.master, 'refresh'):
            self.master.refresh()
        self.destroy()

    def show_error(self, message):
        error = ttk.Toplevel(self)
        error.title("Error")
        ttk.Label(error, text=message).pack(padx=20, pady=10)
        ttk.Button(error, text="OK", command=error.destroy).pack(pady=5)