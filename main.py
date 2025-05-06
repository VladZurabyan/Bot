import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")  # Задай переменную TOKEN в окружении

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Отправка фото с приветствием
    with open("welcome.jpg", "rb") as photo:
        caption = f"🌟 Добро пожаловать, {user.first_name}!\n\nТы можешь поддержать нас переводом на TON."
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=caption)

    # Ждём 5 секунд
    await asyncio.sleep(5)

    # Отправляем кнопку "Узнать адрес TON"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Узнать адрес TON", callback_data="get_ton")]
    ])
    await context.bot.send_message(chat_id=update.effective_chat.id, text="👇 Нажми кнопку ниже:", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_ton":
        ton_address = "EQC1234567890TONaddress..."  # Замени на свой адрес
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"💎 Адрес TON:\n`{ton_address}`",
            parse_mode="Markdown"
        )

# Удаление всех текстовых сообщений от пользователей
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
