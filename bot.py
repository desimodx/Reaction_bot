import telebot
import os
import random
import time
import requests
from flask import Flask
from threading import Thread

# 1. Dummy Flask Server
app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive and Active!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- SELF PING LOGIC (Bot ko jagaye rakhne ke liye) ---
def self_ping():
    # Yaha apna Render wala URL dalein (e.g. https://my-bot.onrender.com/)
    URL = "https://reaction-bot-r003.onrender.com" 
    while True:
        try:
            requests.get(URL)
            print("Self-ping: Keep-alive signal sent!")
        except:
            print("Self-ping failed, will try again.")
        time.sleep(300) # Har 5 minute mein check karega

# 2. Bot Logic
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

REACTION_LIST = [
    "❤️", "👍", "👎", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", 
    "😢", "🎉", "🤩", "🤮", "🙏", "👌", "🕊️", "🤡", 
    "🥱", "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡️", 
    "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", 
    "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", 
    "🤝", "✍️", "🤗", "🫡", "🎅", "🎄", "☃️", "💅", "🤪", "🗿", 
    "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂️", 
    "🤷", "🤷‍♀️"
]

@bot.channel_post_handler(content_types=['text', 'photo', 'video', 'document', 'audio'])
def auto_react(message):
    try:
        random_emoji = random.choice(REACTION_LIST)
        bot.set_message_reaction(
            message.chat.id, 
            message.message_id, 
            [telebot.types.ReactionTypeEmoji(random_emoji)], 
            is_big=False
        )
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    keep_alive() # Web server chalu karega
    
    # Self-ping start karne ke liye thread
    if "onrender.com" in "APKA_RENDER_URL_YAHA_DALEIN":
        Thread(target=self_ping).start()
        
    print("Bot is starting with Self-Ping enabled...")
    bot.infinity_polling()
            
