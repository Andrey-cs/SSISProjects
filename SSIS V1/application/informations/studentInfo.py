import tkinter as tk
import ttkbootstrap as ttk
from ..database import programs, students

class StudentInfo(ttk.Toplevel):
    def __init__(self, master, mode: str, data: dict=None):
        super().__init__(master=master)
        self.data = data
        self.mode = mode
        self.transient(master)

        window_width = 380
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.title('New Student' if mode == 'new' else 'Student Information')

        form_frame = ttk.Frame(self, padding=20)
        form_frame.pack(fill='both', expand=True)

        ttk.Label(form_frame, text="STUDENT ID (YYYY-NNNN)", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.id_entry = ttk.Entry(form_frame)
        self.id_entry.pack(padx=0, fill='x', pady=(0,10))

        ttk.Label(form_frame, text="FIRST NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.firstname_entry = ttk.Entry(form_frame)
        self.firstname_entry.pack(padx=0, fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="LAST NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.lastname_entry = ttk.Entry(form_frame)
        self.lastname_entry.pack(padx=0, fill='x', pady=(0,10))

        ttk.Label(form_frame, text="SEX", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.sex_values = ["NO SELECTION", "MALE", "FEMALE", "PREFER NOT TO SAY"]
        self.sex_option = ttk.Combobox(form_frame, values=self.sex_values, state='readonly')
        self.sex_option.pack(fill='x', padx=0, pady=(0,10))
        
        ttk.Label(form_frame, text="PROGRAM", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        raw_program_ids = [str(pid) for pid in programs.get_program_ids() if pid] 
        self.program_ids_list = []
        has_no_selection_prog = any(pid.upper() == "NO SELECTION" for pid in raw_program_ids)

        if has_no_selection_prog:
            for pid in raw_program_ids:
                self.program_ids_list.append(pid.upper() if pid.upper() == "NO SELECTION" else pid)
        else:
            self.program_ids_list = ["NO SELECTION"] + raw_program_ids
        self.program_ids_list = list(dict.fromkeys(self.program_ids_list)) 

        self.program_option = ttk.Combobox(form_frame, values=self.program_ids_list, state='readonly')
        self.program_option.pack(fill='x', padx=0, pady=(0,10))

        ttk.Label(form_frame, text="YEAR LEVEL", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.year_level_values = ["NO SELECTION", "FIRST YEAR", "SECOND YEAR", "THIRD YEAR", "FOURTH YEAR", "FIFTH YEAR", "IRREGULAR"]
        self.yearlevel_option = ttk.Combobox(form_frame, values=self.year_level_values, state='readonly')
        self.yearlevel_option.pack(fill='x', padx=0, pady=(0,20))

        self.buttons_frame = ttk.Frame(form_frame)
        self.create_button = ttk.Button(self.buttons_frame, text="Create" if mode == 'new' else 'Save Changes', width=15, bootstyle="success" if mode == 'new' else "primary", command=self.create_button_callback)
        self.create_button.pack(side='left', fill='x', expand=True, padx=(0,5), ipady=3)
        
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", width=15, bootstyle="secondary", command=self.destroy)
        self.cancel_button.pack(side='right', fill='x', expand=True, padx=(5,0), ipady=3)
        self.buttons_frame.pack(side='bottom', padx=0, pady=(10,0), fill='x')

        if self.data is not None: 
            self.id_entry.insert(0, self.data.get('ID',''))
            self.id_entry.configure(state='disabled')
            self.firstname_entry.insert(0, self.data.get("FIRSTNAME",''))
            self.lastname_entry.insert(0, self.data.get("LASTNAME",''))
            
            sex_val_from_data = str(self.data.get("SEX", "NO SELECTION")).strip()
            if sex_val_from_data and sex_val_from_data in self.sex_values:
                self.sex_option.set(sex_val_from_data)
            else:
                self.sex_option.set("NO SELECTION") 
            
            if self.mode == 'edit':
                self.sex_option.configure(state='disabled') 
            
            program_val_from_data = str(self.data.get("PROGRAM", "NO SELECTION")).strip()
            if program_val_from_data and program_val_from_data in self.program_option['values']: 
                self.program_option.set(program_val_from_data)
            else:
                self.program_option.set("NO SELECTION")
            
            year_level_val_from_data = str(self.data.get("YEAR LEVEL", "NO SELECTION")).strip()
            if year_level_val_from_data and year_level_val_from_data in self.year_level_values:
                self.yearlevel_option.set(year_level_val_from_data)
            else:
                self.yearlevel_option.set("NO SELECTION")
        else: 
            self.sex_option.set("NO SELECTION") 
            self.program_option.set("NO SELECTION")
            self.yearlevel_option.set("NO SELECTION")
            
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
        stud_id = self.id_entry.get().strip()
        firstname = self.firstname_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        
        sex = self.sex_option.get() 
        program_code = self.program_option.get()
        year_level = self.yearlevel_option.get()

        selected_sex = sex if sex != "NO SELECTION" else ""
        selected_program = program_code if program_code != "NO SELECTION" else "" 
        selected_year_level = year_level if year_level != "NO SELECTION" else ""

        if not (len(stud_id) == 9 and stud_id[4] == '-' and stud_id[:4].isdigit() and stud_id[5:].isdigit()):
             return self.dialog("Invalid Student ID format.\nExpected: YYҮY-NNNN (e.g., 2023-0001)", "Input Error")
        
        current_data = {
            "ID": stud_id, 
            "FIRSTNAME": firstname, 
            "LASTNAME": lastname, 
            "PROGRAM": selected_program, 
            "YEAR LEVEL": selected_year_level
        }
        
        if self.mode == 'edit' and self.data:
            current_data["SEX"] = self.data.get("SEX", "") 
        else: 
            current_data["SEX"] = selected_sex

        if not stud_id or not firstname or not lastname:
            return self.dialog("Student ID, First Name, and Last Name are required.\nPlease try again.", "Input Error")

        if self.mode == 'new':
            if students.check(stud_id): return self.dialog("Student ID already exists!", "Error")
            students.insert_one(current_data) 
            self.dialog(f"Successfully created Student #{stud_id}", "Success")
            if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
            self.destroy()
        else: 
            changed = False
            if self.data:
                for key in ["FIRSTNAME", "LASTNAME", "PROGRAM", "YEAR LEVEL"]: 
                    if self.data.get(key, "") != current_data.get(key, ""): 
                        changed = True
                        break
            else: 
                changed = True 

            if not changed: 
                 return self.dialog("No changes were made to the fields.\nPlease try again.", "Information")
            
            students.edit(current_data) 
            self.dialog(f"Successfully updated Student #{stud_id}", "Success") 
            if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
            self.destroy()