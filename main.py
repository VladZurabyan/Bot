import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")  # Убедись, что переменная TOKEN задана

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Отправка фото с приветствием
    with open("welcome.jpg", "rb") as photo:  # Замените на путь к своему файлу
        caption = f"🌟 Добро пожаловать, {user.first_name}!\n\nТы можешь поддержать нас переводом на TON."
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=caption)

    # Кнопка "Узнать адрес"
    keyboard = [[InlineKeyboardButton("💎 Узнать адрес TON", callback_data="get_ton")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👇 Нажми кнопку:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_ton":
        ton_address = "EQC1234567890TONaddress..."  # замените на свой адрес
        text = f"💎 Адрес TON:\n`{ton_address}`"
        await context.bot.send_message(chat_id=query.message.chat_id, text=text, parse_mode="Markdown")

async def block_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except:
        pass

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, block_messages))
    app.run_polling()
