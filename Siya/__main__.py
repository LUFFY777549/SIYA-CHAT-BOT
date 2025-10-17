import asyncio
import importlib
import os
import sys
from pathlib import Path

# ------------------ Add Siya.Modules to sys.path ------------------ #
MODULES_DIR = Path(__file__).parent / "Siya" / "Modules"
if MODULES_DIR.exists():
    sys.path.append(str(MODULES_DIR))
else:
    raise FileNotFoundError("Siya.Modules folder not found!")

# ------------------ Async module loader ------------------ #
async def load_modules():
    for file in MODULES_DIR.glob("*.py"):
        if file.name.startswith("__"):
            continue
        module_name = file.stem
        try:
            importlib.import_module(module_name)
            print(f"[✅] Loaded module: {module_name}")
        except Exception as e:
            print(f"[❌] Failed to load module {module_name}: {e}")

# ------------------ Bot main function ------------------ #
async def main():
    print("🚀 Siya Chat Bot starting...")
    await load_modules()
    print("🌟 All modules loaded successfully!")
    print("🤖 Bot is now running...")

    # Keep bot running
    while True:
        await asyncio.sleep(3600)

# ------------------ Entry point ------------------ #
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")