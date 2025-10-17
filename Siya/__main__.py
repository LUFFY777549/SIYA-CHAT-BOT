import asyncio
import importlib
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ------------------ Load .env ------------------ #
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")      # Optional if using PTB BotToken only
API_HASH = os.getenv("API_HASH")  # Optional if using PTB BotToken only

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

# ------------------ Add Siya.Modules to sys.path ------------------ #
MODULES_DIR = Path(__file__).parent / "Siya" / "Modules"
if MODULES_DIR.exists():
    sys.path.append(str(MODULES_DIR))
else:
    raise FileNotFoundError("Siya.Modules folder not found!")

# ------------------ Create PTB Application ------------------ #
app = Application.builder().token(BOT_TOKEN).build()

# ------------------ Async module loader ------------------ #
async def load_modules(application):
    for file in MODULES_DIR.glob("*.py"):
        if file.name.startswith("__"):
            continue
        module_name = file.stem
        try:
            mod = importlib.import_module(f"Siya.Modules.{module_name}")
            # If module has `init` function, pass application
            if hasattr(mod, "init"):
                await mod.init(application)
            print(f"[✅] Loaded module: {module_name}")
        except Exception as e:
            print(f"[❌] Failed to load module {module_name}: {e}")

# ------------------ Main Bot Function ------------------ #
async def main():
    print("🚀 Siya Chat Bot starting...")
    await load_modules(app)
    print("🌟 All modules loaded successfully!")
    print("🤖 Bot is now running...")
    await app.start()
    await app.updater.start_polling()  # PTB 21+ polling
    await app.updater.idle()

# ------------------ Entry Point ------------------ #
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")