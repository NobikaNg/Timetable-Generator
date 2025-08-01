import tkinter as tk
from ui.teacher_management import TeacherUI

def whole_ui_display():
    """Create the main UI window."""
    root = tk.Tk()
    root.geometry("800x600")
    teacher_ui = TeacherUI(root)

    root.mainloop()