from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, responder_mensagem

TOKEN = '8104465905:AAE45QOfgX6L6IpidS3kcMSgXwg8XF71obk'

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensagem))

    print("Bot rodando...")
    app.run_polling()
