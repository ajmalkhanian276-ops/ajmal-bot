import os
import streamlit as strt
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ------------------------------------------------------------------
# SECURITY SYSTEM: CREATING YOUR SECRET PASSWORD
# ------------------------------------------------------------------
SECRET_PASSWORD = "AjmalSecure2026"

# Initialize security state memory bank
if "authenticated" not in strt.session_state:
    strt.session_state.authenticated = False

# Function to check if the typed password matches
def check_password():
    if strt.session_state["password_input"] == SECRET_PASSWORD:
        strt.session_state.authenticated = True
        del strt.session_state["password_input"]  # Clear password from memory safely
    else:
        strt.error("❌ Incorrect Password. Please try again.")

# If the user has NOT typed the right password yet, block the screen!
if not strt.session_state.authenticated:
    strt.set_page_config(page_title="Security Lock", page_icon="🔒", layout="centered")
    strt.title("🔒 Security Access Required")
    strt.write("This custom business AI application is locked. Please enter the developer access key below.")
    
    # Text input box for the password (masks characters with dots)
    strt.text_input(
        "Enter App Password", 
        type="password", 
        key="password_input", 
        on_change=check_password
    )
    strt.stop()  # STOPS the rest of the web application code from loading!

# ------------------------------------------------------------------
# MAIN CHAT APPLICATION (Loads ONLY if password is correct)
# ------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a friendly, highly professional AI Assistant for 'Ajmal's Tech Solutions'. 
Your primary goal is to help website visitors, answer questions about our services, and collect customer leads.

Our Services:
- Web Development
- Custom AI Integration
- Workflow Automation

Follow these strict rules:
1. Be polite, concise, and helpful.
2. If the user seems interested in working with Ajmal, ask for their Name, Email, and Project Idea.
3. Once they give you all three details, say exactly: "[LEAD_CAPTURED] Thank you! Ajmal will reach out to you shortly."
"""

# Configure the Streamlit Page Look
strt.set_page_config(page_title="Ajmal's AI Assistant", page_icon="🚀", layout="centered")
strt.title("🚀 Ajmal's Business AI Assistant")
strt.write("Welcome! Chat with my custom AI receptionist below.")

# Initialize conversation memory bank inside the web app
if "messages" not in strt.session_state:
    strt.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display past chat messages beautifully on the web screen
for msg in strt.session_state.messages:
    if msg["role"] != "system":
        with strt.chat_message(msg["role"]):
            strt.write(msg["content"])

# Handle User Input Box
if user_input := strt.chat_input("Type your message here..."):
    # Show user message instantly
    with strt.chat_message("user"):
        strt.write(user_input)
    strt.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Get AI response from Groq
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=strt.session_state.messages,
            temperature=0.7,
            max_tokens=100
        )
        
        # STRUCTURAL FIX ADDED HERE -> [0]
        bot_reply = response.choices[0].message.content

        # Show bot message instantly with an assistant icon
        with strt.chat_message("assistant"):
            strt.write(bot_reply)
        strt.session_state.messages.append({"role": "assistant", "content": bot_reply})

        # Save leads automatically to leads.txt if triggered
        if "[LEAD_CAPTURED]" in bot_reply:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("leads.txt", "a", encoding="utf-8") as file:
                file.write(f"--- NEW WEB LEAD SECURED ({current_time}) ---\n")
                file.write(f"User Message: {user_input}\n")
                file.write(f"Bot Reply: {bot_reply}\n\n")
            strt.success("📝 Lead safely saved to 'leads.txt' inside your folder!")

    except Exception as e:
        strt.error(f"An error occurred: {e}")
