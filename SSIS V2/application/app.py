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
            # Treeview columns can have generic names for display
            columns=('ID_Display', 'FIRSTNAME_Display', 'LASTNAME_Display', 'SEX_Display', 'PROGRAM_Display', 'YEAR_LEVEL_Display'),
            show='headings'
        )
        # Headings match the display names
        self.heading('ID_Display', text='Student ID')
        self.heading('FIRSTNAME_Display', text='First Name')
        self.heading('LASTNAME_Display', text='Last Name')
        self.heading('SEX_Display', text='Sex')
        self.heading('PROGRAM_Display', text='Program')
        self.heading('YEAR_LEVEL_Display', text='Year Level')

        self.column('ID_Display', width=100, anchor='center')
        self.column('FIRSTNAME_Display', width=150, anchor='center')
        self.column('LASTNAME_Display', width=150, anchor='center')
        self.column('SEX_Display', width=80, anchor='center')
        self.column('PROGRAM_Display', width=120, anchor='center') # dakoon para sa program codes/names
        self.column('YEAR_LEVEL_Display', width=100, anchor='center')

class ProgramTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(
            master=master,
            bootstyle='info',
            height=12,
            columns=('CODE_Display', 'NAME_Display', 'COLLEGE_Display'),
            show='headings'
        )
        self.heading('CODE_Display', text='Code')
        self.heading('NAME_Display', text='Program Name') 
        self.heading('COLLEGE_Display', text='College')
        self.column('CODE_Display', width=80, anchor='center') 
        self.column('NAME_Display', width=300, anchor='center')     # padakoon para sa long program names
        self.column('COLLEGE_Display', width=280, anchor='center') 

class CollegeTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(
            master=master,
            bootstyle='info',
            height=12,
            columns=('CODE_Display', 'NAME_Display'),
            show='headings'
        )
        self.heading('CODE_Display', text='College Code')
        self.heading('NAME_Display', text='College Name')
        self.column('CODE_Display', width=100, anchor='center')
        self.column('NAME_Display', width=550, anchor='center') # padakoon para sa long college names

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
        main_title_label = ttk.Label(self, text="STUDENT INFORMATION SYSTEM", style="WhiteTitle.TLabel", anchor="center")
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
        
        all_student_data = students.get_all(keyword=keyword) 

        for idx, student_record in enumerate(all_student_data): # student_record keys are now SQL column names
            if not isinstance(student_record, dict): continue
            
            program_code_val = student_record.get("programCODE", "NOT ASSIGNED") # Use SQL column name
            if not program_code_val: 
                program_code_val = "NOT ASSIGNED"
            
            self.students_table.insert('', 'end', iid=f"student_{idx}", values=(
                student_record.get("studentID", "N/A"), 
                student_record.get("FIRSTNAME", ""),
                student_record.get("LASTNAME", ""), 
                student_record.get("SEX", ""),
                program_code_val, # Display programCODE directly or map to name if desired
                student_record.get("YEAR LEVEL", "")))

    def new_student_button_callback(self): StudentInfo(self, 'new')

    def edit_student_button_callback(self):
        selected_item_iid = self.students_table.selection()
        if not selected_item_iid: return self.dialog("Please select a student from the table first.")
        
        # The values from treeview might be display-formatted. Fetch full record by ID.
        # Assuming the first value in treeview row is the studentID
        item_values = self.students_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get student ID from table.", "Error")
        student_id_val = item_values[0]

        # --- CRITICAL CHANGE: Fetch specific student data using SQL column names for editing ---
        student_data_for_edit = None
        # Ideally, a students.get_one(student_id_val) method would be better.
        all_stud_records = students.get_all(filter_criteria={"studentID": student_id_val})
        if all_stud_records and len(all_stud_records) > 0:
            student_data_for_edit = all_stud_records[0]
        
        if not student_data_for_edit:
             return self.dialog(f"Could not retrieve details for student ID {student_id_val}.", "Error")

        StudentInfo(self, 'edit', student_data_for_edit)


    def delete_student_data(self):
        selected_item_iid = self.students_table.selection()
        if not selected_item_iid: return
        
        item_values = self.students_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get student ID from table.", "Error")
        student_id_val = item_values[0] # This is studentID

        if students.remove(student_id_val):
            self.dialog(f"Successfully deleted Student #{student_id_val}")
            self.refresh_student_table()
        else:
            self.dialog(f"Failed to delete Student #{student_id_val}", "Error")


    def delete_student_button_callback(self):
        selected_item_iid = self.students_table.selection()
        if not selected_item_iid: return self.dialog("Please select a student from the table first.")
        item_values = self.students_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get student ID from table.", "Error")
        student_id_val = item_values[0] # This is studentID
        self.confirmation(f"Do you want to delete student #{student_id_val}?", self.delete_student_data)

    # FUNCTIONS PARA SA PROGRAM TAB
    def program_search(self, *args): self.refresh_program_table(self.program_key_search.get())

    def refresh_program_table(self, keyword=None):
        for item in self.program_table.get_children(): self.program_table.delete(item)
        
        all_program_data = programs.get_all(keyword=keyword)
        
        # For displaying college name instead of collegeCODE
        all_colleges_data = colleges.get_all()
        college_map = {c.get("collegeCODE"): c.get("collegeNAME", "Unknown College") for c in all_colleges_data if isinstance(c, dict)}

        for idx, program_record in enumerate(all_program_data): # program_record keys are SQL column names
            if not isinstance(program_record, dict): continue
            
            college_code_val = program_record.get("collegeCODE")
            college_display_name = college_map.get(college_code_val, college_code_val if college_code_val else "N/A")

            self.program_table.insert('', 'end', iid=f"program_{idx}", values=(
                program_record.get("programID", "N/A"), 
                program_record.get("programNAME", ""), 
                college_display_name))

    def new_program_button_callback(self): ProgramInfo(self, 'new')

    def edit_program_button_callback(self):
        selected_item_iid = self.program_table.selection()
        if not selected_item_iid: return self.dialog("Please select a program from the table first.")
        item_values = self.program_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get program ID from table.", "Error")
        program_id_val = item_values[0] # This is programID

        program_data_for_edit = None
        all_prog_records = programs.get_all(filter_criteria={"programID": program_id_val})
        if all_prog_records and len(all_prog_records) > 0:
            program_data_for_edit = all_prog_records[0]
        
        if not program_data_for_edit:
            return self.dialog(f"Could not retrieve details for program ID {program_id_val}.", "Error")

        ProgramInfo(self, 'edit', program_data_for_edit)

    def delete_program_data(self):
        selected_item_iid = self.program_table.selection()
        if not selected_item_iid: return
        item_values = self.program_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get program ID from table.", "Error")
        program_id_val = item_values[0] # This is programID
        
        # Original comment from docx:
        # if gusto mag delete og program pero naa pay isa ka data naka assign, error catched
        # The logic below is for Python-driven cascading delete.
        # If ON DELETE CASCADE is set in DB for students.programCODE -> programs.programID,
        # the following student deletion loop is not strictly needed.
        
        students_deleted_count = 0
        # --- CRITICAL CHANGE: Cascading delete now targets students by programCODE ---
        students_to_delete = students.get_all(filter_criteria={"programCODE": program_id_val})
        if students_to_delete: # students_to_delete is a list of dicts
            for student_dict in students_to_delete:
                if students.remove(student_dict.get("studentID")):
                    students_deleted_count += 1
        
        if programs.remove(program_id_val):
            self.dialog(f"Successfully deleted Program {program_id_val} and {students_deleted_count} associated student(s).")
        else:
            self.dialog(f"Failed to delete Program {program_id_val}. Associated students deleted: {students_deleted_count}", "Error")
        
        self.refresh_student_table() 
        self.refresh_program_table()


    def delete_program_button_callback(self):
        selected_item_iid = self.program_table.selection()
        if not selected_item_iid: return self.dialog("Please select a program from the table first.")
        item_values = self.program_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get program ID from table.", "Error")
        program_id_val = item_values[0] # This is programID
        self.confirmation(f"Do you want to delete Program {program_id_val} and all its associated students? This action cannot be undone.", self.delete_program_data)

    # FUNCTIONS FOR COLLEGE TAB
    def college_search(self, *args): self.refresh_college_table(self.college_key_search.get())

    def refresh_college_table(self, keyword=None):
        self.college_table.delete(*self.college_table.get_children())
        all_college_data = colleges.get_all(keyword=keyword)
        for idx, college_record in enumerate(all_college_data): # college_record keys are SQL column names
            if not isinstance(college_record, dict): continue
            self.college_table.insert('', 'end', iid=f"college_{idx}", values=[
                college_record.get("collegeCODE", "N/A"), 
                college_record.get("collegeNAME", "")])

    def new_college_button_callback(self): CollegeInfo(self, 'new')

    def edit_college_button_callback(self):
        selected_item_iid = self.college_table.selection()
        if not selected_item_iid: return self.dialog("Please select a college from the table first.")
        item_values = self.college_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get college ID from table.", "Error")
        college_id_val = item_values[0] # This is collegeCODE

        college_data_for_edit = None
        all_coll_records = colleges.get_all(filter_criteria={"collegeCODE": college_id_val})
        if all_coll_records and len(all_coll_records) > 0:
            college_data_for_edit = all_coll_records[0]

        if not college_data_for_edit:
            return self.dialog(f"Could not retrieve details for college ID {college_id_val}.", "Error")
            
        CollegeInfo(self, 'edit', college_data_for_edit)

    def delete_college_data(self):
        selected_item_iid = self.college_table.selection()
        if not selected_item_iid: return
        item_values = self.college_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get college ID from table.", "Error")
        college_id_val = item_values[0] # This is collegeCODE

        # Original comment from docx:
        # if any(p.get("COLLEGE") == college_id for p in programs.get_all()):
        # (Note: Original get("COLLEGE") would now be get("collegeCODE"))
        # The logic below is for Python-driven cascading delete.
        # If ON DELETE CASCADE is set in DB for programs.collegeCODE -> colleges.collegeCODE
        # AND students.programCODE -> programs.programID, the following loops are not strictly needed.

        programs_deleted_count = 0
        students_deleted_total_count = 0

        # --- CRITICAL CHANGE: Cascading delete now identifies programs by collegeCODE ---
        programs_to_delete = programs.get_all(filter_criteria={"collegeCODE": college_id_val})
        if programs_to_delete:
            for prog_dict in programs_to_delete:
                prog_id_to_delete = prog_dict.get("programID")
                if not prog_id_to_delete: continue

                students_in_prog_to_delete = students.get_all(filter_criteria={"programCODE": prog_id_to_delete})
                if students_in_prog_to_delete:
                    for student_dict in students_in_prog_to_delete:
                        if students.remove(student_dict.get("studentID")):
                            students_deleted_total_count +=1
                
                if programs.remove(prog_id_to_delete):
                    programs_deleted_count += 1
        
        if colleges.remove(college_id_val):
            self.dialog(f"Successfully deleted College {college_id_val}, {programs_deleted_count} associated program(s), and {students_deleted_total_count} associated student(s).")
        else:
            self.dialog(f"Failed to delete College {college_id_val}. Associated items deleted: {programs_deleted_count} programs, {students_deleted_total_count} students.", "Error")
        
        self.refresh_student_table()
        self.refresh_program_table()
        self.refresh_college_table()


    def delete_college_button_callback(self):
        selected_item_iid = self.college_table.selection()
        if not selected_item_iid: return self.dialog("Please select a college from the table first.")
        item_values = self.college_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get college ID from table.", "Error")
        college_id_val = item_values[0] # This is collegeCODE
        self.confirmation(f"Do you want to delete College {college_id_val} and all its associated programs and students? This action cannot be undone.", self.delete_college_data)
    
    def start(self):
        self.mainloop()