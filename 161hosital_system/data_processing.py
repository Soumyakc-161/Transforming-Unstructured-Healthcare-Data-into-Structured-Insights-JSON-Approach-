#--------------WHY THESE LIBRARIES --------------------------------------------------

#os: Provides a way to use operating system-dependent functionality, such as reading or writing files and interacting with the file system.
#json: Allows for parsing and generating JSON (JavaScript Object Notation), which is a popular data interchange format.
#csv: Facilitates reading from and writing to CSV (Comma-Separated Values) files, commonly used for data exchange.
#docx: Used to create, modify, and read Microsoft Word documents (specifically the .docx format).
#xml.etree.ElementTree: Provides tools for parsing and creating XML (Extensible Markup Language) data.
#pdfminer.high_level: Offers capabilities to extract text from PDF files, allowing for text-based data extraction from documents.
#pydub: A simple and easy-to-use library for audio manipulation, including importing, exporting, and editing audio files.
#moviepy.editor: Used for video editing, including basic operations like cutting, concatenating videos, and exporting them in various formats.
#zipfile: Allows for reading and writing ZIP (compressed archive) files, useful for handling compressed data.
#sqlite3: Provides a lightweight database engine for storing and retrieving data using SQL commands.
#PIL (Python Imaging Library): Specifically, Pillow, an imaging library used for opening, manipulating, and saving image files.
#pytesseract: A Python wrapper for Tesseract, an OCR (Optical Character Recognition) tool that allows you to convert images of text into machine-encoded text.
#xlrd: Used for reading data and formatting information from Excel files (.xls).
#email: A module to manage email messages, including constructing, parsing, and sending emails. It includes various utilities such as:
#policy: Helps define parsing policies for email messages.
#BytesParser: Parses email messages from byte streams.
#getaddresses: Retrieves email addresses from headers.
#base64: Provides methods for encoding and decoding data using Base64, commonly used for encoding binary data in email.
#speech_recognition: Provides functionalities for recognizing speech, allowing audio files or live microphone input to be converted into text.

#'''''''''''''''''''''''''''''''''................................''''''''''''''''''''''''''''''''''''


# importing all the requeried libries
import os     #Provides a way to use operating system-dependent functionality, such as reading or writing files and interacting with the file system.
import json
import csv
from docx import Document
import xml.etree.ElementTree as ET
from pdfminer.high_level import extract_text
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import zipfile
import sqlite3
from PIL import Image
import pytesseract  
import xlrd
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import email
import speech_recognition as sr


from email import policy
from email.parser import BytesParser
from email.utils import getaddresses
import base64


from pdfminer.high_level import extract_text

# ------------define processe files ------------------------------all types of unstructured data files --------
def process_file(file_path, output_dir):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.txt':
        return process_txt(file_path)
    elif ext == '.docx':
        return process_docx(file_path)
    elif ext == '.pdf':
        return process_pdf(file_path)
    elif ext == '.csv':
        return process_csv(file_path)
    elif ext == '.eml':
        return process_eml(file_path)
    elif ext == '.msg':
        return process_msg(file_path)
    elif ext == '.log':
        return process_log(file_path)
    elif ext == '.xls':
       return process_xls(file_path)
    elif ext == '.xlsx':
        return process_xlsx(file_path)

    elif ext == '.xml':
        return process_xml(file_path)
    elif ext in ['.mp4', '.avi', '.mkv']:
        return process_video(file_path)
    elif ext in ['.mp3', '.wav', '.flac']:
        return process_audio(file_path)
    elif ext in ['.jpg', '.png', '.gif']:
        return process_image(file_path)
    elif ext in ['.zip', '.rar', '.7z']:
        return process_compressed(file_path)
    elif ext in ['.xls', '.xlsx']:
        return process_xls(file_path)
    elif ext in ['.html', '.htm']:
        return process_html(file_path)
    elif ext in ['.sql', '.sqlite', '.mdb']:
        return process_database(file_path)
    elif ext in ['.exe', '.bat', '.sh']:
        return {"content": "Executable files cannot be processed for content due to security concerns."}
    else:
        raise ValueError(f"Unsupported file format: {ext}")


# ----------START HERE...--- convsrion of text formated files .txt into .json -------------=========================
def process_txt(file_path):
    with open(file_path, 'r') as f:
        return {"content": f.read()}

#------------END HERE ----------------------=======================================-
# ------START HERE--------- conversion of excel files .xlsx files into .json -----------------------------------
def process_xlsx(file_path):
    try:
        import pandas as pd
        data = pd.read_excel(file_path, engine="openpyxl")
        return data.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Failed to process {file_path}: {e}")

#----------================END HERE =================================
    
# ----START HERE...........--- conversion of documents .docx files into .json ------------------------------------
import json
import os
from docx import Document

# Function to process DOCX content into structured JSON
def process_docx(file_path):
    try:
        doc = Document(file_path)
        content = {
            "title": None,
            "sections": {}
        }

        current_section = None
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue

            if content["title"] is None:
                content["title"] = text
            elif para.style.name.startswith("Heading"):
                current_section = text
                content["sections"][current_section] = []
            elif current_section:
                content["sections"][current_section].append(text)

        return content
    except Exception as e:
        return {"error": f"Unable to process DOCX: {str(e)}"}

# Function to convert file to JSON and save the result
def convert_file_to_json(file_path, output_dir):
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    file_extension = file_path.split('.')[-1].lower()
    if file_extension == 'docx':
        result = process_docx(file_path)
    else:
        return {"error": "Unsupported file type"}

    output_file = os.path.join(output_dir, os.path.basename(file_path).replace(f'.{file_extension}', '.json'))
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    return f"Processed {file_path} to {output_file}"

# File paths (update with your actual DOCX file paths)
file_paths = [
    'C:/Users/DELL/Downloads/MedicalReport(1).docx',
    'C:/Users/DELL/Downloads/queries.docx',
]

# Output directory
output_dir = 'processed_files'
os.makedirs(output_dir, exist_ok=True)

# Process each file
for file_path in file_paths:
    print(f"Processing file: {file_path}")
    result = convert_file_to_json(file_path, output_dir)
    print(result)

#---------------END HERE.................-----------------------------============================================================================-------------------------------

#---====START HERE .........................------- converting pdf files into .json  
# in this 1st extract the text from pdf, then clean the text, Parse text into structured sections based on headings or patterns.
# then Split section content into a list of bullet points based on bullet patterns.
import os
import json
from PyPDF2 import PdfReader

# Function to extract text from a PDF file
def extract_pdf_text(file_path):
    """
    Extract text from a PDF file, handling large files and skipping unreadable pages.
    """
    reader = PdfReader(file_path)  # Initialize the PDF reader
    text = ""  # Initialize an empty string to store text
    for i, page in enumerate(reader.pages):  # Iterate through each page in the PDF
        try:
            text += page.extract_text() + "\n"  # Extract text and add a newline
        except Exception as e:
            # Print a warning if text extraction fails for a page
            print(f"Warning: Failed to extract text from page {i+1} of {file_path}: {e}")
    return text  # Return the extracted text

# Function to clean extracted text
def clean_text(text):
    """
    Clean up the extracted text by removing excessive newlines and unnecessary spaces.
    """
    lines = text.split("\n")  # Split the text into lines
    cleaned_lines = [line.strip() for line in lines if line.strip()]  # Remove extra spaces and blank lines
    return "\n".join(cleaned_lines)  # Join the cleaned lines into a single string

# Function to parse text into structured sections
def parse_sections(pdf_text):
    """
    Parse text into structured sections based on headings or patterns.
    """
    sections = {}  # Initialize a dictionary to store sections
    lines = pdf_text.split("\n")  # Split the text into lines
    current_section = None  # Variable to keep track of the current section
    section_content = []  # List to store content for the current section

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace

        # Detect section headers (e.g., titles and subtitles)
        if line.endswith(":") or line.isupper():  # Identify headers based on patterns
            # Save the previous section if one exists
            if current_section:
                sections[current_section] = "\n".join(section_content).strip()
                section_content = []  # Reset the content list

            current_section = line.rstrip(":")  # Set the new section title and remove trailing colon
        else:
            section_content.append(line)  # Append the line to the current section's content

    # Save the last section after looping through all lines
    if current_section:
        sections[current_section] = "\n".join(section_content).strip()

    return sections  # Return the structured sections

# Function to split section content into bullet points
def split_bullets(section_content):
    """
    Split section content into a list of bullet points based on bullet patterns.
    """
    bullets = ["•", "-", "*"]  # Define common bullet characters
    content_list = []  # Initialize a list to store split content

    # Split the content into individual lines
    for line in section_content.split("\n"):
        line = line.strip()  # Remove leading/trailing whitespace
        if any(line.startswith(bullet) for bullet in bullets):  # Check if the line starts with a bullet
            content_list.append(line[1:].strip())  # Remove the bullet and strip extra spaces
        elif line:  # Include lines without explicit bullets
            content_list.append(line)

    return content_list  # Return the list of content as bullet points

# Function to convert sections into a JSON structure
def convert_to_json(sections):
    """
    Convert parsed sections into the desired JSON structure.
    """
    result = {
        "title": "Cardiovascular Diseases",  # Set a predefined title
        "subtitle": "Acute Coronary Syndrome",  # Set a predefined subtitle
        "sections": {}  # Initialize an empty dictionary for sections
    }

    for section_title, section_content in sections.items():  # Loop through each section
        content_list = split_bullets(section_content)  # Convert section content into a list
        result["sections"][section_title] = content_list  # Add the list to the JSON structure

    return result  # Return the final JSON structure

# Function to process a single PDF file
def process_pdf(file_path):
    """
    Process the PDF file, extract text, parse sections, and convert to JSON.
    """
    pdf_text = extract_pdf_text(file_path)  # Extract text from the PDF
    cleaned_text = clean_text(pdf_text)  # Clean the extracted text
    sections = parse_sections(cleaned_text)  # Parse the cleaned text into sections
    converted_json = convert_to_json(sections)  # Convert sections to a JSON structure

    return converted_json  # Return the JSON structure

# Function to process multiple PDFs and save the output
def process_selected_pdfs(file_paths, output_folder):
    """
    Process specified PDF files and save the converted JSON files to an output folder.
    """
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    for file_path in file_paths:  # Iterate through each PDF file path
        try:
            converted_data = process_pdf(file_path)  # Process the PDF and generate JSON
            json_file_name = os.path.basename(file_path).replace('.pdf', '.json')  # Create a JSON file name
            json_path = os.path.join(output_folder, json_file_name)  # Define the full path for the JSON file

            with open(json_path, 'w', encoding='utf-8') as json_file:  # Open the JSON file for writing
                json.dump(converted_data, json_file, indent=4)  # Write the JSON data to the file

            print(f"Processed and saved: {json_path}")  # Print a success message
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")  # Print an error message if processing fails

# List of PDF file paths to process
file_paths = [
    'C:/Users/DELL/Downloads/NLEM.pdf',
    'C:/Users/DELL/Downloads/pdf_format.pdf'
]

# Output folder for saving JSON files
output_folder = 'C:/Users/DELL/Downloads/Processed_JSON'

# Run the processing for the specified PDF files
process_selected_pdfs(file_paths, output_folder)

#--------------================End Here ...................=========================------------------------------------------=============================================----------------------

# .........Start here...............-- converting csv files into .json ==================---------------............................................
def process_csv(file_path):
    """
    Process a CSV file and return its contents as a list of dictionaries.
    Each row in the CSV file is converted into a dictionary where keys are column headers.
    """
    data = []  # Initialize an empty list to store the processed data
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:  # Open the CSV file with specified encoding
        # Use 'utf-8-sig' encoding to handle files with a Byte Order Mark (BOM); try 'latin1' if needed
        reader = csv.DictReader(csvfile)  # Create a DictReader to read rows as dictionaries
        for row in reader:  # Iterate through each row in the CSV file
            data.append(row)  # Append the row (as a dictionary) to the data list
    return data  # Return the processed data


#============================----------------------------------------========================================------------
# converting .xml data files into .json 
def process_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    def parse_element(element):
        parsed_data = {element.tag: {} if element.attrib else None}
        children = list(element)
        if children:
            child_data = {}
            for child in children:
                child_data.update(parse_element(child))
            parsed_data[element.tag] = child_data
        else:
            parsed_data[element.tag] = element.text
        return parsed_data
    return parse_element(root)
#-------------------------=============================================---------------------------==================
# converting email related data files into .json 

def process_eml(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

        # Extract metadata
        subject = msg["subject"]
        sender = msg["from"]
        recipients_to = [addr[1] for addr in getaddresses([msg["to"]])] if msg["to"] else []
        recipients_cc = [addr[1] for addr in getaddresses([msg["cc"]])] if msg["cc"] else []
        recipients_bcc = [addr[1] for addr in getaddresses([msg["bcc"]])] if msg["bcc"] else []
        date = msg["date"]

        # Extract the email body (plain text or HTML)
        body = None
        if msg.is_multipart():
            for part in msg.iter_parts():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_content()
                    break
                elif content_type == "text/html":
                    body = part.get_content()
        else:
            body = msg.get_content()

        # Extract attachments
        attachments = []
        if msg.is_multipart():
            for part in msg.iter_parts():
                if part.get_content_disposition() and part.get_content_disposition().startswith('attachment'):
                    attachment = {
                        "type": part.get_content_type(),
                        "name": part.get_filename(),
                        "content_transfer_encoding": part["Content-Transfer-Encoding"],
                        "content_disposition": part.get_content_disposition(),
                        "content": base64.b64encode(part.get_payload(decode=True)).decode('utf-8')
                    }
                    attachments.append(attachment)

        # Construct the JSON-like dictionary
        email_data = {
            "subject": subject,
            "from": sender,
            "to": recipients_to,
            "cc": recipients_cc,
            "bcc": recipients_bcc,
            "date": date,
            "body": body,
            "attachments": attachments
        }

        return email_data

#----------------=====================================------------------------------------============================
# converting message related data into .json
def process_msg(file_path):
    # Use an external library like `extract_msg` for .msg files
    import extract_msg
    msg = extract_msg.Message(file_path)
    return {
        "subject": msg.subject,
        "from": msg.sender,
        "to": msg.to,
        "date": msg.date,
        "body": msg.body
    }

# ======================------------------------------==================================---------
#converting handwritten letters (image) converting into .json
import json  
from PIL import Image, ImageEnhance  
import pytesseract  
import os  

def preprocess_image(file_path):  
    with Image.open(file_path) as img:  
        # Convert to grayscale  
        img = img.convert("L")  
        # Enhance contrast  
        enhancer = ImageEnhance.Contrast(img)  
        img = enhancer.enhance(2)  # Adjust the contrast factor as needed  
        # Resize if needed  
        img = img.resize((img.width * 2, img.height * 2), Image.ANTIALIAS)  
        return img  

def process_image(file_path):  
    try:  
        # Confirm file exists  
        if not os.path.exists(file_path):  
            print(f"File not found: {file_path}")  
            return None  
        
        # Preprocess the image before OCR  
        img = preprocess_image(file_path)  
        img.save("debug_preprocessed_image.jpg")  # Save for debugging  

        # Perform OCR  
        text = pytesseract.image_to_string(img, lang='eng')  
        print("Extracted Text:", text)  # Print extracted text for debugging  

        # Initialize the JSON object  
        data = {  
            "date": "",  
            "name": "",  
            "age": "",  
            "address": "",  
            "prescriptions": []  
        }  

        # Split the text into lines  
        lines = text.splitlines()  

        # Extract date (assuming it's the first line)  
        if lines:  
            data["date"] = lines[0].strip()  

        # Define a mapping for medications and their instructions  
        medication_instructions = {  
            "Celebrex": ("200 mg", "2 times a day"),  
            "Zovirax": ("200 mg", "as needed"),  
            "Domperidone": ("7.5 mg", "as needed"),  
            "Zantac": ("300 mg", "as needed")  
        }  

        # Iterate through the lines to extract medications  
        for line in lines[1:]:  
            line = line.strip()  
            if line:  
                for medication, (dosage, instructions) in medication_instructions.items():  
                    if medication in line:  
                        data["prescriptions"].append({  
                            "medication": medication,  
                            "dosage": dosage,  
                            "instructions": instructions  
                        })  

        return data  

    except Exception as e:  
        print(f"Error processing image: {e}")  
        return None  # Return None on error  

# Example usage  
file_path = "preprocessed_image-1.jpg"  # Ensure this path is correct  
image_data = process_image(file_path)  
if image_data:  
    print(json.dumps(image_data, indent=4))  # Pretty-print the JSON data  
else:  
    print("No data extracted.")
#==========---------------------------------------------=====================================-----------------------
# converting audio files into .json

def transcribe_audio(file_path):
    # Convert audio to WAV format (required for SpeechRecognition)
    audio = AudioSegment.from_file(file_path)
    wav_path = file_path.replace(file_path.split('.')[-1], 'wav')
    audio.export(wav_path, format='wav')

    # Transcribe audio using SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Audio not clear enough to transcribe."
        except sr.RequestError:
            text = "Error connecting to speech recognition service."

    # Cleanup temporary WAV file
    os.remove(wav_path)

    return text

#-----------------------------------------------------================================-----------------------------------------------========
#converting video files which are related to medical 
def transcribe_video(file_path):
    # Extract audio from video
    video = VideoFileClip(file_path)
    audio_path = "temp_audio.mp3"
    video.audio.write_audiofile(audio_path)

    # Transcribe extracted audio
    text = transcribe_audio(audio_path)

    # Cleanup temporary audio file
    os.remove(audio_path)

    return text

# Metadata and content transcription
def convert_audio_to_text(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = audio.duration_seconds
    metadata = {
        "filename": os.path.basename(file_path),
        "duration": duration,
        "frame_rate": audio.frame_rate,
        "channels": audio.channels,
    }
    metadata["transcription"] = transcribe_audio(file_path)
    return json.dumps(metadata, indent=4)

def convert_video_to_text(file_path):
    video = VideoFileClip(file_path)
    metadata = {
        "filename": os.path.basename(file_path),
        "duration": video.duration,
        "fps": video.fps,
        "size": video.size,
    }
    metadata["transcription"] = transcribe_video(file_path)
    return json.dumps(metadata, indent=4)

#--------------=============================================-------------
# if the data is present in html format that html data files into .json
def process_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        return {
            "title": soup.title.string if soup.title else "No title",
            "body": soup.get_text()
        }

#-----------------------------==========================================================----------------------
# excel files .xls into .json conversion
def process_xls(file_path):
    try:
        data = pd.read_excel(file_path, engine="xlrd")
        return data.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Failed to process {file_path}: {e}")

#---=============-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-================-=-=-=-=-=-=-=-======================-=-=-=-=-=-=-------------
# compressed files zip files into .json 


def process_compressed(file_path, output_dir):
    extracted_data = {}
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
        file_list = zip_ref.namelist()
        for file_name in file_list:
            extracted_file_path = os.path.join(output_dir, file_name)
            if os.path.isfile(extracted_file_path):
                try:
                    extracted_data[file_name] = process_file(extracted_file_path, output_dir)
                except Exception as e:
                    extracted_data[file_name] = f"Failed to process: {e}"
    return extracted_data

#................................-----------------------------------------------.....................................---------------------------
def process_xml(file_path):
    """
    Process an XML file and return its contents as a nested dictionary structure.
    """
    tree = ET.parse(file_path)  # Parse the XML file into an ElementTree
    root = tree.getroot()  # Get the root element of the XML

    def parse_element(element):
        """
        Recursively parse an XML element and its children into a dictionary.
        """
        # Initialize a dictionary with the element's tag as the key
        parsed_data = {element.tag: {} if element.attrib else None}
        children = list(element)  # Get the child elements
        if children:
            for child in children:  # Iterate through child elements
                # Recursively parse each child and update the dictionary
                parsed_data[element.tag].update(parse_element(child))
        else:
            # Assign the text content of the element if it has no children
            parsed_data[element.tag] = element.text
        return parsed_data

    return parse_element(root)  # Parse the root element and return the result


def process_log(file_path):
    """
    Process a log file and return its contents as a list of lines.
    """
    with open(file_path, 'r', encoding='utf-8') as f:  # Open the log file in read mode
        return {"lines": f.readlines()}  # Read all lines and return them in a dictionary


def process_xls(file_path):
    """
    Process an Excel file (in .xls format) and return its contents as a dictionary.
    Each key in the dictionary corresponds to a sheet name, and the value is a list of rows.
    """
    workbook = xlrd.open_workbook(file_path)  # Open the Excel file using xlrd
    data = {}  # Initialize an empty dictionary to store sheet data
    for sheet in workbook.sheets():  # Iterate through all sheets in the workbook
        sheet_data = []  # Initialize a list to store rows of the current sheet
        for row_idx in range(sheet.nrows):  # Iterate through each row in the sheet
            row = sheet.row_values(row_idx)  # Get the values of the row
            sheet_data.append(row)  # Append the row to the sheet data
        data[sheet.name] = sheet_data  # Add the sheet data to the dictionary with the sheet name as the key
    return data  # Return the processed data


#--------------===================================================================--------------------------------------------
def process_compressed(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()  # List of files in archive
    return {"contents": file_list}

#--------------===================================================================--------------------------------------------
def process_database(file_path):
    data = []
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table = table_name[0]
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        data.append({"table": table, "columns": columns})
    conn.close()
    return data
#-----------------------============================........................................
def convert_audio_to_text(file_path):
    audio = AudioSegment.from_file(file_path)
    duration = audio.duration_seconds
    metadata = {
        "filename": os.path.basename(file_path),
        "duration": duration,
        "frame_rate": audio.frame_rate,
        "channels": audio.channels,
    }
    return json.dumps(metadata, indent=4)

#....................----------------------------===============================---------------------------
def convert_video_to_text(file_path):
    video = VideoFileClip(file_path)
    metadata = {
        "filename": os.path.basename(file_path),
        "duration": video.duration,
        "fps": video.fps,
        "size": video.size,
    }
    return json.dumps(metadata, indent=4)



def extract_metadata(file_path):
    if file_path.endswith(('mp3', 'wav', 'flac')):
        audio = AudioSegment.from_file(file_path)
        metadata = {
            'duration': audio.duration_seconds,
            'frame_rate': audio.frame_rate,
            'channels': audio.channels,
            'sample_width': audio.sample_width
        }
    elif file_path.endswith(('mp4', 'avi', 'mkv')):
        video = VideoFileClip(file_path)
        metadata = {
            'duration': video.duration,
            'fps': video.fps,
            'size': video.size
        }
    else:
        raise ValueError("Unsupported file format")
    return metadata

def save_metadata_to_json(metadata, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

def process_file_with_conversion(input_file, output_dir):
    audio_formats = ['mp3', 'wav', 'flac']
    video_formats = ['mp4', 'avi', 'mkv']
    
    ext = os.path.splitext(input_file)[1][1:]
    
    if ext in audio_formats:
        for fmt in audio_formats:
            if fmt != ext:
                converted_file = convert_audio(input_file, fmt, output_dir)
                metadata = extract_metadata(converted_file)


# end .......