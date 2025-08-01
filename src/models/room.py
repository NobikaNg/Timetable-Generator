import sqlite3
import os
from logic.schedule import clear_auto_schedule, token_distribution
import sys

class Room:
    def __init__(self, db_path=None):
        if db_path is None:
            # Handle PyInstaller bundled app
            if getattr(sys, 'frozen', False):
                # Running in a PyInstaller bundle
                bundle_dir = sys._MEIPASS
                self.db_path = os.path.join(bundle_dir, "src", "database", "timetable_generator.db")
            else:
                # Running in normal Python environment
                script_dir = os.path.dirname(os.path.abspath(__file__))
                src_dir = os.path.dirname(script_dir)
                self.db_path = os.path.join(src_dir, "database", "timetable_generator.db")
            self.db_path = os.path.normpath(self.db_path)
        else:
            self.db_path = db_path
    
    def connect_db(self):
        return sqlite3.connect(self.db_path)
    
    def add_room(self, room_id, room_name, working_dates, session_list=None):
        """Add a new room to the ROOM table."""
        if session_list is None:
            session_list = []

        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ROOM (room_id, room_name, working_dates, session_list)
                VALUES (?, ?, ?, ?)
            """, (room_id, room_name, ",".join(working_dates), ",".join(session_list)))
            conn.commit()
    
    def edit_room_info(self, room_id, **kwargs):
        """Edit room attributes and update the ROOM table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            for key, value in kwargs.items():
                if key == "working_dates" or key == "session_list":
                    value = ",".join(value)  # Convert list to string
                cursor.execute(f"""
                    UPDATE ROOM
                    SET {key} = ?
                    WHERE room_id = ?
                """, (value, room_id))
            conn.commit()
        clear_auto_schedule()
        token_distribution()
    
    def delete_room(self, room_id):
        """Delete a room from the ROOM table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ROOM WHERE room_id = ?", (room_id,))
            conn.commit()
        clear_auto_schedule()
        token_distribution()
    
    def find_room(self, room_id):
        """Find and return a room record from the ROOM table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ROOM WHERE room_id = ?", (room_id,))
            room = cursor.fetchone()
        return room
    
    def get_all_rooms(self):
        """Fetch all teacher records from the TEACHER table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT room_id, room_name, working_dates, session_list FROM ROOM")
            rooms = cursor.fetchall()
        return rooms