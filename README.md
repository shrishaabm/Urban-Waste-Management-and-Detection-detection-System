# Garbage Detection Website

Welcome to the Garbage Detection Website! This project aims to help keep our streets clean by using machine learning to detect garbage from photos uploaded by users.

## Features

- **Upload Photos**: Users can take a photo of garbage on the street and upload it to the website.
- **Garbage Detection**: The uploaded photo is processed by a YOLO-based machine learning model via FastAPI to classify if there is garbage or not.
- **Database Storage**: The system stores the image, latitude, longitude, and the true/false result in a PostgreSQL database.
- **Map Integration**: If garbage is detected, a marker is placed on a map using the Leaflet API, indicating the presence of garbage.
- **Interactive Map**: Users can view locations with detected garbage on an interactive map, making it easier to identify areas that need cleaning.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI
- **Machine Learning**: YOLO (You Only Look Once)
- **Database**: PostgreSQL
- **Map API**: Leaflet API
