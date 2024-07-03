import psycopg2
from psycopg2 import sql
from blob_to_img import convert_local_blob_to_image

# Database connection parameters
dbname = "garbage"
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
def blob():
    identifier='1'
    # Create a cursor object
    cursor = conn.cursor()

    sql = f"""
            SELECT image
            FROM captured_data
            WHERE 1 = (%s);
        """

    try:
        

        # Execute the SQL query
        cursor.execute(sql, (identifier),)
        row = cursor.fetchone()
        # Commit the transaction
        conn.commit()
        print("added.")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback the transaction in case of error
        conn.rollback()
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

    if row:
            blob_data=row[0]
            return(blob_data)
    

blob_img=blob()
with open("/Users/shrishaa/Garbage/website/imagesss/db_blob/retrieved_blob3.txt", "wb") as f:
        f.write(blob_img)
        img=convert_local_blob_to_image(f)








