import os
import psycopg2

# Connect to the PostgreSQL database
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)

# Create a cursor object
cur = conn.cursor()

# Create the "pdfs" table
create_table_query = """
CREATE TABLE IF NOT EXISTS pdfs (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    upload_date TIMESTAMP NOT NULL,
    text TEXT
);
"""
cur.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()