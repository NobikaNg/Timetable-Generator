import tkinter as tk
from tkinter import Toplevel, ttk, messagebox
import uuid
from src.models.session import Session
import logging
import calendar
from datetime import date, datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    handlers=[
        logging.StreamHandler(),  
    ]
)

class Session_UI:
    def __init__(self, root, room_id, list_parent=None):
        self.root = root
        self.session_room = room_id
        self.session = {}
        self.selected_sesion_id = None

        top_frame = tk.Frame(root)
        top_frame.pack(side="top", anchor="w", pady=5)

        self.add_button = tk.Button(top_frame, text="Add Session", command=self.open_add_session_window)
        self.add_button.pack(side="left", padx=5)

        self.edit_button = tk.Button(top_frame, text="Edit Session", command=self.open_edit_session_window, state="disabled")
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(top_frame, text="Delete Session", command=self.delete_session, state="disabled")
        self.delete_button.pack(side="left", padx=5)

        list_parent = list_parent or root
        self.session_listbox = tk.Listbox(list_parent, width=50, height=10)
        self.session_listbox.pack(side="top", padx=5, pady=(0, 5), fill="both", expand=True)
        self.session_listbox.bind('<<ListboxSelect>>', self.on_session_select)

    def load_session_data(self):
        self.session_listbox.delete(0, tk.END)
        sessions = Session.get_all_session()

        for session_record in sessions:
            session_id, session_start, session_end, session_room, sesion_date, student_count, on_duty_teachers, session_token = session_record
            # self.session_listbox.insert(
            #     tk.END,
            #     f"ID: {session_id}, Name: {session_start}, "
            # )

    def generate_time_options(self, start="09:00", end="21:00", interval=30):
        time_format = "%H:%M"
        start_time = datetime.strptime(start, time_format)
        end_time = datetime.strptime(end, time_format)
        times = []
        while start_time <= end_time:
            times.append(start_time.strftime(time_format))
            start_time += timedelta(minutes=interval)
        return times

    def update_end_times(self, event):
        selected_start = self.start_combobox.get()
        if selected_start:
            start_index = self.time_options.index(selected_start)
            self.end_combobox['values'] = self.time_options[start_index + 1:]
            self.end_combobox.set('')

    def session_form_window(self, title, submit_command, session_date=None):
        form_window = Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("400x400")

        self.time_options = self.generate_time_options()
    
        # Start Time
        tk.Label(form_window, text = "Start Time (HH:MM):").pack()
        self.start_combobox = ttk.Combobox(form_window, values=self.time_options, state="readonly")
        self.start_combobox.pack()
        self.start_combobox.bind("<<ComboboxSelected>>", self.update_end_times)

        # End Time
        tk.Label(form_window, text="End Time (HH:MM):").pack()
        self.end_combobox = ttk.Combobox(form_window, values=[], state="readonly")
        self.end_combobox.pack()

        # Student Count
        tk.Label(form_window, text="Student Count:").pack()
        self.student_count_entry = tk.Entry(form_window)
        self.student_count_entry.pack()




    def on_session_select(self, event):
        selection = self.session_listbox.curselection()
        if not selection:
            return
        
        selected_item = self.session_listbox.get(selection[0])
        self.selected_session_id = selected_item.split(",")[0].split(": ")[1]
        
        self.edit_button.config(state="normal")
        self.delete_button.config(state="normal")
        logging.info(f"Selected Session: {self.selected_session_id}")
    
    def open_add_session_window(self):
        self.session_form_window("Add Session", self.submit_new_session)
