import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('database/abandoned_checkout.db')

# Read and execute the SQL schema
with open('database/schema.sql', 'r') as f:
    schema = f.read()

conn.executescript(schema)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully!")