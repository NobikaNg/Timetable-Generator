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

class Room:
    def __init__(self, room_id, room_name, working_dates, new):
        self.room_id = room_id
        self.room_name = room_name
        self.working_dates = working_dates
        self.session_list = []

        if new:
            self.save()
    
    def save(self):
        query = """
            INSERT INTO ROOM (room_id, room_name, working_dates, session_list)
            VALUES (?, ?, ?, ?)
        """
        params = (self.room_id, self.room_name, ",".join(self.working_dates), ",".join(self.session_list))
        Database.execute_query(query, params)
        logging.info(f"Room {self.room_name} has been saved to database")
    
    @staticmethod
    def edit_room_info(room_id, **kwargs):
        """Edit room attributes and update the ROOM table."""
        for key, value in kwargs.items():
            if key in ["working_dates", "session_list"]:
                value = ",".join(value)
            query = f"UPDATE ROOM SET {key} = ? WHERE room_id = ?"
            Database.execute_query(query, (value, room_id))
        logging.info(f"Room {room_id}'s data has been updated")
        clear_auto_schedule()
        token_distribution()
    
    @staticmethod
    def delete_room(room_id):
        """Delete a room from the ROOM table."""
        query = "DELETE FROM ROOM WHERE room_id = ?"
        Database.execute_query(query, (room_id,))
        logging.info(f"Room {room_id} has been deleted from the database")
        clear_auto_schedule()
        token_distribution()
    
    @staticmethod
    def find_room(room_id):
        """Find and return a room record from the ROOM table."""
        query = """
            SELECT room_id, room_name, working_dates, session_list
            FROM ROOM 
            WHERE room_id = ?
        """
        return Database.fetch_one(query, (room_id,))
    
    @staticmethod
    def get_all_rooms():
        """Fetch all room records from the ROOM table."""
        query = "SELECT room_id, room_name, working_dates, session_list FROM ROOM"
        return Database.fetch_all(query)