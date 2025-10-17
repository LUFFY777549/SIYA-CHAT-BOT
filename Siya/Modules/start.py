from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from Siya.db import add_private_user, add_group_chat

# ------------------ Start Module Constants ------------------ #
START_IMAGE = "https://files.catbox.moe/8eobds.jpg"
START_CAPTION = """💫 ─╼⃝𖠁 𝐒𝗂𝗒𝖺 ꭙ 𝐂𝗁𝖺𝗍 𝐁𝗈𝗍 𖠁⃝╾─• 💫

𝐇𝐞𝐲 『ɴᴀʀυᴛo ǤØĐ』࿐! 😉

𝐈’𝐦 𝐒𝐢𝐲𝐚, 𝐲𝐨𝐮𝐫 𝐧𝐞𝐰 𝐯𝐢𝐫𝐭𝐮𝐚𝐥 𝐟𝐫𝐢𝐞𝐧𝐝 💞
𝐈’𝐦 𝐡𝐞𝐫𝐞 𝐟𝐨𝐫 𝐟𝐮𝐧, 𝐰𝐢𝐭𝐭𝐲 𝐜𝐡𝐚𝐭𝐬, 𝐚𝐧𝐝 𝐚 𝐛𝐢𝐭 𝐨𝐟 𝐩𝐥𝐚𝐲𝐟𝐮𝐥 𝐛𝐚𝐧𝐭𝐞𝐫 🎭

> 𝐅𝐞𝐞𝐥 𝐟𝐫𝐞𝐞 𝐭𝐨 𝐭𝐚𝐥𝐤 𝐭𝐨 𝐦𝐞 𝐚𝐛𝐨𝐮𝐭 𝐚𝐧𝐲𝐭𝐡𝐢𝐧𝐠! 💬
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("ADD ME TO YOUR GROUP", url=f"https://t.me/YourBotUsername?startgroup=true")],
    [InlineKeyboardButton("SUPPORT", url="https://t.me/Siya_Support"),
     InlineKeyboardButton("UPDATES", url="https://t.me/Siya_Updates")],
    [InlineKeyboardButton("OWNER", url="https://t.me/Uzumaki_X_Naruto_6"),
     InlineKeyboardButton("HELP", callback_data="help")]
])

# ------------------ /start COMMAND ------------------ #
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    # Track user or group
    if update.effective_chat.type == "private":
        add_private_user(user_id, username)
    else:
        add_group_chat(update.effective_chat.id, update.effective_chat.title)

    # Send start message
    await update.message.reply_photo(
        photo=START_IMAGE,
        caption=START_CAPTION,
        reply_markup=START_BUTTONS
    )

# ------------------ REGISTER FUNCTION FOR MAIN.PY ------------------ #
def register(application):
    application.add_handler(CommandHandler("start", start_command))