import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")  # Убедись, что переменная окружения TOKEN задана на Render

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Начать", callback_data="start_clicked")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Привет! Нажми кнопку ниже, чтобы начать:", reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == "start_clicked":
        message = (
            f"🌟 Добро пожаловать, {user.first_name}!\n\n"
            "Ты можешь поддержать нас переводом на TON."
        )
        await context.bot.send_message(chat_id=query.message.chat_id, text=message)

        # Кнопка адреса
        ton_keyboard = [[InlineKeyboardButton("💎 Узнать адрес TON", callback_data="get_ton")]]
        reply_markup = InlineKeyboardMarkup(ton_keyboard)
        await context.bot.send_message(chat_id=query.message.chat_id, text="👇 Нажми кнопку:", reply_markup=reply_markup)

    elif query.data == "get_ton":
        ton_address = "EQC1234567890TONaddress..."  # замените на ваш адрес
        ton_message = "💎 Адрес TON:\n`" + ton_address + "`"
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=ton_message,
            parse_mode="Markdown"
        )

# Блокируем обычные сообщения
async def block_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except:
        pass

# Запуск
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, block_messages))
    app.run_polling()
