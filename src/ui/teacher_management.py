import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
import uuid
from src.models.teacher import Teacher
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Output logs to the terminal
        logging.FileHandler("application.log")  # Write logs to a file
    ]
)

class TeacherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher Management")
        
        # Add Teacher button
        self.add_teacher_button = tk.Button(root, text="Add Teacher", command=self.open_add_teacher_window)
        self.add_teacher_button.pack(pady=20)

        # Teacher Listbox
        self.teacher_listbox = tk.Listbox(root, width=50, height=20)
        self.teacher_listbox.pack(side="right", padx=20, pady=20)

        # Load teacher data from the database
        self.load_teacher_data()

    def load_teacher_data(self):
        """
        Load teacher data from the database and display it in the listbox.
        """
        self.teacher_listbox.delete(0, tk.END) # Clear the listbox
        teacher = Teacher(None, None, None, None, None, None, new=False) 
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

        tk.Button(
            add_teacher_window, 
            text="Submit", 
            command=lambda: self.submit_teacher_data(
                teacher_name_entry.get(), 
                teacher_salary_entry.get(), 
                start_time.get(),
                end_time.get(),
                [],
                add_teacher_window
            )
        ).pack(pady=10)

    def submit_teacher_data(self, teacher_name, teacher_salary, start_time, end_time, available_date, window):
        teacher_id = str(uuid.uuid4().int)[:6]
        teacher = Teacher(
            teacher_id=teacher_id,
            name=teacher_name,
            salary=teacher_salary,
            available_date=available_date, # Correctly pass the list here
            start_time=start_time,         # Correctly pass start_time
            end_time=end_time,             # Correctly pass end_time
            new=True
        )
        logging.info(f"Teacher {teacher.name} with ID: {teacher.teacher_id} has been created.")
        window.destroy()
        self.load_teacher_data()  # Reload the teacher data
    

    # def open_delete_teacher_window(self):
    #     """Delete a new window to delete a teacher."""
    #     delete_teacher_window = Toplevel(self.root)
    #     delete_teacher_window.title("Delete Teacher")
    #     delete_teacher_window.geometry("400x200")
    #     tk.Label(delete_teacher_window, text="Are you sure you want to delete this teacher?", font=("Arial", 12)).pack(pady=20)
        
    #     button_frame = tk.Frame(delete_teacher_window)
    #     button_frame.pack(pady=10)

    #     tk.Button(button_frame, text="Confirm", command=lambda: self.confirm_delete(delete_teacher_window)).pack(side="left", padx=20)
    #     tk.Button(button_frame, text="Cancel", command=delete_teacher_window.destroy).pack(side="right", padx=20)

    # def confirm_delete(self, window):
    #     """Handle the confirmation logic."""
    #     tk.Label(window, text="Teacher deleted!", font=("Arial", 12), fg="green").pack(pady=10)
    #     # Add your delete logic here

    #     window.destroy()  # Close the window after confirming


