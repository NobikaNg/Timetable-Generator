from logic.schedule import clear_auto_schedule, token_distribution
from src.database.database import Database
import logging

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",  
    handlers=[
        logging.StreamHandler(),  
    ]
)

class Session:
    def __init__(self, session_id, session_start, session_end, session_room, session_date, student_count, on_duty_teachers, session_token, new):
        self.session_id = session_id
        self.session_start = session_start
        self.session_end = session_end
        self.session_room = session_room
        self.session_date = session_date
        self.student_count = student_count
        self.on_duty_teachers = on_duty_teachers
        self.session_token = session_token

        if new:
            self.save()
    
    def save(self):
        query = """
            INSERT INTO SESSION (session_id, session_start, session_end, session_room, session_date, student_count, on_duty_teachers, session_token)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (self.session_id, self.session_start, self.session_end, self.session_room, self.session_date, self.student_count, ",".join(self.on_duty_teachers), self.session_token)
        Database.execute_query(query, params)
        logging.info(f"Session {self.session_id} has been saved to database")
    
    @staticmethod
    def edit_session_info(session_id, **kwargs):
        """Edit session attributes and update the SESSION table."""
        for key, value in kwargs.items():
            if key == "on_duty_teachers":
                value = ",".join(value)
            query = f"UPDATE SESSION SET {key} = ? WHERE session_id = ?"
            Database.execute_query(query, (value, session_id))
        logging.info(f"Session {session_id}'s data has been updated")
        clear_auto_schedule()
        token_distribution()
    
    @staticmethod
    def delete_session(session_id):
        """Delete a session from the SESSION table."""
        query = "DELETE FROM SESSION WHERE session_id = ?"
        Database.execute_query(query, (session_id,))
        logging.info(f"Session {session_id} has been deleted from the database")
        clear_auto_schedule()
        token_distribution()
    
    @staticmethod
    def find_session(session_id):
        """Find and return a session record from the SESSION table."""
        query = """
            SELECT session_id, session_start, session_end, session_room, session_date, student_count, on_duty_teachers, session_token 
            FROM SESSION  
            WHERE session_id = ?
        """
        return Database.fetch_one(query, (session_id,))
    
    @staticmethod
    def get_all_session():
        """Fetch all session records from the SESSION table."""
        query = "SELECT session_id, session_start, session_end, session_room, session_date, student_count, on_duty_teachers, session_token FROM SESSION"
        return Database.fetch_all(query)