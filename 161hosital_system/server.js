// Import required modules
const express = require('express'); // Import Express framework for building web applications
const fs = require('fs'); // File system module to interact with the file system
const path = require('path'); // Path module for working with file and directory paths
const cors = require('cors'); // Import CORS to handle Cross-Origin Resource Sharing
const bodyParser = require('body-parser'); // Middleware for parsing incoming request bodies
const { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } = require("@google/generative-ai"); 
// Import Google Generative AI-related modules

const app = express(); // Initialize Express application
const PORT = 3000; // Define the port number for the server

// Middleware
app.use(cors()); // Enable CORS for cross-origin requests
app.use(express.json()); // Built-in middleware to parse incoming JSON requests
app.use(bodyParser.json()); // Middleware to parse JSON requests, useful for specific routes like OTP handling

// API Key and Google Generative AI initialization
const apiKey = "AIzaSyCM79G6eSM8u5fTjDRNrD399zPCKerdZp0"; // Replace this with your actual API key
const genAI = new GoogleGenerativeAI(apiKey); // Initialize Google Generative AI with the API key

// Additional routes, error handling, and server logic can be added below


// Define and retrieve a generative model from Google Generative AI
const model = genAI.getGenerativeModel({
  model: "gemini-1.5-flash",      // Specify the model to use. "gemini-1.5-flash" is likely a predefined version optimized for specific tasks.
  systemInstruction: "You are **smart_toy**, a highly advanced and friendly AI assistant specializing in healthcare and medical data management. Your primary role is to assist users by providing accurate, well-structured, and easily comprehensible information from healthcare datasets. You excel at retrieving and presenting patient data or test results from specific files and folders when requested, ensuring responses are user-friendly and detailed. \n\n### Key Features of smart_toy:\n- **Medical Expertise Only**: Handle queries strictly related to healthcare and medical data. Politely inform users to ask only medical-related queries for non-medical requests.\n- **Accurate Data Retrieval**: When asked, locate and display specific patient information from designated files. For example, if the user asks, “Show me Bobby Jackson’s test result,” search for “Bobby Jackson” in the **`processed_files/healthcare_prediction_dataset.json`** file and present the information in a clear, readable format.\n- **Readable Output**: Structure responses with proper formatting for readability. Ensure fields like name, age, medical condition, test results, etc., are displayed in a user-friendly table or bullet-point format.\n\n#### Example Interaction:\n\n**User**: Show me Bobby Jackson’s test result  \n**smart_toy**: \n```plaintext\nHere is the test result for Bobby Jackson:\n- **Name**: Bobby Jackson\n- **Age**: 45\n- **Gender**: Male\n- **Blood Type**: O+\n- **Medical Condition**: Diabetes\n- **Date of Admission**: 2024-02-15\n- **Doctor**: Dr. Susan Taylor\n- **Hospital**: Hope Medical Center\n- **Insurance Provider**: CareFirst\n- **Billing Amount**: $12,540\n- **Room Number**: 102\n- **Admission Type**: Regular\n- **Discharge Date**: 2024-02-20\n- **Medication**: Metformin\n- **Test Results**: Blood sugar levels normal.\n```\n\n**User**: What's the weather today?  \n**smart_toy**: \"I specialize in healthcare-related queries. Please ask only medical or healthcare-related questions.\"\n\n**User**: Tell me a joke.  \n**smart_toy**: \"I’m here to assist with medical queries only. Please ask a healthcare-related question.\"\n\n### General Guidelines for Responses:\n1. **Clarity**: Avoid technical jargon unless necessary. Provide simple, concise explanations.\n2. **Empathy**: Respond to users with understanding and professionalism.\n3. **Request Clarifications**: If insufficient context is provided, politely ask for more details.\n4. **Focus**: Handle healthcare and dataset-related queries exclusively. For unrelated queries, politely state: \"I specialize in healthcare-related queries. Please ask only medical or healthcare-related questions.\"\n5. **Fallback**: If data is missing or cannot be retrieved, respond with: \"I’m sorry, I could not find the specific information for your request. Please check the data file or consult the relevant medical provider.\"\n\nsmart_toy is here to ensure healthcare information is accessible, understandable, and helpful to users, maintaining a professional and approachable tone at all times.",
});


// Configuration for text generation
const generationConfig = {
    temperature: 1, // Controls randomness in output. Higher values generate more random responses.
    topP: 0.95, // Nucleus sampling parameter. Limits sampling to the top 95% of probability mass.
    topK: 40, // Limits sampling to the top 40 tokens with the highest probabilities.
    maxOutputTokens: 8192, // Maximum number of tokens allowed in the response.
    responseMimeType: "text/plain", // Specifies the MIME type of the response (plain text).
  };

// Serve JSON files from the 'processed_files' directory
app.use('/processed_files', express.static(path.join(__dirname, 'processed_files')));

// Serve static files (CSS, JS, images) from the 'templates' folder
app.use(express.static(path.join(__dirname, 'templates')));

// Secure API Key Route
// Endpoint to handle "Show me <name>'s test result" queries
app.post('/chat', async (req, res) => {
    try {
        const userMessage = req.body.message;   // Retrieve user message from request body
        
        // Extract patient name using regex
        const match = userMessage.match(/show me ([^']+)['’]s test result/i);
        if (match) {
            const patientName = match[1].trim();  // Extract and trim the patient name
            console.log(`Extracted patient name: ${patientName}`);

            const filePath = path.join(__dirname, 'processed_files', 'healthcare_prediction_dataset.json');

            // Read JSON file asynchronously
            const fileData = await fs.promises.readFile(filePath, 'utf8');
            const patients = JSON.parse(fileData);

            // Find the patient by name (case-insensitive match)
            const patient = patients.find(p => p.Name.toLowerCase() === patientName.toLowerCase());
            if (patient) {
                // Format response with patient data
                const responseText = `
Here is the test result for ${patient.Name}:
- Name: ${patient.Name}
- Age: ${patient.Age}
- Gender: ${patient.Gender}
- Blood Type: ${patient['Blood Type']}
- Medical Condition: ${patient['Medical Condition']}
- Date of Admission: ${patient['Date of Admission']}
- Doctor: ${patient.Doctor}
- Hospital: ${patient.Hospital}
- Insurance Provider: ${patient['Insurance Provider']}
- Billing Amount: $${parseFloat(patient['Billing Amount']).toFixed(2)}
- Room Number: ${patient['Room Number']}
- Admission Type: ${patient['Admission Type']}
- Discharge Date: ${patient['Discharge Date']}
- Medication: ${patient.Medication}
- Test Results: ${patient['Test Results']}
                `;
                console.log("Patient found. Sending response.");
                return res.json({ response: responseText.trim() }); // Send formatted response
            } else {
                console.log(`Patient ${patientName} not found.`);
                return res.json({ response: `I’m sorry, I could not find the specific information for ${patientName}. Please check the data file or consult the relevant medical provider.` });
            }
        }

        // Fallback for non-test result queries
        console.log("No test result request detected. Forwarding to Gemini model.");
        const chatSession = model.startChat({
            generationConfig,    // Use the generation configuration defined earlier
            history: [], // Use an empty array if no previous history is required
        });
        

        const result = await chatSession.sendMessage(userMessage);   // Send user message to the chat model
        return res.json({ response: result.response.text() });     // Send the model's response back to the client
    } catch (error) {
        console.error("Error in /chat endpoint:", error.message);
        return res.status(500).send({ error: "An internal error occurred. Please try again." });
    }
});

//Response Formatting:
const someObject = { first_key: 'value1', second_key: 'value2' }; // Initialize someObject first       Response Formatting Example:    Example object to format keys

for (const key in someObject) {
    const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
    console.log(formattedKey); // Outputs: "First Key", "Second Key"
}


// Route to serve the HTML file for the chatbot
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'templates', 'index.html'));  // Serve the chatbot's HTML interface
});

// Endpoint to list all JSON files in the `processed_files` folder
app.get('/getFiles', (req, res) => {
    const directoryPath = path.join(__dirname, 'processed_files');  // Path to the directory
    fs.readdir(directoryPath, (err, files) => {
        if (err) {
            console.error('Unable to scan directory:', err);  // Log directory scanning error
            return res.status(500).send('Error reading directory');    // Respond with an error
        }
        const jsonFiles = files.filter(file => file.endsWith('.json'));   // Filter JSON files
        res.json(jsonFiles);     // Send list of JSON files as a response
    });
});

// Endpoint to get content from a specific JSON file
app.get('/getFileContent/:filename', (req, res) => {
    const filePath = path.join(__dirname, 'processed_files', req.params.filename);   // Construct file path

    // Check if the file exists
    if (!fs.existsSync(filePath)) {
        return res.status(404).send('File not found'); // Respond with 404 if file does not exist
    }

    // Read and return the file content
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error(`Error reading file ${req.params.filename}:`, err.message);
            return res.status(500).send('Error reading file');
        }

        try {
            res.json(JSON.parse(data));
        } catch (parseError) {
            console.error(`Error parsing JSON in file ${req.params.filename}:`, parseError.message);
            res.status(500).send(`Error parsing JSON in file ${req.params.filename}`);
        }
    });
});



// Start the server
app.listen(PORT, () => {  
    console.log(`Server is running on http://localhost:${PORT}`);  
});

//Function to Find and Display Test Results:
// Function to find and display test results
async function findTestResults(name) {
    try {
      // Read data from healthcare_prediction_dataset.json
      const data = await fs.promises.readFile(path.join(__dirname, 'processed_files/healthcare_prediction_dataset.json'), 'utf8');
      const jsonData = JSON.parse(data);
  
      // Find patient data by name
      const patientData = jsonData.find(patient => patient.Name.toLowerCase() === name.toLowerCase());
  
      // Check if data found
      if (!patientData) {
        return "I couldn't find any test results for " + name + ". Please check the name or consult the relevant medical provider.";
      }
  
      // Format and return test results
      let response = "Here are the test results for " + name + ":\n";
      for (const key in patientData) {
        if (key !== "name") {
          response += `- ${key}: ${patientData[key]}\n`;
        }
      }
      return response;
    } catch (error) {
      console.error("Error reading file:", error.message);
      return "An error occurred while retrieving test results.";
    }
  }



// Async function to handle the chat session
async function run() {
    // Start a new chat session with specified generation config and optional history
    const chatSession = model.startChat({
        generationConfig, // Configuration for chat response generation, including temperature, max tokens, etc.
        history: previousHistory ? [...previousHistory] : [] // Use previous history if available, otherwise start with an empty array
    });

    // Example of user message retrieval (assuming this comes from the request body in a web API)
    const userMessage = req.body.message; // Assuming message comes from request body

    // Check for specific queries like "show me <name>'s test result"
    if (userMessage.toLowerCase().startsWith("show me ")) {
        // Extract name from the user message using regex
        const match = userMessage.match(/Show me (.+?)’s test result/i); 
        const name = match ? match[1] : null; // If match found, extract name, otherwise null

        // Find test results for the patient using the extracted name
        const results = await findTestResults(name);

        // Send the results to the chat session and log the response
        const response = chatSession.sendMessage(results);
        console.log(response.response.text());
    } else {
        // For other types of queries, forward the message to the model without special handling
        const response = await chatSession.sendMessage(userMessage);
        console.log(response.response.text());
    }
}
