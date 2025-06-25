import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, jsonify

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# --- INITIALIZATION ---

# Load .env vars
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Initialize Firebase
# NOTE: This part can cause issues if re-initialized (e.g., in a debug environment).
# We add a check to prevent this.
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
collection = db.collection("chat_history")

# LangChain setup
chat_template = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful {domain} expert.'),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', '{query}')
])
model = ChatOpenAI()

# --- HELPER FUNCTIONS (Adapted from your script) ---

def get_chat_history():
    """Fetches chat history from Firestore and converts to LangChain message objects."""
    docs = collection.order_by("timestamp").stream()
    history = []
    for doc in docs:
        msg = doc.to_dict()
        if msg.get("sender") == "user":
            history.append(HumanMessage(content=msg.get("content", "")))
        elif msg.get("sender") == "bot":
            history.append(AIMessage(content=msg.get("content", "")))
    return history

def save_message(sender, content):
    """Saves a message to the Firestore collection."""
    collection.add({
        "sender": sender,
        "content": content,
        "timestamp": firestore.SERVER_TIMESTAMP
    })


# --- HELPER FUNCTIONS ---
# ... (keep the other functions) ...

# (This is the function to replace)
def clear_chat_history():
    """
    Deletes all documents in the chat_history collection using a batch process.
    This is more efficient and robust than deleting one by one.
    """
    docs = collection.stream()
    
    # Firestore batches have a limit of 500 operations.
    # If you expect more, you'll need a more complex loop.
    # For a typical chatbot, this is usually sufficient.
    batch = db.batch()
    deleted_count = 0
    
    for doc in docs:
        batch.delete(doc.reference)
        deleted_count += 1

    if deleted_count > 0:
        batch.commit()
        print(f"Deleted {deleted_count} documents from chat_history.")
    else:
        print("No documents to delete in chat_history.")

# ... (keep the rest of the file the same) ...
# --- FLASK ROUTES ---

@app.route("/")
def index():
    """Render the main chat page with history."""
    # We get the history in LangChain format and convert it to a simpler dict
    # for rendering in the template.
    chat_history_messages = get_chat_history()
    display_history = []
    for msg in chat_history_messages:
        if isinstance(msg, HumanMessage):
            display_history.append({"sender": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            display_history.append({"sender": "bot", "content": msg.content})
            
    return render_template("index.html", history=display_history)

@app.route("/chat", methods=["POST"])
def chat():
    """Handle the chat interaction."""
    try:
        user_input = request.json["message"]
        
        # 1. Fetch history from Firebase
        chat_history = get_chat_history()
        
        # 2. Build prompt
        prompt = chat_template.invoke({
            "domain": "customer service", # Example domain
            "chat_history": chat_history,
            "query": user_input 
        })
        
        # 3. Get response from OpenAI
        response = model.invoke(prompt)
        bot_response = response.content
        
        # 4. Save both messages to Firebase
        save_message("user", user_input)
        save_message("bot", bot_response)
        
        # 5. Return bot's response
        return jsonify({"response": bot_response})
        
    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({"error": "An error occurred."}), 500

@app.route("/clear", methods=["POST"])
def clear_chat():
    """Clear the chat history in Firestore."""
    try:
        clear_chat_history()
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Error clearing chat: {e}")
        return jsonify({"error": "Failed to clear chat."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)