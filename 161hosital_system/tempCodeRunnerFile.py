from flask import Flask, render_template, jsonify
import os
import json
import time
from data_processing import process_file
import xlrd

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed_files/'

# Ensure directories exist
os.makedirs(UPLOZAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

def process_all_files():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Skip processing if already converted
        json_filename = f"{os.path.splitext(filename)[0]}.json"
        processed_path = os.path.join(PROCESSED_FOLDER, json_filename)

        if not os.path.exists(processed_path) and os.path.isfile(file_path):
            try:
                # Process the file based on its format
                processed_data = process_file(file_path, PROCESSED_FOLDER)

                # Save processed data as JSON
                with open(processed_path, 'w', encoding='utf-8') as json_file:
                    json.dump(processed_data, json_file, indent=4)

                print(f"Processed {filename} to {processed_path}".encode('utf-8'))
            except Exception as e:
                print(f"Failed to process {filename}: {e}".encode('utf-8'))

@app.route('/process_files', methods=['POST'])
def trigger_processing():
    process_all_files()
    return jsonify({"status": "success", "message": "All files processed"}), 200

if __name__ == "__main__":
    # Automatically check and process files every 10 seconds
    while True:
        process_all_files()
        time.sleep(10)  # Check every 10 seconds
    app.run(debug=True)
