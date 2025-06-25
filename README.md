# Flask & LangChain AI Chatbot with Firestore Memory

  <!-- **IMPORTANT**: Replace this with a real screenshot of your app! -->

A responsive, web-based AI chatbot built with a Python Flask backend and a vanilla JavaScript frontend. This project uses **LangChain** and **OpenAI** for intelligent, context-aware responses and **Google Firestore** for persistent chat history, allowing conversations to be remembered across sessions.

## ✨ Features

-   **Interactive Web Interface**: A clean, modern chat interface built with Flask, HTML, CSS, and JavaScript.
-   **Persistent Memory**: Conversations are saved to Google Firestore, so the chatbot remembers previous interactions even after you close the browser.
-   **Context-Aware Responses**: Leverages LangChain's `ChatPromptTemplate` and `MessagesPlaceholder` to provide the full conversation history to the OpenAI model for richer, more relevant answers.
-   **Configurable AI Persona**: Easily change the AI's expertise (e.g., "customer service expert," "python programming expert") in one line of code.
-   **Asynchronous Communication**: The frontend communicates with the backend without page reloads using the Fetch API.
-   **Clear Chat History**: A dedicated button to easily clear the conversation history from the database.
-   **Easy to Set Up**: Requires minimal configuration with a `.env` file for API keys and a Firebase service account key.

## 🛠️ Tech Stack

-   **Backend**:
    -   [Flask](https://flask.palletsprojects.com/): A lightweight WSGI web application framework in Python.
    -   [LangChain](https://python.langchain.com/): A framework for developing applications powered by language models.
    -   [OpenAI API](https://platform.openai.com/): Used for generating chat completions.
    -   [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup): For server-side communication with Google Firestore.
-   **Frontend**:
    -   HTML5
    -   CSS3
    -   Vanilla JavaScript (ES6+)
-   **Database**:
    -   [Google Cloud Firestore](https://firebase.google.com/docs/firestore): A NoSQL document database for storing chat history.

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

-   Python 3.8+
-   An [OpenAI API Key](https://platform.openai.com/api-keys).
-   A [Google Cloud / Firebase Project](https://console.firebase.google.com/) with Firestore Database enabled.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/sadiakhalil125/AIChatbot.git
    cd AIChatbot
    ```

2.  **Create a virtual environment and activate it:**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up Firebase Credentials:**
    -   In your Firebase project console, go to **Project Settings** > **Service accounts**.
    -   Click **"Generate new private key"** and download the JSON file.
    -   Rename the downloaded file to `firebase_key.json` and place it in the root directory of this project.

5.  **Set up OpenAI API Key:**
    -   Create a file named `.env` in the root directory.
    -   Add your OpenAI API key to this file:
      ```env
      OPENAI_API_KEY="sk-your-real-api-key-here"
      ```

6.  **Run the Flask application:**
    ```sh
    python app.py
    ```

7.  **Open your browser:**
    Navigate to `http://127.0.0.1:5001` to start chatting!


## Project Visuals

![Screenshot (1132)](https://github.com/user-attachments/assets/cb8bfd90-11f3-4af5-b6ba-9a7de5c06b24)

![Screenshot (1133)](https://github.com/user-attachments/assets/2168bef6-3d12-41e1-9440-330b2ced5950)

![Screenshot (1134)](https://github.com/user-attachments/assets/445f1e4f-4c6d-4072-86cb-9bc3bd80ee05)


## 📂 Project Structure

```
/chat_project
|-- chatbot_server.py                 # Main Flask application, routes, and logic
|-- firebase_key.json      # Your Firebase service account credentials (gitignored)
|-- .env                   # Environment variables for API keys (gitignored)
|-- requirements.txt       # Python dependencies
|
|-- /templates/
|   |-- index.html         # The single HTML file for the frontend (UI, CSS, JS)
|
|-- .gitignore             # To exclude sensitive files and virtual env from git
```

## ⚙️ How It Works

1.  **User Interface**: The user interacts with the chat interface in `templates/index.html`.
2.  **Send Message**: When the user sends a message, JavaScript sends a `POST` request to the `/chat` endpoint on the Flask server.
3.  **Backend Processing**:
    -   The `chat()` function in `app.py` receives the message.
    -   It calls `get_chat_history()` to pull the entire conversation history from Firestore.
    -   LangChain's `ChatPromptTemplate` assembles a complete prompt, including the system message, the past conversation, and the new user query.
    -   The prompt is sent to the OpenAI model.
4.  **Save to Database**: The user's message and the AI's response are both saved as new documents in the Firestore `chat_history` collection with a server timestamp.
5.  **Return Response**: The AI's response is sent back to the frontend as a JSON object.
6.  **Display Response**: The JavaScript on the frontend receives the response and dynamically adds the AI's message to the chat window.
