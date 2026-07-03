import sqlite3
from pathlib import Path


class DatabaseManager:
    """Handles all SQLite database operations."""

    def __init__(self):
        self.db_path = Path(__file__).parent / "suproc.db"
        self.connection = None
        self.cursor = None

    def connect(self):
        """Open database connection."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()

    def commit(self):
        """Commit changes."""
        self.connection.commit()

    def execute(self, query, params=()):
        """Execute INSERT, UPDATE, DELETE."""
        self.cursor.execute(query, params)

    def fetchall(self, query, params=()):
        """Execute SELECT and return all rows."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=()):
        """Execute SELECT and return one row."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def clear_table(self, table_name):
        """Delete all rows from a table."""
        self.cursor.execute(f"DELETE FROM {table_name}")