# EkoViz

## Purpose and Goals
EkoViz is a simple web application designed to help users visualize public transit data using GTFS (General Transit Feed Specification) files. By providing an easy-to-use platform, EkoViz aims to improve access to transit information, allowing users to better understand and analyze transit routes, stops, and shapes. The core functionality of the application includes uploading, validating, and parsing GTFS .zip files, followed by visualizing the parsed data on an interactive map. 

## Features
- File Upload: Upload GTFS .zip files directly through the web interface.
- Validation: Check the validity of GTFS files.
- Interactive Map: Visualize transit routes, stops, and shapes using Leaflet.js.

## Technologies Used
1. Backend
- Python with Flask: For server-side logic and handling user inputs.
- gtfslib: A Python library for parsing and validating GTFS data.
2. Frontend
- HTML/CSS/JavaScript: For the user interface.
3. Database
- MySQL: For storing parsed GTFS data for efficient querying.
4. Visualization
- Leaflet.js: For rendering maps and visualizing transit routes.
