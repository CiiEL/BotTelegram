from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, responder_mensagem, professorx, professory, descobrir_chat_id, liberar, acessar






TOKEN = '8104465905:AAE45QOfgX6L6IpidS3kcMSgXwg8XF71obk'

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("professorx", professorx))
    app.add_handler(CommandHandler("professory", professory))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensagem))
    app.add_handler(CommandHandler("idgrupo", descobrir_chat_id))
    app.add_handler(CommandHandler("liberar", liberar))
    app.add_handler(CommandHandler("acessar", acessar))


    

    print("Bot rodando...")
    app.run_polling()
