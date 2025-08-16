import tkinter as tk
import logging
from tkinter import Toplevel

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
    
    def open_add_room_window(self):
        logging.info("Open Add Room Window")
    
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