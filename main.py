import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread

# --- STEP 1: UPTIME SERVER (For Render) ---
app = Flask('')

@app.route('/')
def home():
    return "Sentinel-X UserBot is Live and Running!"

def run_server():
    # Render ke port par server chalu karega
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# --- STEP 2: BOT CONFIGURATION ---
# Ye saari values hum Render ke dashboard par bharenge
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
STRING_SESSION = os.environ.get('STRING_SESSION', '').strip().replace(" ", "")
SOURCE_ID = int(os.environ.get('SOURCE_ID', 0))
DEST_ID = int(os.environ.get('DEST_ID', 0))

# UserBot Client initialization
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# --- STEP 3: FORWARDING LOGIC ---
@client.on(events.NewMessage(chats=SOURCE_ID))
async def forward_handler(event):
    try:
        # Bina download kiye direct server-to-server forward
        await client.forward_messages(DEST_ID, event.message)
        print(f"✅ Forwarded Message ID: {event.message.id}")
    except Exception as e:
        print(f"❌ Forwarding Error: {e}")

# --- STEP 4: EXECUTION ---
if __name__ == "__main__":
    if not STRING_SESSION or not API_ID:
        print("🚨 ERROR: Environment Variables (API_ID/SESSION) missing!")
    else:
        # Flask ko alag thread mein chalana zaruri hai
        Thread(target=run_server).start()
        print("🚀 Sentinel-X Starting...")
        
        with client:
            client.run_until_disconnected()
