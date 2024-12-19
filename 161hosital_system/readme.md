# Transforming-Unstructured-Healthcare-Data-into-Structured-Insights-JSON-Approach-

```markdown
# Hospital System Project

This project is designed to process unstructured data files such as PDFs, Excel files, and CSV files, convert them into structured JSON format, and serve this data through a web interface. 

## Project Structure

The project is organized as follows:

```
161HOSPITAL_SYSTEM/
│
├── all_audio_video_files/       # Folder containing all audio and video files for conversion
├── processed_files/             # Folder containing all the processed .json files
├── static/                      # Static files for front-end (CSS, JS, images)
├── templates/                   # HTML, CSS, and JS files for the front-end interface
├── uploads/                     # Folder containing unstructured files (PDF, XLSX, CSV, etc.)
├── app.py                       # Main Python backend file to handle routes and logic
├── data_processing.py           # Python script for converting unstructured files to JSON
├── package-lock.json            # Package lock file for npm dependencies
├── package.json                 # Node.js project configuration file
├── readme.md                    # Project description
├── requirements.txt             # Python dependencies for the project
├── server.js                    # Server file to run the application on localhost
└── tempCodeRunnerFile.py        # Temporary code file (usually for testing)
```
myenv, node_modules, chatbot-backed in these folder all requeried lib are installed to run localhost
## Features

- **Data Conversion**: The system converts unstructured files (PDF, CSV, XLSX) to structured JSON format using the `data_processing.py` script. The converted files are then stored in the `processed_files/` folder.
   
- **Audio and Video Conversion**: Audio and video files are converted into JSON format and stored in the `all_audio_video_files/` folder. The processed files are then saved in the `processed_files/` folder.

- **Front-End Interface**: The `templates/` folder contains the necessary HTML, CSS, and JavaScript code to create a simple front-end for interacting with the system. It provides the user interface for uploading files and viewing the processed results.

- **Unstructured Data**: The `uploads/` folder is used to store unstructured data files such as PDFs, XLSX files, CSV files, etc.

- **Localhost Server**: The `server.js` file runs a local server for testing and development. It serves the front-end files and connects to the back-end functionality.

## How to Run

### 1. Install Dependencies

For Python:
```bash
pip install -r requirements.txt
```

For Node.js:
```bash
npm install
```

### 2. Run the Server

To run the backend:
```bash
python app.py
```

To run the frontend on localhost:
```bash
node server.js
```

### 3. Access the Web Interface

Once the server is running, you can access the web interface by navigating to `http://localhost:3000/` .

### 4. Upload Files

You can upload unstructured files (e.g., PDF, CSV, XLSX) on uploads folder. The files will be processed and stored in the `processed_files/` folder in JSON format.

## Files Description

- **`app.py`**: This is the main backend file for the project. It contains the routes and logic to interact with the front-end, process uploaded files, and display results.

- **`data_processing.py`**: This script contains the code to convert unstructured data files (such as PDFs, CSVs, and XLSX) into JSON format. It processes the files in the `uploads/` folder and stores the converted files in the `processed_files/` folder.
         The code provided **does not implement any explicit machine learning algorithm or statistical model**. Instead, it performs **data extraction, parsing, cleaning, and transformation** for various file formats such as DOCX, PDF, CSV, XML, and EML into structured JSON format.

Here is the breakdown of what the code does in data_processing.py file:
---

### **Algorithms/Methods Used**:
1. **File Parsing and Text Extraction**:
   - *DOCX Files*:  
     - Reads `.docx` files using the `python-docx` library.
     - Identifies headings based on styles like "Heading" to structure content into sections.
   - *PDF Files*:  
     - Uses `PyPDF2` to extract text from each page of a PDF.
     - Handles text cleaning (removing unnecessary spaces or newlines).
     - Parses the text into sections based on patterns like uppercase lines or colons.
   - *CSV Files*:  
     - Uses `csv.DictReader` to convert rows of a CSV file into dictionaries.
   - *XML Files*:  
     - Processes XML using the `xml.etree.ElementTree` library.
     - Recursively parses XML elements and attributes.
   - *EML Files*:  
     - Extracts metadata like sender, subject, and recipients using the `email` library.

2. **Text Cleaning**:
   - Removes excessive newlines, blank spaces, and unnecessary whitespace to standardize content.

3. **Pattern-Based Parsing**:
   - Identifies section headers in PDF/DOCX content based on specific patterns:
     - Lines ending with a colon (`:`).
     - Lines that are entirely uppercase.
   - Splits text into bullet points by identifying bullet characters like `•`, `-`, and `*`.

4. **Data Transformation**:
   - Converts parsed and cleaned content into a structured JSON format.
   - Creates dictionaries where:
     - Keys are section titles (e.g., headings).
     - Values are lists of bullet points or textual content.

5. **Output Saving**:
   - Processes the data and saves the results into JSON files using `json.dump()`.

---

- **`server.js`**: This file runs the local server for serving the front-end files (HTML, CSS, JS) and manages the communication between the front-end and the back-end.
            The provided code integrates multiple components, but the **main algorithm** utilized here revolves around **text generation** and **pattern matching**:

### 1. **Algorithm Used**:
- Google Generative AI - Gemini (gemini-1.5-flash): This model is used to process and generate natural language responses for user queries when no specific result is retrieved.
   - Task: Text generation and understanding.
   - Implementation: 
     - `genAI.getGenerativeModel()` retrieves the AI model.
     - The chat session with `model.startChat()` allows generating responses dynamically based on user input.
     - It processes prompts, formats output, and ensures user-friendly responses.

- Regular Expression (Regex):
   - Used to extract specific user inputs like patient names in requests.
   - Regex Example:
     ```javascript
     const match = userMessage.match(/show me ([^'’]+)['’]s test result/i);
     ```
     - This identifies and extracts text patterns like *"Show me Bobby Jackson's test result"*.

- Search Algorithm:
   - Linear Search (used with the `.find()` method):
     ```javascript
     const patient = patients.find(p => p.Name.toLowerCase() === patientName.toLowerCase());
     ```
     - This performs a case-insensitive linear search through the `patients` array to match the patient name.

---

### 2. **Supporting Components**:
- **Static File Serving**: For JSON and frontend resources using `express.static`.
- **Data Parsing**: JSON file reading and extraction of patient details using `fs` (File System).
- **Response Formatting**: Clean and structured output using string templates for improved readability.
- CORS and Middleware: To enable cross-origin requests and parse incoming JSON data.

---


- **`uploads/`**: Contains all the raw, unstructured files (e.g., PDFs, CSVs, XLSX) that need to be processed by the system.

- **`static/`**: Contains static resources like CSS, JS, and image files for the front-end interface.

- **`processed_files/`**: Stores the JSON files that are the result of the data processing.
- **`p`**

## Contributing

Feel free to fork the repository, make changes, and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

### Key sections explained:

1. **Project Structure**: Lists the files and folders in your project to help users understand the organization.
2. **Features**: Describes the main features of the system, such as data conversion, audio/video handling, front-end interface, etc.
3. **How to Run**: Provides instructions to install dependencies and run the application on a local server.
4. **Files Description**: Gives a detailed explanation of each file in the project and its role.




