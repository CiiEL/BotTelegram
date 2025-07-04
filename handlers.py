from telegram import Update
from telegram.ext import ContextTypes
from respostas import respostas_rapidas, gatilhos, respostas_seguimento
from datetime import datetime, timedelta
import os

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
    print(f"[Recebido]: {texto}")

    respostas_afirmativas = ["sim", "quero", "topo", "tenho interesse", "claro", "sim quero"]
    ultimo_topico = context.user_data.get("ultimo_topico")

    if any(p in texto for p in respostas_afirmativas):
        if ultimo_topico and ultimo_topico in respostas_seguimento:
            await update.message.reply_text(respostas_seguimento[ultimo_topico])
            return

    for chave, palavras in gatilhos.items():
        if any(p in texto for p in palavras):
            context.user_data["ultimo_topico"] = chave
            print(f"[Respondendo com]: {chave}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=respostas_rapidas[chave])
            return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="😅 Não entendi bem, mas me explica melhor que eu te ajudo!"
    )

BASE_PATH = "conteudo"

async def listar_conteudo(update: Update, context: ContextTypes.DEFAULT_TYPE, professor: str):
    caminho = os.path.join(BASE_PATH, professor.lower())

    if not os.path.exists(caminho):
        await update.message.reply_text("❌ Conteúdo não encontrado.")
        return

    arquivos = os.listdir(caminho)
    if not arquivos:
        await update.message.reply_text("📂 Ainda não há arquivos neste professor.")
        return

    await update.message.reply_text(f"📚 Conteúdo do Professor {professor.capitalize()}:")

    for nome_arquivo in arquivos:
        caminho_arquivo = os.path.join(caminho, nome_arquivo)

        if nome_arquivo.lower().endswith((".mp4", ".mov", ".avi")):
            with open(caminho_arquivo, "rb") as video:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video)
        elif nome_arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
            with open(caminho_arquivo, "rb") as foto:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=foto)
        else:
            with open(caminho_arquivo, "rb") as doc:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=doc)

async def professorx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await listar_conteudo(update, context, "professor_x")

async def professory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await listar_conteudo(update, context, "professor_y")

async def descobrir_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"O ID deste grupo é: {chat_id}")

async def liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /liberar @usuario")
        return

    user_to_invite = context.args[0]

    try:
        link = await context.bot.create_chat_invite_link(
            chat_id=-4913959022,
            name=f"Acesso de {user_to_invite}",
            expire_date=datetime.utcnow() + timedelta(hours=24),
            member_limit=1
        )
        await update.message.reply_text(
            f"✅ Acesso liberado para {user_to_invite}:\n{link.invite_link}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao gerar link: {e}")

async def acessar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name

    try:
        link = await context.bot.create_chat_invite_link(
            chat_id=-4913959022,
            name=f"Acesso de {nome}",
            expire_date=datetime.utcnow() + timedelta(hours=24),
            member_limit=1
        )

        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 Olá {nome}! Aqui está seu link de acesso ao grupo VIP:\n{link.invite_link}"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Ocorreu um erro ao gerar seu acesso: {e}")
