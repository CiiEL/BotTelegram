from telegram import Update
from telegram.ext import ContextTypes
from respostas import respostas_rapidas, gatilhos

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = (
        f"Olá, {user.first_name}!\n\n"
        "Sou o assistente do Maciel 🎙️\n"
        "Você pode perguntar sobre:\n"
        "• Aulas de narração\n"
        "• Valores\n"
        "• Formas de pagamento\n"
        "• Como entrar no grupo\n\n"
        "É só mandar sua mensagem!"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

async def responder_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    print(f"[Recebido]: {texto}")  # ← Aqui adicionamos o print

    for chave, palavras in gatilhos.items():
        if any(p in texto for p in palavras):
            print(f"[Respondendo com]: {chave}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=respostas_rapidas[chave])
            return

    await context.bot.send_message(chat_id=update.effective_chat.id, text="😅 Não entendi bem, mas me explica melhor que eu te ajudo!")
