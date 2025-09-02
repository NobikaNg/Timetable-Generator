import tkinter as tk
import logging
import uuid
from src.models.room import Room
from tkinter import Toplevel
from src.ui.session_management import Session_UI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    handlers=[
        logging.StreamHandler(),  
    ]
)

class RoomUI:
    def __init__(self, root, list_parent=None):
        self.root = root

        top_frame = tk.Frame(root)
        top_frame.pack(side="top", anchor="nw", padx=20, pady=20)

        # Add Room button
        self.add_room_button = tk.Button(top_frame, text="Add Room", command=self.open_add_room_window)
        self.add_room_button.pack(side="left", padx=12)

        # Delete Room button
        self.delete_room_button = tk.Button(top_frame, text="Delete Room", command=self.open_delete_room_window)
        self.delete_room_button.pack(side="left", padx=12)

        # Edit Room button
        self.edit_room_button = tk.Button(top_frame, text="Edit Room", command=self.open_edit_room_window)
        self.edit_room_button.pack(side="left", padx=12)

        # Room listbox
        list_parent = list_parent or root
        self.room_listbox = tk.Listbox(list_parent, width=50, height=20)
        self.room_listbox.pack(side="top", padx=20, pady=(0, 20), fill="both")
        self.room_listbox.bind('<<ListboxSelect>>', self.on_room_select)

        self.selected_room_id = None

        self.load_room_data()


    def load_room_data(self):
        logging.info("Load Room Data from DB")
        self.room_listbox.delete(0, tk.END)
        rooms = Room.get_all_rooms()

        for rooms_record in rooms:
            room_id, room_name, working_dates, session_list = rooms_record
            self.room_listbox.insert(
                tk.END,
                f"Room ID: {room_id}, Room Name: {room_name}, Working Dates: {working_dates}, Session List: {session_list}"
            )

    def open_add_room_window(self):
        logging.info("Open Add Room Window")

        add_room_window = Toplevel(self.root)
        add_room_window.title("Add Room")
        add_room_window.geometry("500x500")

        add_room_window.grab_set()

        tk.Label(add_room_window, text="Add Room Form", font=("Arial", 14)).pack(pady=10)

        form_frame = tk.Frame(add_room_window)
        form_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(form_frame, text="Room Name:").pack(anchor="w")
        room_name_entry = tk.Entry(form_frame)
        room_name_entry.pack(fill="x")

        tk.Label(form_frame, text="Working Dates:").pack(anchor="w", pady=(10,0))
        dates_frame = tk.Frame(form_frame)
        dates_frame.pack(anchor="w")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturay", "Sunday"]
        working_dates_vars = {day: tk.BooleanVar() for day in days}
        for day in days:
            tk.Checkbutton(dates_frame, text=day, variable=working_dates_vars[day]).pack(side="left")

        session_container = tk.LabelFrame(add_room_window, text="Session Management", padx=10, pady=10)
        session_container.pack(pady=10, padx=20, fill="both", expand=True)

        # A temporary room_id for the sessions to associate with
        temp_room_id = f"temp-{uuid.uuid4()}"
        session_ui = Session_UI(session_container, temp_room_id)

    def submit_room_data(self):
        logging.info("Submit Room Data to DB")
    
    def on_room_select(self):
        """
        used to obtain the Room Id select by User
        """
    
    def open_delete_room_window(self):
        logging.info("Open Delete Room Window")
    
    def open_edit_room_window(self):
        logging.info("Open Edit Room Window")
    
    def save_edited_room(self):
        """
        used to save the updated room data
        """