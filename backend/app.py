from flask import Flask
from routes import upload_file
import mysql.connector

app = Flask(__name__)

# Configure app settings here
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return "Backend is running"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return upload_file(app)  # Pass app object to the route handler

if __name__ == "__main__":
    app.run(debug=True)
