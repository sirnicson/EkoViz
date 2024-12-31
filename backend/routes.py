from flask import request
import os
import zipfile
import csv

ALLOWED_EXTENSIONS = {'zip'}
REQUIRED_GTFS_FILES = ['agency.txt', 'routes.txt', 'trips.txt', 'stops.txt', 'stop_times.txt', 'calendar.txt']

# Define the function that handles file upload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_zip_file(file, upload_folder):
    """Extracts the contents of the uploaded .zip file into the specified directory."""
    zip_path = os.path.join(upload_folder, file.filename)
    file.save(zip_path)
    extracted_folder = os.path.join(upload_folder, file.filename.rsplit('.', 1)[0])

    # Extract the zip file contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)

    # Remove the .zip file after extraction
    os.remove(zip_path)
    
    return extracted_folder

def validate_gtfs_files(extracted_folder):
    """Validate that all required GTFS files are present in the extracted folder."""
    missing_files = [f for f in REQUIRED_GTFS_FILES if not os.path.exists(os.path.join(extracted_folder, f))]
    if missing_files:
        return f"Missing required GTFS files: {', '.join(missing_files)}"
    return None

def upload_file(app):
    # Ensure the uploads directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            # Step 1: Extract the GTFS .zip file
            extracted_folder = extract_zip_file(file, app.config['UPLOAD_FOLDER'])

            # Step 2: Validate that all required GTFS files are present
            validation_error = validate_gtfs_files(extracted_folder)
            if validation_error:
                return validation_error

            # Step 3: Parse the required GTFS files (we'll just check CSV headers for now)
            gtfs_files = {filename: os.path.join(extracted_folder, filename) for filename in REQUIRED_GTFS_FILES}
            for filename, filepath in gtfs_files.items():
                if not os.path.exists(filepath):
                    return f"GTFS file {filename} is missing or corrupted."

                with open(filepath, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    headers = next(reader, None)  # Read the header row
                    if not headers:
                        return f"GTFS file {filename} is empty or malformed."

            return f"GTFS file validated and uploaded successfully."

    return '''
        <!doctype html>
        <title>Upload GTFS File</title>
        <h1>Upload GTFS .zip file</h1>
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
    '''
