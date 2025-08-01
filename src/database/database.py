import sqlite3
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Output logs to the terminal
        logging.FileHandler("application.log")  # Write logs to a file
    ]
)


class Database:
    _db_path = None

    @staticmethod
    def get_db_path():
        """Gets the path to the database file, relative to the project root."""
        try:
            if Database._db_path is None:
                if getattr(sys, 'frozen', False):
                    project_root = os.path.dirname(os.path.dirname(sys.executable))
                else:
                    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

                db_path = os.path.join(project_root, "src", "database", "timetable_generator.db")
                Database._db_path = os.path.normpath(db_path)

            if not os.path.exists(Database._db_path):
                raise FileNotFoundError(f"Database file not found at {Database._db_path}")
            logging.info(f"Database path: {Database._db_path} is found")
            return Database._db_path
        except Exception as e:
            logging.error(f"Fail to get the path of database. Error: {e}")
            raise

    @staticmethod
    def execute_query(query, params=()):
        """For executing queries that modify the database (INSERT, UPDATE, DELETE)."""
        try:
            with sqlite3.connect(Database.get_db_path()) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                logging.info(f"{query} Execution Successed")
        except Exception as e:
            logging.error(f"{query} Execution Failed. Error: {e}")

    @staticmethod
    def fetch_one(query, params=()):
        """For fetching a single record from the database."""
        try:
            with sqlite3.connect(Database.get_db_path()) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                logging.info(f"Fetch the required item successful.")
                return cursor.fetchone()
        except Exception as e:
            logging.error(f"Fail to fetch the required item. Error: {e}")

    @staticmethod
    def fetch_all(query, params=()):
        """For fetching all records that match a query."""
        try:
            with sqlite3.connect(Database.get_db_path()) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                logging.info(f"Fetch all required items successful.")
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Fail to fetch all required items. Error: {e}")