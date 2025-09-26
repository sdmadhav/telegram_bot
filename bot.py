from telethon import TelegramClient, events, Button
from flask import Flask
from threading import Thread
import asyncio

# === Telegram API credentials ===
api_id = 14300604
api_hash = "c564cb7dc56a5110750727f97e5efc51"
bot_token = "7644736999:AAHc3zRNPy6EG0IJBX7OxsSI9dVk-4Lg2XE"


# === Initialize Telethon client ===
client = TelegramClient('quiz_bot.session', api_id, api_hash).start(bot_token=bot_token)

# === Flask app to keep alive ===
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# === Bot handlers ===
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply('Welcome to the Quiz bot! Use /quiz to start.')

@client.on(events.NewMessage(pattern='/quiz'))
async def start_quiz(event):
    question = "What is the capital of France?"
    options = ["London", "Paris", "Berlin", "Rome"]
    keyboard = [[Button.inline(option, data=option)] for option in options]
    await event.respond(question, buttons=keyboard)

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data == "Paris":
        await event.answer("✅ Correct!")
    else:
        await event.answer("❌ Incorrect!")

# === Intro message when bot starts ===
async def main():
    INTRO_MESSAGE = """
🥂 **Hello AFC'ians!** 🥂

Hamari community bohot hi diverse hai – alag-alag states, languages, aur tastes ke saath! 

Aapki preferences samajhne ke liye hum kuch quick polls share karenge. Yeh humein help karega:
✨ Best movies upload karne mein  
✨ Aapki preferred languages choose karne mein  
✨ Aapke taste ko samajhne mein  

Har poll sirf ek second lega! 🍿  
Starting with our first poll below 👇 👇
"""
    options = ["Let's start! 🚀", "Skip to next poll ➡️", "End polls ❌"]
    keyboard = [[Button.inline(option, data=option)] for option in options]
    await client.send_message(
        'aish_madhav',
        INTRO_MESSAGE,
        file="C:\\Users\\2019c\\Downloads\\Telegram Desktop\\photo_2025-06-26_20-46-17.jpg",
        buttons=keyboard
    )

# === Start ===
keep_alive()  # Start Flask keep-alive server

with client:
    # client.loop.run_until_complete(main())
    client.run_until_disconnected()
