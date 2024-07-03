# from model import predict,upload_image,receive_coordinates,load_model
# import os

# import psycopg2
# from psycopg2 import sql

# dbname = "garbage_db"
# user = "postgres"
# password = "LIon1965"
# host = "localhost"
# port = "5432"

# conn = psycopg2.connect(
#     dbname=dbname,
#     user=user,
#     password=password,
#     host=host,
#     port=port
# )

# cur = conn.cursor()

# z = [int(os.path.splitext(f)[0]) for f in os.listdir("/Users/shrishaa/Garbage/website/web_imgs/") if os.path.splitext(f)[0].isnumeric()]
# if not z:
#     z = [0]

# model=load_model('/Users/shrishaa/Garbage/yolov5/runs/train/yolo_bag_det/weights/best.pt')

# img_path = f"/Users/shrishaa/Garbage/website/web_imgs/{max(z)+1:04}"
# coord_path=f"/Users/shrishaa/Garbage/website/coordinates/{max(z)+1:04}"
# with open(coord_path+'.txt', "rb") as f:
#     data = f.read().decode('utf-8')  
#     coordinates = data.split(',')    
#     coordinates = [coord.strip() for coord in coordinates]  
#     lat=''
#     lng=''

#     for i in coordinates:
#         lat=i[0]
#         lng=i[1]
    

# pred=predict(model,img_path,img_path)

# insert_query = f"""
#     INSERT INTO detections (image_path, latitude, longitude, detection)
#     VALUES ({img_path}, {lat}, {lng}, {predict});
# """



# # img_path,lat,long,t/f





import psycopg2

# Database connection details
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

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Define your SQL query to select all rows from the 'detection' table
select_query = """
SELECT latitude, longitude
FROM detection
ORDER BY slno DESC
LIMIT 1;


"""

# Execute the query
cur.execute(select_query)

# Fetch all rows from the result set
rows = cur.fetchall()

# Display the fetched rows
for row in rows:
    print(row)

# Close cursor and connection
cur.close()
conn.close()
