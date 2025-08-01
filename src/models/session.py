import sqlite3
import os
from logic.schedule import clear_auto_schedule, token_distribution
import sys

class Session:
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
        """Connect to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def add_session(self, session_id, session_start, session_end, session_room, session_date, student_count,
                    on_duty_teachers=None, session_token=0):
        """Add a new session to the SESSION table."""
        if on_duty_teachers is None:
            on_duty_teachers = []

        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO SESSION (session_id, session_start, session_end, session_room, session_date, 
                                     student_count, on_duty_teachers, session_token)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (session_id, session_start, session_end, session_room, session_date, student_count,
                  ",".join(on_duty_teachers), session_token))
            conn.commit()   
    
    def edit_session_info(self, session_id, **kwargs):
        """Edit session attributes and update the SESSION table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            for key, value in kwargs.items():
                if key == "on_duty_teachers":
                    value = ",".join(value)  # Convert list to string
                cursor.execute(f"""
                    UPDATE SESSION
                    SET {key} = ?
                    WHERE session_id = ?
                """, (value, session_id))
            conn.commit()
        clear_auto_schedule()
        token_distribution()
    
    def delete_session(self, session_id):
        """Delete a session from the SESSION table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM SESSION WHERE session_id = ?", (session_id,))
            conn.commit()
    
    def find_session(self, session_id):
        """Find and return a session record from the SESSION table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM SESSION WHERE session_id = ?", (session_id,))
            session = cursor.fetchone()
        return session
    
    def get_all_sessions(self):
        """Fetch all teacher records from the TEACHER table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT session_id, session_start, session_end, session_room, session_date, student_count, on_duty_teachers, session_token FROM SESSION")
            sessions = cursor.fetchall()
        return sessions
