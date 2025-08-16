import tkinter as tk
from ui.teacher_management import TeacherUI
from ui.room_mangement import RoomUI

def whole_ui_display():
    """Create the main UI window."""
    root = tk.Tk()
    root.geometry("1200x800")
    right_frame = tk.Frame(root)
    right_frame.pack(side="right", anchor="ne", fill="y")

    teacher_ui = TeacherUI(root, list_parent=right_frame)
    room_ui = RoomUI(root, list_parent=right_frame)

    root.mainloop()