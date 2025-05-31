import tkinter as tk
import ttkbootstrap as ttk
from ..database import programs, students

class StudentInfo(ttk.Toplevel):
    def __init__(self, master, mode: str, data: dict=None): 
        super().__init__(master=master)
        self.data = data # values for studentID, FIRSTNAME, LASTNAME, SEX, programCODE, YEAR LEVEL
        self.mode = mode
        self.transient(master)
        window_width = 380
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.title('New Student' if mode == 'new' else 'Edit Student Information')
        form_frame = ttk.Frame(self, padding=20)
        form_frame.pack(fill='both', expand=True)

        ttk.Label(form_frame, text="STUDENT ID (YYYY-NNNN)", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.id_entry = ttk.Entry(form_frame) # studentID
        self.id_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="FIRST NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.firstname_entry = ttk.Entry(form_frame) # FIRSTNAME
        self.firstname_entry.pack(padx=0, fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="LAST NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.lastname_entry = ttk.Entry(form_frame) # LASTNAME
        self.lastname_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="SEX", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        sex_values = ["No Selection", "Male", "Female", "Prefer not to say"]
        self.sex_option = ttk.Combobox(form_frame, values=sex_values, state='readonly') # SEX
        self.sex_option.pack(fill='x', padx=0, pady=(0,10))
        
        ttk.Label(form_frame, text="PROGRAM", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        program_codes_list = [pcode for pcode in programs.get_program_ids() if pcode] 
        if not program_codes_list or program_codes_list[0] != "No Selection":
            program_codes_list.insert(0, "No Selection")
        self.program_option = ttk.Combobox(form_frame, values=program_codes_list, state='readonly') # programCODE
        self.program_option.pack(fill='x', padx=0, pady=(0,10))

        ttk.Label(form_frame, text="YEAR LEVEL", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        year_level_values = ["No Selection", "First Year", "Second Year", "Third Year", "Fourth Year"]
        self.yearlevel_option = ttk.Combobox(form_frame, values=year_level_values, state='readonly') # YEAR LEVEL
        self.yearlevel_option.pack(fill='x', padx=0, pady=(0,20))
        
        self.buttons_frame = ttk.Frame(form_frame)
        self.create_button = ttk.Button(self.buttons_frame, text="Create" if mode == 'new' else 'Save Changes', width=15, bootstyle="success" if mode == 'new' else "primary", command=self.create_button_callback)
        self.create_button.pack(side='left', fill='x', expand=True, padx=(0,5), ipady=3)
        
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", width=15, bootstyle="secondary", command=self.destroy)
        self.cancel_button.pack(side='right', fill='x', expand=True, padx=(5,0), ipady=3)
        self.buttons_frame.pack(side='bottom', padx=0, pady=(10,0), fill='x')

        if self.data is not None: # Editing existing student
            self.id_entry.insert(0, self.data.get('studentID',''))
            self.id_entry.configure(state='disabled') # ID is disabled or read-only when editing
            self.firstname_entry.insert(0, self.data.get("FIRSTNAME",''))
            self.lastname_entry.insert(0, self.data.get("LASTNAME",''))
            
            sex_val = self.data.get("SEX", "No Selection")
            self.sex_option.set(sex_val if sex_val in sex_values else "No Selection")
            if self.mode == 'edit':
                self.sex_option.configure(state='disabled')  # Setting Sex Combobox to disabled or read-only if editing
            
            program_code_val = self.data.get("programCODE", "No Selection") # Using SQL column name
            self.program_option.set(program_code_val if program_code_val in program_codes_list else "No Selection")
            
            year_level_val = self.data.get("YEAR LEVEL", "No Selection") # Use SQL column name (with space)
            self.yearlevel_option.set(year_level_val if year_level_val in year_level_values else "No Selection")
        else: # New student
            self.sex_option.set("No Selection") 
            self.program_option.set("No Selection")
            self.yearlevel_option.set("No Selection")
            # Para sa new student, sex_option remains 'readonly' as set during creation.
        self.grab_set()

    def dialog(self, text, title="Message"):
        toplevel = ttk.Toplevel(self)
        toplevel.title(title)
        toplevel.transient(self)
        window_width = 350
        window_height = 180
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        toplevel.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        
        outer_frame = ttk.Frame(toplevel)
        outer_frame.pack(expand=True, fill='both', padx=10, pady=10)
        msg_label = ttk.Label(outer_frame, text=text, wraplength=window_width-60, justify='center', anchor='center')
        msg_label.pack(expand=True, fill='both', pady=(0,15)) 
        button_frame = ttk.Frame(outer_frame)
        button_frame.pack(side='bottom', pady=(0,5)) 
        ok_button = ttk.Button(button_frame, text='Ok', width=10, command=toplevel.destroy, bootstyle="primary")
        ok_button.pack() 
        toplevel.grab_set()

    def create_button_callback(self):
        stud_id_val = self.id_entry.get().strip() 
        firstname_val = self.firstname_entry.get().strip() 
        lastname_val = self.lastname_entry.get().strip()
        
        # For sex, if in 'edit' mode and disabled, get its current value.
        # If maghimog bago, makuha from combobox.
        sex_from_option = self.sex_option.get()       
        program_code_from_option = self.program_option.get()
        year_level_from_option = self.yearlevel_option.get()

        # Store None in DB if "No Selection" or empty, which is good for SQL NULLable fields
        db_sex = sex_from_option if sex_from_option != "No Selection" else None
        db_program_code = program_code_from_option if program_code_from_option != "No Selection" else None
        db_year_level = year_level_from_option if year_level_from_option != "No Selection" else None

        if not (len(stud_id_val) == 9 and stud_id_val[4] == '-' and stud_id_val[:4].isdigit() and stud_id_val[5:].isdigit()):
            return self.dialog("Invalid Student ID format.\nExpected: YYYY-NNNN (e.g., 2023-0001)", "Input Error") # Completed the error message
        
        # --- CRITICAL CHANGE: Data dictionary keys match SQL column names for DB operations ---
        current_data_payload = {
            "studentID": stud_id_val, 
            "FIRSTNAME": firstname_val, 
            "LASTNAME": lastname_val, 
            "programCODE": db_program_code, 
            "YEAR LEVEL": db_year_level # SQL column name with space
        }

        if self.mode == 'edit' and self.data:
            # Sex is disabled in edit mode, so use the original value from self.data
            # Ensure self.data.get("SEX") is what was originally fetched (could be None or a value)
            current_data_payload["SEX"] = self.data.get("SEX") 
        else: # New mode
            current_data_payload["SEX"] = db_sex
        
        if not stud_id_val or not firstname_val or not lastname_val:
            return self.dialog("Student ID, First Name, and Last Name are required.", "Input Error")
        
        if self.mode == 'new':
            if students.check(stud_id_val): return self.dialog("Student ID already exists!", "Error")
            students.insert_one(current_data_payload)
            self.dialog(f"Successfully created Student #{stud_id_val}", "Success")
            if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
            self.destroy()
        else: # Edit mode
            changed = False
            original_student_id = self.data.get("studentID") # ID doesn't change

            # Compare current form values (for editable fields) with original data from self.data
            if self.data:
                if firstname_val != self.data.get("FIRSTNAME", "") or \
                   lastname_val != self.data.get("LASTNAME", "") or \
                   db_program_code != self.data.get("programCODE") or \
                   db_year_level != self.data.get("YEAR LEVEL"):
                    changed = True
                # Note: SEX is not editable in the form in edit mode, so it's not part of "changed" check from form.
                # The original requirement "Also e check if ID kay mag match, just in case." is implicitly handled
                # as we are fetching by ID for edit and the ID field is disabled.
            else: 
                changed = True # Should not happen in edit mode if self.data is always present
            
            if not changed: 
                return self.dialog("No changes were made to the fields.\nPlease try again.", "Information")

            # Payload for edit should use the original studentID
            edit_payload = {
                "studentID": original_student_id, 
                "FIRSTNAME": firstname_val,
                "LASTNAME": lastname_val,
                "programCODE": db_program_code,
                "YEAR LEVEL": db_year_level
                # SEX is not updated from form in edit mode as it's disabled. It's taken from self.data if needed by edit.
                # The students.edit() in database.py will update fields present in the payload.
            }
            students.edit(edit_payload)
            self.dialog(f"Successfully updated the Student #{original_student_id}", "Success")
            if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
            self.destroy()