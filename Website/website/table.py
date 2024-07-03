import psycopg2
from psycopg2 import sql

# Database connection parameters
dbname = "garbage_db"
user = "postgres"
password = "LIon1965"
host = "localhost"
port = "5432"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)

# Create a cursor object
cur = conn.cursor()

# SQL query to create the table
create_table_query = '''
CREATE TABLE detection(
    slno SERIAL PRIMARY KEY,
    image_path TEXT NOT NULL,
    latitude TEXT NOT NULL,
    longitude TEXT NOT NULL,
    detection BOOLEAN
);

'''

cur.execute(create_table_query)
conn.commit()
conn.close()
cur.close()
# drop_table_query = '''
# DROP TABLE IF EXISTS captured_data;
# '''
# filepath = "/Users/shrishaa/Garbage/website/imagesss/blob"
# with open(filepath, 'rb') as f:
#     blob_data = f.read()

#         # Prepare the SQL insert statement.
#         # If no filename is provided, use a generic name.
# sql = """INSERT INTO captured_data (image) VALUES (%s)"""

# try:
#     # Execute the SQL query
#     cursor.execute(sql, (psycopg2.Binary(blob_data),))
#     # Commit the transaction
#     conn.commit()
#     print("added.")
# except Exception as e:
#     print(f"An error occurred: {e}")
#     # Rollback the transaction in case of error
#     conn.rollback()
# finally:
#     # Close the cursor and connection
#     cursor.close()
#     conn.close()




# # Example usage

filename = "blob"  # No filename provided, so use a generic name
table_name = "captured_data"
column_name = "image"
