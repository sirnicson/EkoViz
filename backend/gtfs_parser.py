import csv
import os
import mysql.connector

REQUIRED_GTFS_FILES = ['agency.txt', 'routes.txt', 'trips.txt', 'stops.txt', 'stop_times.txt', 'calendar.txt']

def parse_gtfs_files(extracted_folder):
    """Parse the GTFS files and store their data in memory."""
    gtfs_data = {}

    # Parse each required GTFS file
    for filename in REQUIRED_GTFS_FILES:
        filepath = os.path.join(extracted_folder, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                gtfs_data[filename] = list(reader)  # Store each file's data as a list of dictionaries
        else:
            raise FileNotFoundError(f"File {filename} is missing in {extracted_folder}")

    return gtfs_data

def store_gtfs_data_in_db(gtfs_data):
    """Store the parsed GTFS data in the MySQL database."""
    # Connect to the MySQL database
    db_config = {
        'host': 'localhost',
        'user': 'newuser',
        'password': 'StrongPassword1!',
        'database': 'ekoviz'
    }

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Insert parsed data into respective tables in MySQL
        for filename, data in gtfs_data.items():
            if filename == 'agency.txt':
                # Insert agency data into 'agency' table
                for row in data:
                    cursor.execute("INSERT INTO agency (agency_id, agency_name, agency_url) VALUES (%s, %s, %s)",
                                   (row['agency_id'], row['agency_name'], row['agency_url']))

            elif filename == 'routes.txt':
                # Insert route data into 'routes' table
                for row in data:
                    cursor.execute("INSERT INTO routes (route_id, route_short_name, route_long_name) VALUES (%s, %s, %s)",
                                   (row['route_id'], row['route_short_name'], row['route_long_name']))

            elif filename == 'trips.txt':
                # Insert trip data into 'trips' table
                for row in data:
                    cursor.execute("INSERT INTO trips (trip_id, route_id, service_id) VALUES (%s, %s, %s)",
                                   (row['trip_id'], row['route_id'], row['service_id']))

            elif filename == 'stops.txt':
                # Insert stop data into 'stops' table
                for row in data:
                    cursor.execute("INSERT INTO stops (stop_id, stop_name, stop_lat, stop_lon) VALUES (%s, %s, %s, %s)",
                                   (row['stop_id'], row['stop_name'], row['stop_lat'], row['stop_lon']))

            elif filename == 'stop_times.txt':
                # Insert stop times data into 'stop_times' table
                for row in data:
                    cursor.execute("INSERT INTO stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence) VALUES (%s, %s, %s, %s, %s)",
                                   (row['trip_id'], row['arrival_time'], row['departure_time'], row['stop_id'], row['stop_sequence']))

            elif filename == 'calendar.txt':
                # Insert calendar data into 'calendar' table
                for row in data:
                    cursor.execute("INSERT INTO calendar (service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                   (row['service_id'], row['monday'], row['tuesday'], row['wednesday'], row['thursday'], row['friday'], row['saturday'], row['sunday'], row['start_date'], row['end_date']))

        connection.commit()  # Commit all changes to the database

    except Exception as e:
        connection.rollback()  # Rollback on error
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()