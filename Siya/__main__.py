import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from telegram.ext import Application

# ------------------ Load .env ------------------ #
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")      # Optional
API_HASH = os.getenv("API_HASH")  # Optional

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

# ------------------ PTB Application ------------------ #
app = Application.builder().token(BOT_TOKEN).build()

# ------------------ Manual Module Imports ------------------ #
# ✅ Yahan manually modules import karo
from Siya.Modules import start  # Sirf start.py

# Agar module me init(application) function hai, call karo
async def init_modules():
    if hasattr(start, "init"):
        await start.init(app)
    print("[✅] start.py module loaded successfully!")

# ------------------ Main Function ------------------ #
async def main():
    print("🚀 Siya Chat Bot starting...")
    await init_modules()
    print("🌟 All manual modules loaded!")
    print("🤖 Bot is now running...")
    
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# ------------------ Entry Point ------------------ #
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")