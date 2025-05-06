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

        with open("welcome.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo, caption=message)

    elif query.data == "get_tron":
        tron_address = "TABC1234567890XYZ..."  # Замените на свой реальный адрес TRC-20
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"💰 Адрес TRON (TRC-20):\n`{tron_address}`",
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
