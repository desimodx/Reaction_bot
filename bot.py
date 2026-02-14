import telebot
import os
import random
from flask import Flask
from threading import Thread

# 1. Dummy Flask Server (Render ke liye)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Active!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Bot Logic
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Sabhi reactions jo image me hain:
REACTION_LIST = [
    "❤️", "👍", "👎", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", 
    "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊️", "🤡", 
    "🥱", "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡️", 
    "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", 
    "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", 
    "🤝", "✍️", "🤗", "🫡", "🎅", "🎄", "☃️", "💅", "🤪", "🗿", 
    "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂️", 
    "🤷", "🤷‍♀️", "😡"
]

@bot.channel_post_handler(content_types=['text', 'photo', 'video', 'document', 'audio'])
def auto_react(message):
    try:
        # Random emoji select karna list se
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
    keep_alive()
    print("Bot is starting with all reactions...")
    bot.infinity_polling()
