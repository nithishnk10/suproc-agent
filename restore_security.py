from database.database_manager import DatabaseManager

db = DatabaseManager()
db.connect()

db.execute("""
UPDATE suppliers
SET name = 'Smart Supplies'
WHERE supplier_id = 'SUP-004'
""")

db.commit()
db.close()

print("Supplier restored successfully.")