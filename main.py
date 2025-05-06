import os
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Отправка приветственного изображения
    with open("welcome.jpg", "rb") as photo:
        caption = f"🌟 Добро пожаловать, {user.first_name}!\n\nТы можешь поддержать нас переводом на TON."
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=caption)

    # Кнопка "Начать" — по центру
    start_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Начать", callback_data="start_clicked")]
    ])
    await update.message.reply_text("👇 Нажми кнопку ниже:", reply_markup=start_keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    user = query.from_user

    if query.data == "start_clicked":
        await context.bot.send_message(
            chat_id=chat_id,
            text="⏳ Подготовка адреса TON..."
        )

        # Задержка 5 секунд
        await asyncio.sleep(5)

        # Кнопка "Узнать адрес TON" — по центру
        ton_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Узнать адрес TON", callback_data="get_ton")]
        ])
        await context.bot.send_message(
            chat_id=chat_id,
            text="Готово! Нажми кнопку ниже:",
            reply_markup=ton_keyboard
        )

    elif query.data == "get_ton":
        ton_address = "EQC1234567890TONaddress..."  # Замените на свой TON адрес
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"💎 Адрес TON:\n`{ton_address}`",
            parse_mode="Markdown"
        )

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
