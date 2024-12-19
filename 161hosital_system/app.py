from flask import Flask, render_template, jsonify
import os
from moviepy.editor import VideoFileClip

import json
import time
from data_processing import process_file, convert_audio_to_text, convert_video_to_text

app = Flask(__name__)  # Initialize the Flask application
UPLOAD_FOLDER = 'uploads/'  # Directory for uploaded files
PROCESSED_FOLDER = 'processed_files/'  # Directory for processed files
AUDIO_VIDEO_FOLDER = 'all_audio_video_files/'  # Directory for audio/video files

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create upload folder if it doesn't exist
os.makedirs(PROCESSED_FOLDER, exist_ok=True)  # Create processed folder if it doesn't exist
os.makedirs(AUDIO_VIDEO_FOLDER, exist_ok=True)  # Create audio/video folder if it doesn't exist

@app.route('/')
def index():
    """
    Render the login page as the home page of the application.
    """
    return render_template('login.html ')

#--------- Conversion of files into .json
def process_all_files():
    """
    Process all files in the upload folder and convert them into .json format.
    """
    for filename in os.listdir(UPLOAD_FOLDER):  # Iterate through files in the upload folder
        file_path = os.path.join(UPLOAD_FOLDER, filename)  # Get full file path
        if not os.path.isfile(file_path):  # Skip directories or invalid files
            continue

        # Define the target .json file name and path
        json_filename = f"{os.path.splitext(filename)[0]}.json"
        processed_path = os.path.join(
            AUDIO_VIDEO_FOLDER if filename.lower().endswith(('.mp3', '.mp4')) else PROCESSED_FOLDER,
            json_filename
        )

        if os.path.exists(processed_path):  # Skip if the file has already been processed
            continue

        try:
            # Handle .mp3 and .mp4 files separately
            if filename.lower().endswith('.mp3'):
                content = convert_audio_to_text(file_path)  # Convert audio to text
            elif filename.lower().endswith('.mp4'):
                content = convert_video_to_text(file_path)  # Convert video to text
            else:
                # Process other file types
                content = process_file(file_path, PROCESSED_FOLDER)

            # Save content as a .json file
            with open(processed_path, 'w', encoding='utf-8') as json_file:
                if isinstance(content, dict):  # If content is a dictionary, write directly
                    json.dump(content, json_file, indent=4)
                else:
                    json_file.write(json.dumps({"content": content}, indent=4))  # Wrap non-dict content in a dictionary
            print(f"Processed {filename} to {processed_path}".encode('utf-8'))
        except Exception as e:
            # Log any errors during file processing
            print(f"Failed to process {filename}: {e}".encode('utf-8'))

@app.route('/process_files', methods=['POST'])
def trigger_processing():
    """
    API endpoint to manually trigger file processing.
    """
    process_all_files()  # Process all files in the upload folder
    return jsonify({"status": "success", "message": "All files processed"}), 200

if __name__ == "__main__":
    """
    Run the Flask application and periodically process files every 10 seconds.
    """
    # Automatically check and process files every 10 seconds
    while True:
        process_all_files()  # Process files
        time.sleep(10)  # Wait 10 seconds before checking again
    app.run(debug=True)  # Run the app in debug mode

# Password Reset:

# Save the hashed password (e.g., using bcrypt).
# Example (Python):

from werkzeug.security import generate_password_hash

def reset_password(user_id, new_password):
    """
    Reset the password for a user by saving the hashed password.
    """
    hashed_pw = generate_password_hash(new_password)  # Hash the new password
    # Update the password in the database
