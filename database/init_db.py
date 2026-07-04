import sqlite3
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent / "suproc.db"

def create_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_suppliers_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT,
        state TEXT,
        product_category TEXT,
        certifications TEXT,
        monthly_capacity INTEGER,
        delivery_days INTEGER,
        rating REAL,
        availability TEXT,
        sustainability_score INTEGER,
        startup_friendly INTEGER,
        previous_projects INTEGER,
        description TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    """)
  
def create_professionals_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professionals (
        professional_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        skills TEXT,
        certifications TEXT,
        preferred_industry TEXT,
        experience_years INTEGER,
        hourly_rate INTEGER,
        remote_available INTEGER,
        city TEXT,
        state TEXT,
        availability TEXT,
        rating REAL,
        created_at TEXT,
        updated_at TEXT
    );
    """)

def create_businesses_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS businesses (
        business_id TEXT PRIMARY KEY,
        company_name TEXT NOT NULL,
        industry TEXT,
        city TEXT,
        state TEXT,
        employee_count INTEGER,
        requirements TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    """)

def create_opportunities_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        opportunity_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        industry TEXT,
        product_category TEXT,
        location TEXT,
        required_skills TEXT,
        budget INTEGER,
        deadline_days INTEGER,
        client_name TEXT,
        priority TEXT,
        status TEXT,
        description TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    """)

def create_procurement_requests_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS procurement_requests (
        request_id TEXT PRIMARY KEY,
        business_id TEXT,
        product_category TEXT,
        quantity INTEGER,
        budget INTEGER,
        deadline TEXT,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY (business_id) REFERENCES businesses(business_id)
    );
    """)

def create_interactions_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        interaction_id TEXT PRIMARY KEY,
        supplier_id TEXT,
        interaction_date TEXT,
        outcome TEXT,
        satisfaction_score INTEGER,
        notes TEXT,
        FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    );
    """)

def main():
    conn = create_connection()
    create_suppliers_table(conn)
    create_professionals_table(conn)
    create_businesses_table(conn)
    create_opportunities_table(conn)
    create_procurement_requests_table(conn)
    create_interactions_table(conn)
    conn.commit()
    conn.close()

    print("✅ Database and tables created successfully!")


if __name__ == "__main__":
    main()  