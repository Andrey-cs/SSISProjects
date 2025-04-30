import tkinter as tk 
import ttkbootstrap as ttk 
from ..database import database  

class ProgramInfo(tk.Toplevel):
    def __init__(self, master, mode: str, data: dict = None):
        super().__init__(master=master)
        self.mode = mode
        self.data = data
        self.title('New Program' if mode == 'new' else 'Program Information')
        self.geometry('300x250')
        self.resizable(False, False)

        # Widgets
        ttk.Label(self, text="PROGRAM CODE").pack(pady=(10, 0))
        self.code_entry = ttk.Entry(self)
        self.code_entry.pack(fill='x', padx=10, pady=5)

        ttk.Label(self, text="PROGRAM NAME").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(fill='x', padx=10, pady=5)

        ttk.Label(self, text="COLLEGE CODE").pack(pady=(10, 0))
        self.college_combo = ttk.Combobox(self, values=[c['College Code'] for c in database.colleges.get_all()])
        self.college_combo.pack(fill='x', padx=10, pady=5)

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
            self.code_entry.insert(0, self.data['Program Code'])
            self.code_entry.config(state='disabled')
            self.name_entry.insert(0, self.data['Program Name'])
            self.college_combo.set(self.data['College Code'])

    def save(self):
        code = self.code_entry.get().strip().upper()
        name = self.name_entry.get().strip()
        college = self.college_combo.get().strip()

        if not all([code, name, college]):
            self.show_error("All fields are required!")
            return

        if self.mode == 'new':
            if database.programs.exists(code):
                self.show_error("Program code already exists!")
                return
            database.programs.add({
                'Program Code': code,
                'Program Name': name,
                'College Code': college
            })
        else:
            database.programs.update(code, {
                'Program Name': name,
                'College Code': college
            })

        if self.master and hasattr(self.master, 'refresh'):
            self.master.refresh()
        self.destroy()

    def show_error(self, message):
        error = ttk.Toplevel(self)
        error.title("Error")
        ttk.Label(error, text=message).pack(padx=20, pady=10)
        ttk.Button(error, text="OK", command=error.destroy).pack(pady=5)