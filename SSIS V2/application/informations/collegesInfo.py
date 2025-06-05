import tkinter as tk
import ttkbootstrap as ttk
from ..database import colleges

class CollegeInfo(tk.Toplevel):
    def __init__(self, master, mode: str, data: dict = None): 
        super().__init__(master=master)
        self.mode = mode
        self.data = data # will display the values collegeCODE, collegeNAME
        self.transient(master)
        window_width = 350
        window_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.title('New College' if mode == 'new' else 'Edit College Information')
    
        form_frame = ttk.Frame(self, padding=20)
        form_frame.pack(fill='both', expand=True)
        
        ttk.Label(form_frame, text="COLLEGE CODE", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.id_entry = ttk.Entry(form_frame)
        self.id_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="COLLEGE NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.pack(padx=0, fill='x', pady=(0,20))
        
        self.buttons_frame = ttk.Frame(form_frame)
        self.create_button = ttk.Button(self.buttons_frame, text="Create" if mode == 'new' else 'Save Changes', width=15, bootstyle="success" if mode == 'new' else "primary", command=self.create_button_callback)
        self.create_button.pack(side='left', fill='x', expand=True, padx=(0,5), ipady=3)
        
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", width=15, bootstyle="secondary", command=self.destroy)
        self.cancel_button.pack(side='right', fill='x', expand=True, padx=(5,0), ipady=3) 
        self.buttons_frame.pack(side='bottom', padx=0, pady=(10,0), fill='x')

        if self.data is not None:
            self.id_entry.insert(0, self.data.get('collegeCODE','')) 
            self.id_entry.configure(state='disabled')
            self.name_entry.insert(0, self.data.get("collegeNAME",'')) 
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
        ok_button = ttk.Button(button_frame, text='OK', width=10, command=toplevel.destroy, bootstyle="primary")
        ok_button.pack() 
        toplevel.grab_set()

    def create_button_callback(self):
        college_code_val = self.id_entry.get().strip() # for the collegeCODE
        college_name_val = self.name_entry.get().strip() # for the collegeNAME'
        
        # data dictionary keys that match SQL column names
        current_data_payload = {"collegeCODE": college_code_val, "collegeNAME": college_name_val}
        
        if not college_code_val or not college_name_val:
            return self.dialog("College Code and College Name are required!", "Input Error")
            
        if self.mode == 'new':
            if colleges.check(college_code_val): return self.dialog("This College code already exists!", "Please try again.")
            colleges.insert_one(current_data_payload)
            self.dialog(f"Successfully created the College!!\n{college_code_val}", "Success!!!")
            if hasattr(self.master, 'refresh_college_table'): self.master.refresh_college_table()
            if hasattr(self.master, 'refresh_program_table'): self.master.refresh_program_table()
            self.destroy()
        else: 
            original_college_code = self.data.get('collegeCODE')
            
            if self.data and original_college_code == college_code_val and self.data.get('collegeNAME') == college_name_val:
                 return self.dialog("No changes were made. Please try again.", "Information")

            update_payload = {"collegeCODE": original_college_code, "collegeNAME": college_name_val}
            colleges.edit(update_payload) 
            self.dialog(f"Successfully updated the College '{original_college_code}'", "Success!!!")
            if hasattr(self.master, 'refresh_college_table'): self.master.refresh_college_table()
            if hasattr(self.master, 'refresh_program_table'): self.master.refresh_program_table()
            self.destroy()