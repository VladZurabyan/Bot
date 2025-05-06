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

TOKEN = os.getenv("TOKEN")  # Установи переменную окружения TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Приветствие с картинкой
    with open("welcome.jpg", "rb") as photo:
        caption = (
            f"✨\n\n"
            f"🌟 *Добро пожаловать, {user.first_name}!* 🌟\n\n"
            f"_Ты можешь поддержать нас переводом на TON._\n\n"
            f"✨"
        )
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=caption,
            parse_mode="Markdown"
        )

    # Ждём 5 секунд
    await asyncio.sleep(5)

    # Кнопка — одна и по центру
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Узнать адрес TON", callback_data="get_ton")]
    ])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👇",
        reply_markup=keyboard
    )

# Ответ на кнопку
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_ton":
        ton_address = "EQC1234567890TONaddress..."  # ← Замени на свой TON-адрес
        message = (
            f"💎 *TON адрес для поддержки:*\n\n"
            f"`{ton_address}`"
        )
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            parse_mode="Markdown"
        )

# Удаление всех пользовательских сообщений
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
