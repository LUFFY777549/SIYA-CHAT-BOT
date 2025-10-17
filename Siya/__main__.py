import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application
from Siya.Modules import start, chat  

# ------------------ Load .env ------------------ #
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")      # Optional
API_HASH = os.getenv("API_HASH")  # Optional

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

# ------------------ Logging ------------------ #
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    # ✅ Single Application instance
    application = Application.builder().token(BOT_TOKEN).build()

    # Register start module
    start.register(application)
    chat.register(application)

    print("🚀 Siya Chat Bot Started!")

    # ✅ 21.4 style synchronous polling
    application.run_polling()

if __name__ == "__main__":
    main()