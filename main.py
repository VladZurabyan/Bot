# Проверим и исправим main.py с учётом правильного форматирования строк
fixed_main_py = '''\
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")  # Получаем токен из переменной окружения

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Начать", callback_data="start_clicked")],
        [InlineKeyboardButton("💸 Адрес TRON (TRC-20)", callback_data="get_tron")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 Привет! Нажми кнопку ниже, чтобы начать:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    if query.data == "start_clicked":
        message = (
            f"🌟 Добро пожаловать, {user.first_name}!\n\n"
            "Мы рады видеть тебя в нашем Telegram-боте. Надеемся, тебе понравится! 😊"
        )
        with open("welcome_usdt_bright.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=message)

    elif query.data == "get_tron":
        tron_address = "TABC1234567890XYZ..."  # Замените на свой реальный адрес TRC-20
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"💰 Адрес TRON (TRC-20):\\n`{tron_address}`",
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
'''

# Сохраняем исправленный main.py
with open(os.path.join(project_name, "main.py"), "w", encoding="utf-8") as f:
    f.write(fixed_main_py)

# Пересоздаём архив
zip_path = "/mnt/data/telegram_greeting_bot_fixed.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for root, _, files in os.walk(project_name):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, project_name)
            zipf.write(full_path, arcname)

zip_path  # Путь к исправленному архиву

