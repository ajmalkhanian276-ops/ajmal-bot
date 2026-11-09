import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# Load your secret free AI key from the .env file
load_dotenv()

# Initialize the free Groq AI client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Rebranded with your real name: Ajmal
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

def chat_session():
    print("🚀 Ajmal's Business AI Chatbot is live! (Type 'quit' to exit)\n")
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Chatbot: Goodbye!")
            break
            
        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            # Let the free AI brain think and reply
            response = client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=messages,
                temperature=0.7,
                max_tokens=100
            )
            
            # FIXED LINE: Added [0] so it extracts the text correctly from the list
            bot_reply = response.choices[0].message.content
            print(f"\nBot: {bot_reply}\n")

            if "[LEAD_CAPTURED]" in bot_reply:
                print("✨ SYSTEM ALERT: New business lead secured! ✨\n")
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open("leads.txt", "a", encoding="utf-8") as file:
                    file.write(f"--- NEW LEAD SECURED ({current_time}) ---\n")
                    file.write(f"User Message: {user_input}\n")
                    file.write(f"Bot Reply: {bot_reply}\n\n")
                print("📝 Lead safely saved with timestamp to 'leads.txt' inside your folder!\n")

            messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    chat_session()
