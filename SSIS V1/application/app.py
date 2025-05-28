import tkinter as tk
import ttkbootstrap as ttk
from tkinter import font as tkfont # import para sa font
from .database import programs, students, colleges
from .informations import StudentInfo, ProgramInfo, CollegeInfo

class StudentTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(
            master=master,
            bootstyle='info',
            height=12,
            columns=('ID', 'FIRSTNAME', 'LASTNAME', 'SEX', 'PROGRAM', 'YEAR_LEVEL'),
            show='headings'
        )
        self.heading('ID', text='Student ID')
        self.heading('FIRSTNAME', text='First Name')
        self.heading('LASTNAME', text='Last Name')
        self.heading('SEX', text='Sex')
        self.heading('PROGRAM', text='Program')
        self.heading('YEAR_LEVEL', text='Year Level')
        self.column('ID', width=100, anchor='center')
        self.column('FIRSTNAME', width=150, anchor='w')
        self.column('LASTNAME', width=150, anchor='w')
        self.column('SEX', width=80, anchor='center')
        self.column('PROGRAM', width=120, anchor='w') # dakoon para sa program codes/names
        self.column('YEAR_LEVEL', width=100, anchor='center')

class ProgramTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(
            master=master,
            bootstyle='info',
            height=12,
            columns=('CODE', 'NAME', 'COLLEGE'),
            show='headings'
        )
        self.heading('CODE', text='Code')
        self.heading('NAME', text='Program Name')
        self.heading('COLLEGE', text='College')
        self.column('CODE', width=80, anchor='center')
        self.column('NAME', width=300, anchor='w')   # padakoon para sa long program names
        self.column('COLLEGE', width=280, anchor='w')

class CollegeTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(
            master=master,
            bootstyle='info',
            height=12,
            columns=('CODE', 'NAME'),
            show='headings'
        )
        self.heading('CODE', text='College Code')
        self.heading('NAME', text='College Name')
        self.column('CODE', width=100, anchor='center')
        self.column('NAME', width=550, anchor='w') # padakoon para sa long college names

class StudentInformationSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style("superhero")
        self.title("Simple Student Information System")
        self.resizable(False, False)
        window_width = 1000
        window_height = 650
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        title_font_family = "Montserrat"
        available_fonts = list(tkfont.families())
        # para sa title header
        self.style.configure("WhiteTitle.TLabel", foreground="white", font=(title_font_family, 25, 'bold'))
        main_title_label = ttk.Label(self, text="STUDENT  INFORMATION  SYSTEM", style="WhiteTitle.TLabel", anchor="center")
        main_title_label.pack(pady=(10,5), fill='x')
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(5,10))
        self.students_frame = ttk.Frame(self.notebook)
        self.program_frame = ttk.Frame(self.notebook)
        self.college_frame = ttk.Frame(self.notebook)
        
        # para sa tabs
        self.notebook.add(self.students_frame, text="Students")
        self.notebook.add(self.program_frame, text="Programs")
        self.notebook.add(self.college_frame, text="Colleges")
        self.setup_students_tab()
        self.setup_programs_tab()
        self.setup_colleges_tab()
        self.refresh_college_table()
        self.refresh_program_table()
        self.refresh_student_table()

    def setup_students_tab(self):
        self.student_buttons = ttk.Frame(self.students_frame)
        self.student_buttons.pack(side='left', fill='y', padx=10, pady=10)
        self.student_label = ttk.Label(self.student_buttons, text="STUDENTS", font=('Default', 15, 'bold'))
        self.student_label.pack(padx=10, pady=10)
        # size sa buttons
        self.new_student_button = ttk.Button(self.student_buttons, text="CREATE STUDENT", width=20, bootstyle="success", command=self.new_student_button_callback)
        self.new_student_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.edit_student_button = ttk.Button(self.student_buttons, text='EDIT STUDENT', width=20, bootstyle="info", command=self.edit_student_button_callback)
        self.edit_student_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.delete_student_button = ttk.Button(self.student_buttons, text='DELETE STUDENT', width=20, bootstyle="danger", command=self.delete_student_button_callback)
        self.delete_student_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.student_content = ttk.Frame(self.students_frame)
        self.student_content.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        self.search_frame = ttk.Frame(self.student_content)
        self.search_frame.pack(fill='x', pady=(0,10))
        self.search_label = ttk.Label(self.search_frame, text="Search:", font=('Default', 10))
        self.search_label.pack(side='left', padx=5)
        self.student_key_search = tk.StringVar()
        self.student_search_tab = ttk.Entry(self.search_frame, width=50, textvariable=self.student_key_search)
        self.student_search_tab.pack(side='left', fill='x', expand=True, padx=5)
        self.students_table = StudentTable(self.student_content)
        self.students_table.pack(fill='both', expand=True)
        self.student_key_search.trace_add("write", self.student_search)

    def setup_programs_tab(self):
        self.program_buttons = ttk.Frame(self.program_frame)
        self.program_buttons.pack(side='right', fill='y', padx=10, pady=10)
        self.program_label = ttk.Label(self.program_buttons, text="PROGRAMS", font=('Default', 15, 'bold'))
        self.program_label.pack(padx=10, pady=10)
        # function buttons for program
        self.new_program_button = ttk.Button(self.program_buttons, text="CREATE PROGRAM", width=20, bootstyle="success", command=self.new_program_button_callback)
        self.new_program_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.edit_program_button = ttk.Button(self.program_buttons, text='EDIT PROGRAM', width=20, bootstyle="info", command=self.edit_program_button_callback)
        self.edit_program_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.delete_program_button = ttk.Button(self.program_buttons, text='DELETE PROGRAM', width=20, bootstyle="danger", command=self.delete_program_button_callback)
        self.delete_program_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.program_content = ttk.Frame(self.program_frame)
        self.program_content.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.program_search_frame = ttk.Frame(self.program_content)
        self.program_search_frame.pack(fill='x', pady=(0,10))
        self.program_search_label = ttk.Label(self.program_search_frame, text="Search:", font=('Default', 10))
        self.program_search_label.pack(side='left', padx=5)
        self.program_key_search = tk.StringVar()
        self.program_search_tab = ttk.Entry(self.program_search_frame, width=50, textvariable=self.program_key_search)
        self.program_search_tab.pack(side='left', fill='x', expand=True, padx=5)
        self.program_table = ProgramTable(self.program_content)
        self.program_table.pack(fill='both', expand=True)
        self.program_key_search.trace_add("write", self.program_search)

    def setup_colleges_tab(self):
        self.college_buttons = ttk.Frame(self.college_frame)
        self.college_buttons.pack(side='right', fill='y', padx=10, pady=10)
        self.college_label = ttk.Label(self.college_buttons, text="COLLEGES", font=('Default', 15, 'bold'))
        self.college_label.pack(padx=10, pady=10)
        # buttons for college tab
        self.new_college_button = ttk.Button(self.college_buttons, text="CREATE COLLEGE", width=20, bootstyle="success", command=self.new_college_button_callback)
        self.new_college_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.edit_college_button = ttk.Button(self.college_buttons, text='EDIT COLLEGE', width=20, bootstyle="info", command=self.edit_college_button_callback)
        self.edit_college_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.delete_college_button = ttk.Button(self.college_buttons, text='DELETE COLLEGE', width=20, bootstyle="danger", command=self.delete_college_button_callback)
        self.delete_college_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.college_content = ttk.Frame(self.college_frame)
        self.college_content.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.college_search_frame = ttk.Frame(self.college_content)
        self.college_search_frame.pack(fill='x', pady=(0,10))
        self.college_search_label = ttk.Label(self.college_search_frame, text="Search:", font=('Default', 10))
        self.college_search_label.pack(side='left', padx=5)
        self.college_key_search = tk.StringVar()
        self.college_search_tab = ttk.Entry(self.college_search_frame, width=50, textvariable=self.college_key_search)
        self.college_search_tab.pack(side='left', fill='x', expand=True, padx=5)
        self.college_table = CollegeTable(self.college_content)
        self.college_table.pack(fill='both', expand=True)
        self.college_key_search.trace_add("write", self.college_search)

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
        message_frame = ttk.Frame(toplevel, padding=(20, 20))
        message_frame.pack(fill='both', expand=True)
        msg_label = ttk.Label(message_frame, text=text, wraplength=window_width-60, justify='center', anchor='center')
        msg_label.pack(expand=True, fill='both', pady=(0,15))
        button_frame = ttk.Frame(message_frame)
        button_frame.pack(side='bottom', pady=(0,5))
        ok_button = ttk.Button(button_frame, text='Ok', bootstyle="primary", width=10, command=toplevel.destroy)
        ok_button.pack()
        toplevel.grab_set()

    def confirmation(self, text, func, title="Confirmation"):
        toplevel = ttk.Toplevel(self)
        toplevel.title(title)
        toplevel.transient(self)
        window_width = 380
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        toplevel.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        def confirmed_action():
            func()
            toplevel.destroy()
        message_frame = ttk.Frame(toplevel, padding=(20,20))
        message_frame.pack(fill='both', expand=True)
        msg_label = ttk.Label(message_frame, text=text, wraplength=window_width-60, justify='center', anchor='center')
        msg_label.pack(expand=True, fill='both', pady=(0,15))
        button_frame = ttk.Frame(message_frame)
        button_frame.pack(side='bottom', pady=(0,5))
        yes_button = ttk.Button(button_frame, text="Yes", bootstyle="primary", width=10, command=confirmed_action)
        yes_button.pack(side='left', padx=(0,10))
        cancel_button = ttk.Button(button_frame, text="Cancel", bootstyle="secondary", width=10, command=toplevel.destroy)
        cancel_button.pack(side='right')
        toplevel.grab_set()

    # FUNCTIONS PARA SA STUDENT TAB
    def student_search(self, *args):
        self.refresh_student_table(self.student_key_search.get())

    def refresh_student_table(self, keyword=None):
        for item in self.students_table.get_children():
            self.students_table.delete(item)
        all_student_data = students.get_all()
        valid_program_ids = programs.get_program_ids()
        for idx, student_record in enumerate(all_student_data):
            if not isinstance(student_record, dict): continue
            if keyword:
                keyword_upper = keyword.upper()
                match_found = False
                for value in student_record.values():
                    if keyword_upper in str(value).upper():
                        match_found = True
                        break
                if not match_found: continue
            student_program_code = student_record.get("PROGRAM")
            program_display_name = "NOT ENROLLED"
            if student_program_code and student_program_code in (valid_program_ids[1:] if valid_program_ids and valid_program_ids[0] == "No Selection" else valid_program_ids):
                program_display_name = student_program_code
            elif not student_program_code or student_program_code.strip() == "":
                program_display_name = "NOT ASSIGNED"
            self.students_table.insert('', 'end', iid=f"student_{idx}", values=(
                student_record.get("ID", "N/A"), student_record.get("FIRSTNAME", ""),
                student_record.get("LASTNAME", ""), student_record.get("SEX", ""),
                program_display_name, student_record.get("YEAR LEVEL", "")))

    def new_student_button_callback(self): StudentInfo(self, 'new')

    def edit_student_button_callback(self):
        selected_item = self.students_table.selection()
        if not selected_item: return self.dialog("Please select a student from the table first.")
        values = self.students_table.item(selected_item[0], 'values')
        StudentInfo(self, 'edit', {"ID": values[0], "FIRSTNAME": values[1], "LASTNAME": values[2],
                                    "SEX": values[3], "PROGRAM": values[4], "YEAR LEVEL": values[5]})

    def delete_student_data(self):
        selected_item = self.students_table.selection()
        if not selected_item: return
        student_id = self.students_table.item(selected_item[0], 'values')[0]
        students.remove(student_id)
        self.dialog(f"Successfully deleted Student #{student_id}")
        self.refresh_student_table()

    def delete_student_button_callback(self):
        selected_item = self.students_table.selection()
        if not selected_item: return self.dialog("Please select a student from the table first.")
        student_id = self.students_table.item(selected_item[0], 'values')[0]
        self.confirmation(f"Do you want to delete student #{student_id}?", self.delete_student_data)

    # FUNCTIONS PARA SA PROGRAM TAB
    def program_search(self, *args): self.refresh_program_table(self.program_key_search.get())

    def refresh_program_table(self, keyword=None):
        for item in self.program_table.get_children(): self.program_table.delete(item)
        all_program_data = programs.get_all()
        if not isinstance(all_program_data, list): all_program_data = []
        all_colleges_data = colleges.get_all()
        college_code_to_name_map = {c.get("ID"): c.get("NAME", "Unknown College") for c in all_colleges_data if isinstance(c, dict) and c.get("ID")}
        for idx, program_record in enumerate(all_program_data):
            if not isinstance(program_record, dict): continue
            program_college_code = program_record.get("COLLEGE", "")
            college_display_name = college_code_to_name_map.get(program_college_code, "N/A" if not program_college_code else f"Unknown Code: {program_college_code}")
            if keyword:
                keyword_upper = keyword.upper()
                if not (keyword_upper in str(program_record.get("ID", "")).upper() or \
                        keyword_upper in str(program_record.get("NAME", "")).upper() or \
                        keyword_upper in str(college_display_name).upper()):
                    continue
            self.program_table.insert('', 'end', iid=f"program_{idx}", values=(
                program_record.get("ID", "N/A"), program_record.get("NAME", ""), college_display_name))

    def new_program_button_callback(self): ProgramInfo(self, 'new')

    def edit_program_button_callback(self):
        selected_item = self.program_table.selection()
        if not selected_item: return self.dialog("Please select a program from the table first.")
        values = self.program_table.item(selected_item[0], 'values')
        program_id_val, name_val, _ = values
        original_program_data = next((p for p in programs.get_all() if p.get("ID") == program_id_val), None)
        college_code_for_edit = original_program_data.get("COLLEGE", "") if original_program_data else ""
        ProgramInfo(self, 'edit', {"ID": program_id_val, "NAME": name_val, "COLLEGE": college_code_for_edit})

    def delete_program_data(self):
        selected_item = self.program_table.selection()
        if not selected_item: return
        program_id = self.program_table.item(selected_item[0], 'values')[0]
        
        students_to_delete = [s for s in students.get_all() if s.get("PROGRAM") == program_id]
        for stud in students_to_delete:
            students.remove(stud.get("ID"))

        programs.remove(program_id)
        self.dialog(f"Successfully deleted the Program {program_id} and all its associated students.")
        self.refresh_student_table()
        self.refresh_program_table()

    def delete_program_button_callback(self):
        selected_item = self.program_table.selection()
        if not selected_item: return self.dialog("Please select a program from the table first.")
        program_id = self.program_table.item(selected_item[0], 'values')[0]
        self.confirmation(f"Do you want to delete Program {program_id}?", self.delete_program_data)

    # FUNCTIONS FOR COLLEGE TAB
    def college_search(self, *args): self.refresh_college_table(self.college_key_search.get())

    def refresh_college_table(self, keyword=None):
        self.college_table.delete(*self.college_table.get_children())
        data = colleges.get_all()
        for idx, college in enumerate(data):
            if not isinstance(college, dict): continue
            if keyword is not None:
                keyword_upper = keyword.upper()
                if not any(keyword_upper in str(x).upper() for x in college.values()): continue
            self.college_table.insert('', 'end', iid=f"college_{idx}", values=[
                college.get("ID", "N/A"), college.get("NAME", "")])

    def new_college_button_callback(self): CollegeInfo(self, 'new')

    def edit_college_button_callback(self):
        selected_item = self.college_table.selection()
        if not selected_item: return self.dialog("Please select a college from the table first.")
        values = self.college_table.item(selected_item[0], 'values')
        CollegeInfo(self, 'edit', {"ID": values[0], "NAME": values[1]})

    def delete_college_data(self):
        selected_item = self.college_table.selection()
        if not selected_item: return
        college_id = self.college_table.item(selected_item[0], 'values')[0]

        programs_to_delete = [p for p in programs.get_all() if p.get("COLLEGE") == college_id]

        for prog in programs_to_delete:
            program_id_to_delete = prog.get("ID")
            students_in_program = [s for s in students.get_all() if s.get("PROGRAM") == program_id_to_delete]
            for stud in students_in_program:
                students.remove(stud.get("ID"))
            
            programs.remove(program_id_to_delete)

        colleges.remove(college_id)
        self.dialog(f"Successfully deleted College {college_id} and all its associated programs and students.")
        self.refresh_student_table() 
        self.refresh_program_table() 
        self.refresh_college_table() 

    def delete_college_button_callback(self):
        selected_item = self.college_table.selection()
        if not selected_item: return self.dialog("Please select a college from the table first.")
        college_id = self.college_table.item(selected_item[0], 'values')[0]
        self.confirmation(f"Do you want to delete college {college_id}?", self.delete_college_data)
        
    def start(self):
        self.mainloop()