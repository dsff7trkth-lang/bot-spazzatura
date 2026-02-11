import logging
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURAZIONE ---
TOKEN = '8417218844:AAGtp-eA6WefQXFCu4jmGRyR2ipvYKtSvfE'

CHAT_ID_GRUPPO = '-1071202678' # Lo scoprirai col comando /info

# Calendario dei ritiri
# Nota: La chiave √® il giorno in cui passa il camion
calendario = {
    0: "Secco (Indifferenziata) üóëÔ∏è", # Luned√¨
    1: "Umido + Vetro üçèüçæ",          # Marted√¨
    2: "Cartone üì¶",                  # Mercoled√¨
    3: "Umido üçè",                   # Gioved√¨
    4: "Plastica üçº",                # Venerd√¨
    5: "Nessun ritiro domani",       # Sabato
    6: "Umido üçè"                    # Domenica
}

# Variabile per tracciare chi ha buttato la spazzatura oggi
stato_giornaliero = {"fatto": False, "chi": None, "data": None}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao ragazze! Sono il vostro assistente per la spazzatura. üóëÔ∏è\nUsa /oggi per vedere cosa buttare e segnare chi lo fa.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Comando per scoprire l'ID del gruppo
    await update.message.reply_text(f"L'ID di questa chat √®: {update.effective_chat.id}")

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Controlliamo cosa si butta stasera (per domani)
    oggi_settimana = datetime.datetime.now().weekday()
    domani = (oggi_settimana + 1) % 7
    tipo = calendario.get(domani, "Niente")
    
    data_oggi = datetime.date.today()
    
    # Se √® un nuovo giorno, resetta lo stato
    if stato_giornaliero["data"] != data_oggi:
        stato_giornaliero["fatto"] = False
        stato_giornaliero["chi"] = None
        stato_giornaliero["data"] = data_oggi

    if tipo == "Nessun ritiro domani":
        await update.message.reply_text("Stasera non c'√® bisogno di uscire nulla! üéâ")
        return

    text = f"Stasera bisogna esporre: *{tipo}*"
    
    if stato_giornaliero["fatto"]:
        text += f"\n\n‚úÖ Gi√† fatto da {stato_giornaliero['chi']}!"
        await update.message.reply_text(text, parse_mode='Markdown')
    else:
        keyboard = [[InlineKeyboardButton("L'ho portata io! üôã‚Äç‚ôÄÔ∏è", callback_data='fatto')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_data
    await query.answer()
    
    user_name = query.from_user.first_name
    stato_giornaliero["fatto"] = True
    stato_giornaliero["chi"] = user_name
    stato_giornaliero["data"] = datetime.date.today()
    
    await query.edit_message_text(text=f"Grazie {user_name}! üåü La spazzatura √® stata portata fuori.")

async def promemoria_serale(context: ContextTypes.DEFAULT_TYPE):
    # Questa funzione viene chiamata automaticamente ogni sera
    domani = (datetime.datetime.now().weekday() + 1) % 7
    tipo = calendario.get(domani)
    
    if tipo != "Nessun ritiro domani":
        text = f"üîî *PROMEMORIA STASERA*\nBisogna buttare: *{tipo}*\n\nChi di voi la porta fuori? Scrivete /oggi per segnarlo!"
        await context.bot.send_message(chat_id=CHAT_ID_GRUPPO, text=text, parse_mode='Markdown')

def main():
    application = Application.builder().token(TOKEN).build()

    # Comandi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("oggi", oggi))
    application.add_handler(CallbackdataHandler(button_callback))

    # Programmazione promemoria: ogni giorno alle 20:00
    job_queue = application.job_queue
    job_queue.run_daily(promemoria_serale, time=datetime.time(hour=20, minute=0, second=0))

    print("Bot partito...")
    application.run_polling()

if __name__ == '__main__':
    main()
