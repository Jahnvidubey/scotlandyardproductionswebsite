#create_tables.py
from database import Base, engine
import models

print("Dropping existing tables...")
Base.metadata.drop_all(bind=engine)
print("Old tables dropped!")

print("Creating new tables with updated schema...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

# Verify tables
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables in database: {tables}")

# Show columns for contacts table
if 'contacts' in tables:
    columns = inspector.get_columns('contacts')
    print("\nContacts table columns:")
    for column in columns:
        print(f"  - {column['name']}: {column['type']} (nullable: {column['nullable']})")