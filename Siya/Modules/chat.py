from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from datetime import datetime, timedelta
import asyncio
import aiohttp

# ------------------ Constants ------------------ #
OWNER_USERNAME = "@Uzumaki_X_Naruto_6"
API_KEY = "AIzaSyA7Cd9CtgNsWr1Si9wV16vKcWFKUGzfP-c"

# Track last activity per user (for limits)
user_last_reply = {}
GROUP_REPLY_INTERVAL = 3 * 60 * 60  # 3 hours
PRIVATE_REPLY_INTERVAL = 30  # 30 seconds per user limit for spam

# Time-based greetings
def get_time_greeting():
    now = datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        return "Good Morning 🌅"
    elif 12 <= hour < 17:
        return "Good Afternoon ☀️"
    elif 17 <= hour < 21:
        return "Good Evening 🌇"
    else:
        return "Hello 🌙"

# ------------------ AI Reply Function ------------------ #
async def get_ai_reply(message: str) -> str:
    url = f"https://api.openai.com/v1/engines/text-davinci-003/completions"  # example
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "prompt": message,
        "max_tokens": 100,
        "temperature": 0.7,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                res = await resp.json()
                return res.get("choices", [{}])[0].get("text", "Hmm 🤔")
    except:
        return "Sorry, I couldn't process that 😅"

# ------------------ Message Handler ------------------ #
async def chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    text = update.message.text

    # Owner-related questions
    owner_keywords = ["owner", "malik", "husband", "bf"]
    if any(word in text.lower() for word in owner_keywords):
        await update.message.reply_text(f"My owner is {OWNER_USERNAME} 😉")
        return

    # Time-based greetings
    greetings_keywords = ["good morning", "good afternoon", "good evening", "hello", "hi", "hey"]
    if any(word in text.lower() for word in greetings_keywords):
        greeting = get_time_greeting()
        await update.message.reply_text(f"{greeting} {user.first_name}!")
        return

    # Limit user replies (private)
    now = datetime.now()
    last_time = user_last_reply.get(user.id, datetime.min)
    interval = PRIVATE_REPLY_INTERVAL if chat.type == "private" else GROUP_REPLY_INTERVAL
    if (now - last_time).total_seconds() < interval:
        return  # skip reply to avoid spam

    user_last_reply[user.id] = now

    # Private chat -> reply AI
    if chat.type == "private":
        reply = await get_ai_reply(text)
        await update.message.reply_text(reply)

    # Group chat -> only reply if mentioned
    elif chat.type in ["group", "supergroup"]:
        if f"@{context.bot.username}" in text or update.message.reply_to_message:
            reply = await get_ai_reply(text)
            await update.message.reply_text(reply)

# ------------------ REGISTER FUNCTION ------------------ #
def register(app):
    # Listen to all messages in private & group
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message))