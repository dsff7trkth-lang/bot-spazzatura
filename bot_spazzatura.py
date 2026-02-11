import os
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- METTI IL NUOVO TOKEN QUI SOTTO ---
TOKEN = '8417218844:AAGyHF-mBGKakHPG-SNjwDtmZEJUPtj73ew'
CHAT_ID_GRUPPO = '-1071202678'

calendario_fisso = {
    0: "Secco (Indifferenziata) 🗑️",
    1: "Umido + Vetro 🍏🍾",
    2: "Cartone 📦",
    3: "Umido 🍏",
    4: "Plastica 🍼",
    5: "Niente, riposo! 😴",
    6: "Umido 🍏"
}

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Prende il giorno attuale senza errori di nomi
    oggi_num = datetime.datetime.now().weekday()
    tipo = calendario_fisso.get(oggi_num, "Niente")
    
    keyboard = [[InlineKeyboardButton("L'ho portata iooo yeeee", callback_data='fatto')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Turno attuale: *{tipo}*\nChi la butta?", 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_name = query.from_user.first_name
    await query.edit_message_text(text=f"Grazieeee {user_name}! ✅ Portata fuori superlusso🤩.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('oggi', oggi))
    application.add_handler(CallbackQueryHandler(button_callback))
    print("Bot online!")
    application.run_polling()
