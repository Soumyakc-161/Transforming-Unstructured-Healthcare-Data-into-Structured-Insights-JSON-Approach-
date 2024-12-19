//The below script is a chatbot that interacts with the user and fetches data like test results from a JSON file(healthcare_prediction_dataset.json).
//  Below is an explanation of key sections of the code:
// 1. API Configuration
        //API_KEY: Stores the API key used for making requests.
        //API_URL: The URL used for generating content using the Gemini model (though it is not being used in the provided code).
        //PROCESSED_FILES: The list of files (in this case, a single file "healthcare_prediction_dataset.json") that the chatbot interacts with.
// 
// 2. Message Handling:
        //createChatLi: A helper function that creates and returns a chat message list item (li), where the message content is inserted depending on whether it’s an incoming or outgoing message.
        //fetchTestResult: A function that processes a user query to fetch test results from the healthcare_prediction_dataset.json file. It extracts the name from the query and searches the JSON file for a matching record.
        //generateResponse: A function that generates a response based on the user’s message. If the message contains "test result", it fetches the test result. Otherwise, it sends the message to the server for further processing.

// 3.Chatbot UI:
      //handleChat: This function handles the logic of appending user messages to the chatbox and generating a bot response. It creates a new chat item, waits for the response, and displays it.
// Event Listeners:
      //chatInput.addEventListener("input"): Adjusts the height of the textarea based on the input.
      //chatInput.addEventListener("keydown"): If the Enter key is pressed (without Shift key), it triggers the handleChat function.
      //sendChatBtn.addEventListener("click"): Triggers the chat functionality when the send button is clicked.
      //closeBtn.addEventListener("click"): Closes the chatbot when the close button is clicked.
      //chatbotToggler.addEventListener("click"): Toggles the visibility of the chatbot when the chatbot toggle button is clicked.

      
      //-------------------LET'S START WITH CODE ----------------------
// Selecting the necessary DOM elements for toggling and chat functionality
const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight; // Initial height of the input field

// API configuration for the chatbot
const API_KEY = "AIzaSyCM79G6eSM8u5fTjDRNrD399zPCKerdZp0"; // i added my  API key here
const API_URL = `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key=${API_KEY}`;// URL for the API 

const PROCESSED_FILES = ["healthcare_prediction_dataset.json"]; // List of files the chatbot interacts with

// Function to create a new chat message list item
const createChatLi = (message, className) => {
  const chatLi = document.createElement("li"); // Create a new list item for the message
  chatLi.classList.add("chat", `${className}`); // Add the outgoing or incoming class
  let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`; // Set content based on the message type
  chatLi.innerHTML = chatContent; // Set the HTML content
  chatLi.querySelector("p").textContent = message; // Set the message text
  return chatLi;
};

// Function to fetch test results from a JSON file based on the user query
const fetchTestResult = async (query) => {
  const targetFile = "healthcare_prediction_dataset.json"; // The target file to fetch data from

  try {
      const response = await fetch(`/processed_files/${targetFile}`); // Fetch the file
      if (!response.ok) {
          throw new Error(`Unable to fetch the file: ${targetFile}`); // Error handling if file can't be fetched
      }

      const data = await response.json(); // Parse the JSON data

      // Extract the name from the user query using regex
      const nameMatch = query.match(/show me ([a-z\s]+)’?s test result/i);
      const searchName = nameMatch ? nameMatch[1].trim().toLowerCase() : null;

      if (!searchName) {
          return "Invalid query. Please specify a valid name."; // Return an error message if no name is provided
      }

      // Search for the record in the dataset
      const record = data.content.find(person =>
          person.Name?.toLowerCase() === searchName
      );

      if (record) {
          // If a matching record is found, format and return the test results
          return `Here is the test result for ${record.Name}:\n\n` +
              `- Name: ${record.Name}\n` +
              `- Age: ${record.Age}\n` +
              `- Gender: ${record.Gender}\n` +
              `- Blood Type: ${record["Blood Type"]}\n` +
              `- Medical Condition: ${record["Medical Condition"]}\n` +
              `- Date of Admission: ${record["Date of Admission"]}\n` +
              `- Doctor: ${record.Doctor}\n` +
              `- Hospital: ${record.Hospital}\n` +
              `- Insurance Provider: ${record["Insurance Provider"]}\n` +
              `- Billing Amount: $${parseFloat(record["Billing Amount"]).toFixed(2)}\n` +
              `- Room Number: ${record["Room Number"]}\n` +
              `- Admission Type: ${record["Admission Type"]}\n` +
              `- Discharge Date: ${record["Discharge Date"]}\n` +
              `- Medication: ${record.Medication}\n` +
              `- Test Results: ${record["Test Results"]}`;
      } else {
          return `No test result found for ${searchName} in ${targetFile}.`; // If no record is found, return a message
      }
  } catch (error) {
      console.error(`Error reading ${targetFile}: ${error.message}`); // Log any errors
      return `An error occurred while searching for test results in ${targetFile}.`; // Return a user-friendly error message
  }
};

// Function to fetch patient records based on the user query
const fetchPatientRecord = async (query) => {
  const targetFile = "Patient_ID_records.json"; // The target file to fetch data from

  try {
      const response = await fetch(`/processed_files/${targetFile}`); // Fetch the file
      if (!response.ok) {
          throw new Error(`Unable to fetch the file: ${targetFile}`); // Error handling if file can't be fetched
      }

      const data = await response.json(); // Parse the JSON data

      // Extract the name from the user query using regex
      const nameMatch = query.match(/show me ([a-z\s]+)’?s record/i);
      const searchName = nameMatch ? nameMatch[1].trim().toLowerCase() : null;

      if (!searchName) {
          return "Invalid query. Please specify a valid name."; // Return an error message if no name is provided
      }

      // Search for the record in the dataset
      const record = data.content.find(person =>
          person["Patient Name"]?.toLowerCase() === searchName
      );

      if (record) {
          // If a matching record is found, format and return the patient details
          return `Here is the record for ${record["Patient Name"]}:\n\n` +
              `- Patient ID: ${record["Patient ID"]}\n` +
              `- Name: ${record["Patient Name"]}\n` +
              `- Age: ${record.Age}\n` +
              `- Gender: ${record.Gender}\n` +
              `- Diagnosis: ${record.Diagnosis}\n` +
              `- Medications: ${record.Medications}\n` +
              `- Last Visit Date: ${record["Last Visit Date"]}`;
      } else {
          return `No record found for ${searchName} in ${targetFile}.`; // If no record is found, return a message
      }
  } catch (error) {
      console.error(`Error reading ${targetFile}: ${error.message}`); // Log any errors
      return `An error occurred while searching for patient records in ${targetFile}.`; // Return a user-friendly error message
  }
};


// Function to generate a response based on the user input
const generateResponse = async (userMessage) => {
  if (userMessage.toLowerCase().includes("test result")) {
      // If the user is asking for a test result, fetch it from the dataset
      return await fetchTestResult(userMessage);
  } else {
      try {
          // Otherwise, send the message to the server for processing
          const response = await fetch('/chat', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ message: userMessage })
          });
          const data = await response.json(); // Parse the server response
          return data.response || 'Error generating response'; // Return the server's response or an error message
      } catch (error) {
          console.error(`Error fetching response: ${error.message}`); // Log any errors
          return `An error occurred: ${error.message}`; // Return a user-friendly error message
      }
  }
};

// Function to handle the chat when the user submits a message
const handleChat = async () => {
    userMessage = chatInput.value.trim(); // Get the user's message
    if (!userMessage) return; // If the message is empty, do nothing
  
    chatInput.value = ""; // Clear the input field
    chatInput.style.height = `${inputInitHeight}px`; // Reset the input field height
  
    // Add the outgoing message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight); // Scroll to the bottom of the chatbox
  
    // Show a "thinking" message while waiting for the bot's response
    const incomingChatLi = createChatLi("Thinking...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight); // Scroll to the bottom of the chatbox
  
    try {
      // Generate a response from the chatbot
      const botResponse = await generateResponse(userMessage);
      incomingChatLi.querySelector("p").textContent = botResponse; // Display the response in the chatbox
    } catch (error) {
      incomingChatLi.querySelector("p").textContent = "Error processing your message."; // Display an error if the bot fails
      console.error("Error generating response:", error); // Log any errors
    }
};

// Adjust the height of the input field as the user types
chatInput.addEventListener("input", () => {
  chatInput.style.height = `${inputInitHeight}px`; // Reset the height
  chatInput.style.height = `${chatInput.scrollHeight}px`; // Adjust the height to fit the content
});

// Listen for the Enter key press (without Shift key) to send the message
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault(); // Prevent the default behavior (new line in the input field)
    handleChat(); // Handle the chat
  }
});

// Listen for the send button click to send the message
sendChatBtn.addEventListener("click", handleChat);

// Close the chatbot when the close button is clicked
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));

// Toggle the visibility of the chatbot when the toggle button is clicked
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));



