from logic.schedule import clear_auto_schedule, token_distribution
from src.database.database import Database
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Output logs to the terminal
        logging.FileHandler("application.log")  # Write logs to a file
    ]
)

class Teacher:
    def __init__(self, teacher_id, name, salary, available_date, start_time, end_time, new):
        self.teacher_id = teacher_id
        self.name = name
        self.salary = salary
        self.available_date = available_date
        self.start_time = start_time
        self.end_time = end_time
        self.working_hr = 0
        self.auto_working_token = 0
        self.assign_working_token = 0
        self.on_duty_session = []

        # if it is a new teacher, save it to the database
        if new:
            self.save()        
    
    def save(self):
            """Saves a new teacher record to the database."""
            query = """
                INSERT INTO TEACHER (teacher_id, name, salary, available_date, start_time, end_time, working_hr,
                                    auto_working_token, assign_working_token, on_duty_session)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.teacher_id, self.name, self.salary, ",".join(self.available_date), self.start_time, self.end_time, self.working_hr,
                    self.auto_working_token, self.assign_working_token, ",".join(self.on_duty_session))
            Database.execute_query(query, params)
            logging.info(f"{self.name} has been saved to database")

              

    @staticmethod
    def edit_teacher_info(teacher_id, **kwargs):
        """Edit teacher attributes and update the TEACHER table."""
        for key, value in kwargs.items():
            if key in ["available_date", "on_duty_session"]:
                value = ",".join(value)
            query = f"UPDATE TEACHER SET {key} = ? WHERE teacher_id = ?"
            Database.execute_query(query, (value, teacher_id))
        
        clear_auto_schedule()
        token_distribution()

    @staticmethod
    def delete_teacher(teacher_id):
        """Delete a teacher from the TEACHER table."""
        query = "DELETE FROM TEACHER WHERE teacher_id = ?"
        Database.execute_query(query, (teacher_id,))
        
        clear_auto_schedule()
        token_distribution()

    @staticmethod
    def find_teacher(teacher_id):
        """Find and return a teacher record from the TEACHER table."""
        query = "SELECT * FROM TEACHER WHERE teacher_id = ?"
        # Here you could convert the returned tuple into a Teacher object if needed
        return Database.fetch_one(query, (teacher_id,))

    @staticmethod
    def get_all_teachers():
        """Fetch all teacher records from the TEACHER table."""
        query = "SELECT teacher_id, name, salary, available_date, start_time, end_time, working_hr FROM TEACHER"
        return Database.fetch_all(query)