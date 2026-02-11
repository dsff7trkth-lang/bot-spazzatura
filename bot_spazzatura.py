import os
import logging
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURAZIONE ---
TOKEN = '8417218844:AAGtp-eA6WefQXFCu4jmGRyR2ipvYktSvfE'
CHAT_ID_GRUPPO = '-1071202678' #

# IL VOSTRO CALENDARIO (0=Lun, 1=Mar, 2=Mer, 3=Gio, 4=Ven, 5=Sab, 6=Dom)
calendario_fisso = {
    0: "Secco (Indifferenziata) 🗑️",
    1: "Umido + Vetro 🍏🍾",
    2: "Cartone 📦",
    3: "Umido 🍏",
    4: "Plastica 🍼",
    5: "Niente, riposo! 😴",
    6: "Umido 🍏"
}

# FUNZIONE COMANDO /OGGI
async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Definiamo oggi_num così non dà più errore alla riga 55
    oggi_num = datetime.datetime.now().weekday()
    tipo = calendario_fisso.get(oggi_num, "Niente")
    
    keyboard = [[InlineKeyboardButton("L'ho portata iooooo yee! ", callback_data='fatto')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Oggi il turno è: *{tipo}*\nChi la butta?", 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

# FUNZIONE PER IL TASTO "L'HO PORTATA IO"
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_name = query.from_user.first_name
    await query.edit_message_text(text=f"Grazie {user_name}! ✅ La spazzatura è stata portata fuoriiiii yuppiiiii")

# FUNZIONE PROMEMORIA AUTOMATICO
async def promemoria_automatico(context: ContextTypes.DEFAULT_TYPE):
    oggi_num = datetime.datetime.now().weekday()
    tipo = calendario_fisso.get(oggi_num)
    if "Niente" not in tipo:
        testo = f"🔔 *PROMEMORIA*\nStasera bisogna esporre: *{tipo}*\n\nScrivete /oggi per segnare chi la porta!"
        await context.bot.send_message(chat_id=CHAT_ID_GRUPPO, text=testo, parse_mode='Markdown')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Comandi
    application.add_handler(CommandHandler('oggi', oggi))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Promemoria automatico ogni sera alle 20:00
    application.job_queue.run_daily(promemoria_automatico, time=datetime.time(hour=20, minute=0, second=0))
    
    print("Bot avviato correttamente!")
    application.run_polling()
