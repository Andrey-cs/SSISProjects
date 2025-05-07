import tkinter as tk
import ttkbootstrap as ttk
from ..database import programs, colleges

class ProgramInfo(tk.Toplevel):
    def __init__(self, master, mode: str, data: dict = None):
        super().__init__(master=master)
        self.mode = mode
        self.data = data
        self.transient(master)

        window_width = 350
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.title('New Program' if mode == 'new' else 'Edit Program Information')

        form_frame = ttk.Frame(self, padding=20)
        form_frame.pack(fill='both', expand=True)

        ttk.Label(form_frame, text="PROGRAM CODE", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.id_entry = ttk.Entry(form_frame)
        self.id_entry.pack(padx=0, fill='x', pady=(0,10))

        ttk.Label(form_frame, text="PROGRAM NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.pack(padx=0, fill='x', pady=(0,10))
        
        ttk.Label(form_frame, text="COLLEGE", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        college_ids_list = [cid for cid in colleges.get_college_ids() if cid] 
        if not college_ids_list or college_ids_list[0] != "No Selection":
            college_ids_list.insert(0, "No Selection")
        self.college_option = ttk.Combobox(form_frame, values=college_ids_list, state='readonly')
        self.college_option.pack(fill='x', padx=0, pady=(0,20))

        self.buttons_frame = ttk.Frame(form_frame)
        self.create_button = ttk.Button(self.buttons_frame, text="Create" if mode == 'new' else 'Save Changes', width=15, bootstyle="success" if mode == 'new' else "primary", command=self.create_button_callback)
        self.create_button.pack(side='left', fill='x', expand=True, padx=(0,5), ipady=3) 
        
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", width=15, bootstyle="secondary", command=self.destroy)
        self.cancel_button.pack(side='right', fill='x', expand=True, padx=(5,0), ipady=3) 
        self.buttons_frame.pack(side='bottom', padx=0, pady=(10,0), fill='x')

        if self.data is not None:
            self.id_entry.insert(0, self.data.get('ID', ''))
            self.id_entry.configure(state='disabled')
            self.name_entry.insert(0, self.data.get("NAME", ''))
            current_college = self.data.get("COLLEGE", "No Selection")
            self.college_option.set(current_college if current_college in college_ids_list else "No Selection")
        else:
            self.college_option.set("No Selection")
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
        outer_frame = ttk.Frame(toplevel) # Use a frame for better centering control
        outer_frame.pack(expand=True, fill='both', padx=10, pady=10)
        msg_label = ttk.Label(outer_frame, text=text, wraplength=window_width-60, justify='center', anchor='center')
        msg_label.pack(expand=True, fill='both', pady=(0,15))
        button_frame = ttk.Frame(outer_frame)
        button_frame.pack(side='bottom', pady=(0,5))
        ok_button = ttk.Button(button_frame, text='OK', width=10, command=toplevel.destroy, bootstyle="primary")
        ok_button.pack() 
        toplevel.grab_set()

    def create_button_callback(self):
        prog_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        college_val = self.college_option.get()
        selected_college = college_val if college_val != "No Selection" else ""
        current_data = {"ID": prog_id, "NAME": name, "COLLEGE": selected_college}

        if not prog_id or not name:
            return self.dialog("Program Code and Program Name are required.", "Input Error")

        if self.mode == 'new':
            if programs.check(prog_id): return self.dialog("Program code already exists!!", "Error")
            programs.insert_one(current_data)
            self.dialog(f"Successfully created Program!! {prog_id}", "Success!")
            if hasattr(self.master, 'refresh_program_table'): self.master.refresh_program_table()
            if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
            self.destroy()
        else: 
            changed = False
            if self.data:
                for key in current_data:
                     # Check against empty string for COLLEGE if it was "No Selection"
                    data_val = self.data.get(key, "") if key == "COLLEGE" and self.data.get(key) == "No Selection" else self.data.get(key, "")
                    current_val = current_data[key]
                    if data_val != current_val:
                        changed = True
                        break
            else: # Should not happen
                changed = True

            if not changed and self.data.get('ID') == current_data['ID']:
                return self.dialog("No changes were made. Please try again.", "Information")
            
            programs.edit(current_data)
            self.dialog(f"Successfully Updated Program '{prog_id}'", "Success")
            if hasattr(self.master, 'refresh_program_table'): self.master.refresh_program_table()
            if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
            self.destroy()