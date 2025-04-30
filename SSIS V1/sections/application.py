import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from .database import students, programs, colleges
from .infos import StudentInfo, ProgramInfo

class StudentInformationSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Information System")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.configure(bg="#121212")
        self.center_window()
        self.setup_styles()
        self.create_widgets()
        self.refresh_student_table()
        self.refresh_program_table()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors for UI
        self.bg_color = "#121212"
        self.card_color = "#1E1E1E"
        self.accent_color = "#00BFFF"
        self.text_color = "#FFFFFF"
        self.entry_bg = "#2D2D2D"
        self.hover_color = "#3A3A3A"
        
        # Fonts for UI
        try:
            self.title_font = tkfont.Font(family="Montserrat", size=25, weight="bold")
            self.label_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
            self.button_font = tkfont.Font(family="Segoe UI", size=10)
        except:
            self.title_font = tkfont.Font(size=16, weight="bold")
            self.label_font = tkfont.Font(size=10, weight="bold")
            self.button_font = tkfont.Font(size=10)
        
        # Configuring the Styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=self.label_font)
        self.style.configure("TButton", 
                           background=self.card_color, 
                           foreground=self.accent_color,
                           font=self.button_font,
                           borderwidth=0)
        self.style.map("TButton",
                      background=[('active', '#3A3A3A')],
                      foreground=[('active', self.text_color)])
        
        self.style.configure("TEntry", 
                           fieldbackground=self.entry_bg,
                           foreground=self.text_color,
                           insertcolor=self.accent_color)
        
        self.style.configure("TCombobox",
                           fieldbackground=self.entry_bg,
                           foreground=self.text_color)
        
        self.style.configure("Treeview",
                           background=self.card_color,
                           foreground=self.text_color,
                           fieldbackground=self.card_color,
                           rowheight=25)
        self.style.map("Treeview",
                      background=[('selected', self.accent_color)],
                      foreground=[('selected', self.text_color)])
        
    def create_widgets(self):
        # Title Frame
        title_frame = ttk.Frame(self)
        title_frame.pack(pady=10)
        
        ttk.Label(title_frame, 
                 text="STUDENT INFORMATION SYSTEM",
                 font=self.title_font,
                 foreground=self.accent_color).pack()
        
        # Notebook for Students/Programs tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Students Tab
        self.create_students_tab()     
        # Programs Tab
        self.create_programs_tab()
        
    def create_students_tab(self):
        """Create students tab with all widgets"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Students")
        
        # Input Frame
        input_frame = ttk.Frame(tab)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        # Input Fields
        ttk.Label(input_frame, text="Student ID:").grid(row=0, column=0, sticky='w')
        self.student_id_entry = ttk.Entry(input_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="First Name:").grid(row=1, column=0, sticky='w')
        self.first_name_entry = ttk.Entry(input_frame)
        self.first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Last Name:").grid(row=2, column=0, sticky='w')
        self.last_name_entry = ttk.Entry(input_frame)
        self.last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Sex:").grid(row=0, column=2, sticky='w', padx=(10,0))
        self.sex_combobox = ttk.Combobox(input_frame, values=["Male", "Female"], state='readonly')
        self.sex_combobox.grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Program:").grid(row=1, column=2, sticky='w', padx=(10,0))
        self.program_combobox = ttk.Combobox(input_frame, state='readonly')
        self.program_combobox.grid(row=1, column=3, padx=5, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Year Level:").grid(row=2, column=2, sticky='w', padx=(10,0))
        self.year_combobox = ttk.Combobox(input_frame, values=["1", "2", "3", "4"], state='readonly')
        self.year_combobox.grid(row=2, column=3, padx=5, pady=5, sticky='ew')
        
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="New", command=self.new_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.student_tree = ttk.Treeview(tree_frame, columns=('id', 'fname', 'lname', 'sex', 'program', 'year'), show='headings')
        self.student_tree.heading('id', text='ID')
        self.student_tree.heading('fname', text='First Name')
        self.student_tree.heading('lname', text='Last Name')
        self.student_tree.heading('sex', text='Sex')
        self.student_tree.heading('program', text='Program')
        self.student_tree.heading('year', text='Year Level')
        
        self.student_tree.column('id', width=100)
        self.student_tree.column('fname', width=150)
        self.student_tree.column('lname', width=150)
        self.student_tree.column('sex', width=80)
        self.student_tree.column('program', width=150)
        self.student_tree.column('year', width=80)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        
        self.student_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double click to edit
        self.student_tree.bind('<Double-1>', lambda e: self.edit_student())
        
    def create_programs_tab(self):
        """Create programs tab with all widgets"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Programs")
        
        # Input Frame
        input_frame = ttk.Frame(tab)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        # Input Fields
        ttk.Label(input_frame, text="Program Code:").grid(row=0, column=0, sticky='w')
        self.program_code_entry = ttk.Entry(input_frame)
        self.program_code_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(input_frame, text="Program Name:").grid(row=1, column=0, sticky='w')
        self.program_name_entry = ttk.Entry(input_frame)
        self.program_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="New", command=self.new_program).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_program).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_program).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_program_fields).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.program_tree = ttk.Treeview(tree_frame, columns=('code', 'name'), show='headings')
        self.program_tree.heading('code', text='Code')
        self.program_tree.heading('name', text='Name')
        
        self.program_tree.column('code', width=100)
        self.program_tree.column('name', width=400)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.program_tree.yview)
        self.program_tree.configure(yscrollcommand=scrollbar.set)
        
        self.program_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double click to edit
        self.program_tree.bind('<Double-1>', lambda e: self.edit_program())
        
    def refresh_student_table(self):
        """Refresh student table with current data"""
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
            
        for student in students.get_all():
            self.student_tree.insert('', 'end', values=(
                student['ID'],
                student['First Name'],
                student['Last Name'],
                student['Sex'],
                student['Program Code'],
                student['Year Level']
            ))
        
        # Update program combobox
        self.program_combobox['values'] = [p['Program Code'] for p in programs.get_all()]
        
    def refresh_program_table(self):
        """Refresh program table with current data"""
        for item in self.program_tree.get_children():
            self.program_tree.delete(item)
            
        for program in programs.get_all():
            self.program_tree.insert('', 'end', values=(
                program['Program Code'],
                program['Program Name']
            ))
    
    def new_student(self):
        """Open new student dialog"""
        StudentInfo(self, 'new')
        
    def edit_student(self):
        """Edit selected student"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student first")
            return
            
        student_id = self.student_tree.item(selected[0])['values'][0]
        student_data = next(s for s in students.get_all() if s['ID'] == student_id)
        StudentInfo(self, 'edit', student_data)
        
    def delete_student(self):
        """Delete selected student"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student first")
            return
            
        student_id = self.student_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete student {student_id}?"):
            students.remove(student_id)
            self.refresh_student_table()
        
    def clear_fields(self):
        """Clear all student input fields"""
        self.student_id_entry.delete(0, 'end')
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.sex_combobox.set('')
        self.program_combobox.set('')
        self.year_combobox.set('')
        self.student_tree.selection_remove(self.student_tree.selection())
        
    def new_program(self):
        """Open new program dialog"""
        ProgramInfo(self, 'new')
        
    def edit_program(self):
        """Edit selected program"""
        selected = self.program_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a program first")
            return
            
        program_code = self.program_tree.item(selected[0])['values'][0]
        program_data = next(p for p in programs.get_all() if p['Program Code'] == program_code)
        ProgramInfo(self, 'edit', program_data)
        
    def delete_program(self):
        """Delete selected program"""
        selected = self.program_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a program first")
            return
            
        program_code = self.program_tree.item(selected[0])['values'][0]
        
        # Check if any students are enrolled in this program
        enrolled = any(s['Program Code'] == program_code for s in students.get_all())
        if enrolled:
            messagebox.showwarning("Warning", "Cannot delete program with enrolled students")
            return
            
        if messagebox.askyesno("Confirm", f"Delete program {program_code}?"):
            programs.remove(program_code)
            self.refresh_program_table()
            self.refresh_student_table()
        
    def clear_program_fields(self):
        """Clear all program input fields"""
        self.program_code_entry.delete(0, 'end')
        self.program_name_entry.delete(0, 'end')
        self.program_tree.selection_remove(self.program_tree.selection())

if __name__ == "__main__":
    app = StudentInformationSystem()
    app.mainloop()
