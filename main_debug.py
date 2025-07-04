import logging
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters
)
from handlers import start, responder_mensagem

TOKEN = '8104465905:AAE45QOfgX6L6IpidS3kcMSgXwg8XF71obk'

# Configura log detalhado
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Iniciando o bot...")

    app = ApplicationBuilder().token(TOKEN).build()

    # Comando /start
    app.add_handler(CommandHandler("start", start))
    # Qualquer mensagem comum
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensagem))

    logger.info("Bot está rodando. Aguardando mensagens.")
    app.run_polling()

if __name__ == '__main__':
    main()
