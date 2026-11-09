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
# SECURITY SYSTEM
# ------------------------------------------------------------------
SECRET_PASSWORD = "AjmalSecure2026"

if "authenticated" not in strt.session_state:
    strt.session_state.authenticated = False

def check_password():
    if strt.session_state["password_input"] == SECRET_PASSWORD:
        strt.session_state.authenticated = True
        del strt.session_state["password_input"]
    else:
        strt.error("❌ Incorrect Password. Please try again.")

if not strt.session_state.authenticated:
    strt.set_page_config(page_title="Security Lock", page_icon="🔒", layout="centered")
    strt.title("🔒 Security Access Required")
    strt.write("This custom real estate AI application is locked. Please enter the access key below.")
    strt.text_input("Enter App Password", type="password", key="password_input", on_change=check_password)
    strt.stop()

# ------------------------------------------------------------------
# MAIN REAL ESTATE CHAT APPLICATION
# ------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a friendly, highly professional AI Assistant for 'Apex Realty Group'. 
Your primary goal is to engage website visitors, answer basic real estate questions, and capture client leads.

Our Main Services:
- Residential Home Buying & Selling
- Free Commercial Property Appraisals
- Virtual & In-Person Home Viewings

Follow these strict rules:
1. Be exceptionally polite, professional, and helpful.
2. If the user wants to buy, sell, or view a property, ask for their Full Name, Email, and what type of home they are looking for (Budget/Bedrooms).
3. Once they give you those details, say exactly: "[LEAD_CAPTURED] Thank you! A licensed agent from Apex Realty will reach out to you shortly."
"""

strt.set_page_config(page_title="Apex Realty AI Receptionist", page_icon="🏡", layout="centered")
strt.title("🏡 Premier Real Estate AI Receptionist")
strt.write("Welcome! Looking to buy, sell, or rent? Chat with our 24/7 AI virtual agent below.")

if "messages" not in strt.session_state:
    strt.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in strt.session_state.messages:
    if msg["role"] != "system":
        with strt.chat_message(msg["role"]):
            strt.write(msg["content"])

if user_input := strt.chat_input("Ask about listings, buying, or selling..."):
    with strt.chat_message("user"):
        strt.write(user_input)
    strt.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=strt.session_state.messages,
            temperature=0.7,
            max_tokens=100
        )
        bot_reply = response.choices[0].message.content

        with strt.chat_message("assistant"):
            strt.write(bot_reply)
        strt.session_state.messages.append({"role": "assistant", "content": bot_reply})

        if "[LEAD_CAPTURED]" in bot_reply:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("leads.txt", "a", encoding="utf-8") as file:
                file.write(f"--- NEW REAL ESTATE LEAD ({current_time}) ---\n")
                file.write(f"User: {user_input}\n")
                file.write(f"Bot: {bot_reply}\n\n")
            strt.success("📝 Real estate lead logged securely to your dashboard file!")

    except Exception as e:
        strt.error(f"System Error: {e}")
# HIDE STREAMLIT BRANDING AND BUTTONS
HIDE_STYLE = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
strt.markdown(HIDE_STYLE, unsafe_allow_html=True)
