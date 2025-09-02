import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import uuid
from src.models.teacher import Teacher
import logging
import calendar
from datetime import date

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    handlers=[
        logging.StreamHandler(),  
    ]
)

class TeacherUI:
    def __init__(self, root, list_parent=None):
        self.root = root

        # top-left
        top_frame = tk.Frame(root)
        top_frame.pack(side="top", anchor="nw", padx=20, pady=20)
        
        # Add Teacher button
        self.add_teacher_button = tk.Button(top_frame, text="Add Teacher", command=self.open_add_teacher_window)
        self.add_teacher_button.pack(side="left", padx=12)

        # Delete Teacher button
        self.delete_teacher_button = tk.Button(top_frame, text="Delete Teacher", command=self.open_delete_teacher_window)
        self.delete_teacher_button.pack(side="left", padx=12)

        # Edit Teacher button
        self.edit_teacher_button = tk.Button(top_frame, text="Edit Teacher", command=self.open_edit_teacher_window)
        self.edit_teacher_button.pack(side="left", padx=12)

        # Teacher Listbox
        list_parent = list_parent or root
        self.teacher_listbox = tk.Listbox(list_parent, width=50, height=20)
        self.teacher_listbox.pack(side="top", padx=20, pady=(20, 10), fill="both")
        self.teacher_listbox.bind('<<ListboxSelect>>', self.on_teacher_select)

        self.selected_teacher_id = None

        # Load teacher data from the database
        self.load_teacher_data()

    def load_teacher_data(self):
        """
        Load teacher data from the database and display it in the listbox.
        """
        self.teacher_listbox.delete(0, tk.END) # Clear the listbox
        #teacher = Teacher(None, None, None, None, None, None, new=False) 
        teachers = Teacher.get_all_teachers()  # Fetch all teacher records from the database
        
        for teacher_record in teachers:
            teacher_id, name, salary, available_date, start_time, end_time, working_hr = teacher_record
            self.teacher_listbox.insert(
                tk.END, 
                f"ID: {teacher_id}, Name: {name}, Salary: {salary}, Available_date: {available_date}, Start: {start_time}, End: {end_time}, Working Hour: {working_hr}"
            )

    def open_add_teacher_window(self):
        """Open a new window to add a teacher."""

        logging.info("Open the add teacher window")

        add_teacher_window = Toplevel(self.root)
        add_teacher_window.title("Add Teacher")
        add_teacher_window.geometry("500x500")

        add_teacher_window.grab_set()

        tk.Label(add_teacher_window, text="Add Teacher Form", font=("Arial", 14)).pack(pady=10)
        
        # name field
        tk.Label(add_teacher_window, text="Name:").pack()
        teacher_name_entry = tk.Entry(add_teacher_window)
        teacher_name_entry.pack(pady=5)

        # salary field
        tk.Label(add_teacher_window, text="Salary:").pack()
        teacher_salary_entry = tk.Entry(add_teacher_window)
        teacher_salary_entry.pack(pady=5)

        # time field, dropdown for start_time and end_time
        times = [f"{hour}:{minute:02d}" for hour in range(9, 22) for minute in [0, 30]]
        tk.Label(add_teacher_window, text="Start Time").pack(pady=5)
        start_time = tk.StringVar()
        start_time_dropdown = ttk.Combobox(add_teacher_window, textvariable=start_time, values=times, state="readonly")
        start_time_dropdown.pack(pady=5)

        tk.Label(add_teacher_window, text="End Time").pack(pady=5)
        end_time = tk.StringVar()
        end_time_dropdown = ttk.Combobox(add_teacher_window, textvariable=end_time, values=times, state="readonly")
        end_time_dropdown.pack(pady=5)

        # Available dates calendar
        tk.Label(add_teacher_window, text="Available Dates:").pack(pady=10)

        calendar_frame = tk.Frame(add_teacher_window)
        calendar_frame.pack(pady=5)

        today = date.today()
        year, month = today.year, today.month

        cal = calendar.Calendar(firstweekday=6)
        weeks = cal.monthdatescalendar(year, month)
        headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for col, h in enumerate(headers):
            tk.Label(calendar_frame, text = h, font = ("Arial", 12, "bold"), padx = 8, pady = 4).grid(row=0, column = col, sticky = "nsew")

        selected_dates = set()

        def make_toggle(day_date):
            btn_ref = {"btn": None, "default_bg": None}

            def on_click():
                if day_date.month != month:
                    return
                iso = day_date.isoformat()
                if iso in selected_dates:
                    selected_dates.remove(iso)
                    btn_ref["btn"].config(relief = "raised", bg=btn_ref["default_bg"])
                else:
                    selected_dates.add(iso)
                    btn_ref["btn"].config(relief = "sunken", bg="#cce5ff")
            
            return btn_ref, on_click
        
        for r, week in enumerate(weeks, start=1):
            for c, day_date in enumerate(week):
                if day_date.month != month:
                    tk.Label(calendar_frame, text = "", width = 4, padx=8, pady=6).grid(row=r, column=c, sticky="nsew")
                else:
                    ref, handler = make_toggle(day_date)
                    day_val = day_date.day
                    btn = tk.Button(calendar_frame, text=str(day_val), width=4, padx=8, pady=6, command=handler)
                    btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                    ref["btn"] = btn
                    ref["default_bg"] = btn.cget("bg")

        # submit button
        tk.Button(
            add_teacher_window, 
            text="Submit", 
            command=lambda: self.submit_teacher_data(
                teacher_name_entry.get(), 
                teacher_salary_entry.get(), 
                start_time.get(),
                end_time.get(),
                list(sorted(selected_dates)), # This is the list of available dates, not implemented yet
                add_teacher_window
            )
        ).pack(pady=10)

    def submit_teacher_data(self, teacher_name, teacher_salary, start_time, end_time, available_date, window):
        teacher_id = str(uuid.uuid4().int)[:6]
        teacher = Teacher(
            teacher_id=teacher_id,
            name=teacher_name,
            salary=teacher_salary,
            available_date=available_date, 
            start_time=start_time,         
            end_time=end_time,             
            new=True
        )
        logging.info(f"Teacher {teacher.name} with ID: {teacher.teacher_id} has been created.")
        window.destroy()
        self.load_teacher_data()  # Reload the teacher data
    
    def on_teacher_select(self, event):
        """ 
        handler: when a teacher in the list box is selected
        """
        selection = event.widget.curselection()
        if selection:
            selected_line = event.widget.get(selection[0])
            teacher_id = selected_line.split(",")[0].replace("ID: ","").strip()
            self.selected_teacher_id = teacher_id

            logging.info(f"Selected teacher ID: {self.selected_teacher_id}")

            self.delete_teacher_button.config(state="normal")
        
        else:
            self.selected_teacher_id = None
            self.delete_teacher_button.config(state="disabled")

    def open_delete_teacher_window(self):
        """Delete a new window to delete a teacher."""
        if not self.selected_teacher_id:
            return  # No teacher selected

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this teacher?")
        if confirm:
            Teacher.delete_teacher(self.selected_teacher_id)
            self.selected_teacher_id = None
            self.load_teacher_data()
            self.delete_teacher_button.config(state="disabled")

    def open_edit_teacher_window(self):
        """Edit the selected teacher's information"""
        if not self.selected_teacher_id:
            return  # No teacher selected

        edit_teacher_window = Toplevel(self.root)
        edit_teacher_window.title("Edit Teacher")
        edit_teacher_window.geometry("500x650")

        # Fetch the selected teacher's information
        teacher = Teacher.find_teacher(self.selected_teacher_id)
        if not teacher:
            logging.error(f"Teacher with ID {self.selected_teacher_id} not found.")
            return

        logging.info("Get Teacher object's data")
        id, name, salary, available_date_str, start_time_val, end_time_val, _, _, _, _ = teacher
        logging.info("Get data success")

        # Name
        tk.Label(edit_teacher_window, text="Name:").pack()
        teacher_name_entry = tk.Entry(edit_teacher_window)
        teacher_name_entry.insert(0, name) # Pre-fill name
        teacher_name_entry.pack(pady=5)

        # Salary 
        tk.Label(edit_teacher_window, text="Salary:").pack()
        teacher_salary_entry = tk.Entry(edit_teacher_window)
        teacher_salary_entry.insert(0, salary) # Pre-fill salary
        teacher_salary_entry.pack(pady=5)

        # Time
        times = [f"{hour}:{minute:02d}" for hour in range(9, 22) for minute in [0, 30]]
        tk.Label(edit_teacher_window, text="Start Time").pack(pady=5)
        start_time = tk.StringVar(value=start_time_val)
        start_time_dropdown = ttk.Combobox(edit_teacher_window, textvariable=start_time, values=times, state="readonly")
        start_time_dropdown.pack(pady=5)

        tk.Label(edit_teacher_window, text="End Time").pack(pady=5)
        end_time = tk.StringVar(value=end_time_val)
        end_time_dropdown = ttk.Combobox(edit_teacher_window, textvariable=end_time, values=times, state="readonly")
        end_time_dropdown.pack(pady=5)

        # Available date 
        tk.Label(edit_teacher_window, text="Available Dates:").pack(pady=10)

        calendar_frame = tk.Frame(edit_teacher_window)
        calendar_frame.pack(pady=5)

        today = date.today()
        year, month = today.year, today.month

        cal = calendar.Calendar(firstweekday=6)
        weeks = cal.monthdatescalendar(year, month)
        headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for col, h in enumerate(headers):
            tk.Label(calendar_frame, text = h, font = ("Arial", 12, "bold"), padx = 8, pady = 4).grid(row=0, column = col, sticky = "nsew")

        selected_dates = set(available_date_str.split(',')) if available_date_str else set()

        def make_toggle(day_date):
            btn_ref = {"btn": None, "default_bg": None}

            def on_click():
                if day_date.month != month:
                    return
                iso = day_date.isoformat()
                if iso in selected_dates:
                    selected_dates.remove(iso)
                    btn_ref["btn"].config(relief = "raised", bg=btn_ref["default_bg"])
                else:
                    selected_dates.add(iso)
                    btn_ref["btn"].config(relief = "sunken", bg="#cce5ff")
            
            return btn_ref, on_click
        
        for r, week in enumerate(weeks, start=1):
            for c, day_date in enumerate(week):
                if day_date.month != month:
                    tk.Label(calendar_frame, text = "", width = 4, padx=8, pady=6).grid(row=r, column=c, sticky="nsew")
                else:
                    ref, handler = make_toggle(day_date)
                    day_val = day_date.day
                    btn = tk.Button(calendar_frame, text=str(day_val), width=4, padx=8, pady=6, command=handler)
                    btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                    ref["btn"] = btn
                    ref["default_bg"] = btn.cget("bg")
                    if day_date.isoformat() in selected_dates:
                        btn.config(relief="sunken", bg="#cce5ff")

        # Save button
        tk.Button(edit_teacher_window, text="Save", command=lambda: self.save_edited_teacher(
            self.selected_teacher_id,
            teacher_name_entry.get(),
            teacher_salary_entry.get(),
            start_time.get(),
            end_time.get(),
            list(sorted(selected_dates)), 
            edit_teacher_window
        )).pack(pady=20)

    def save_edited_teacher(self, teacher_id, name, salary, start_time, end_time, available_dates, window):
        """Save the edited teacher's information"""
        update_data = {
            "name": name,
            "salary": salary,
            "start_time": start_time,
            "end_time": end_time,
            "available_date": available_dates
        }

        filtered_data = {k: v for k, v in update_data.items() if v}

        if filtered_data:
            Teacher.edit_teacher_info(
                teacher_id, 
                **filtered_data)
        window.destroy()
        self.load_teacher_data()