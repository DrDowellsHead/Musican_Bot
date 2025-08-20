import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

try:
    from dotenv import load_dotenv

    load_dotenv()
    print("Переменные загружены")
except:
    print("Ошибка в .env-файле")

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Здесь токен бота
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")  # Здесь будет ID канала, куда надо переслать сообщения

if not BOT_TOKEN:
    print("Ошибка: Не найден BOT_TOKEN")
    exit()

if not TARGET_CHANNEL:
    print("Ошибка: Не найден TARGET_CHANNEL")
    exit()


async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Функция-обработчик для всех входящих сообщений
    update: объект с данными о входящем сообщении
    context: контекст выполнения, содержит дополнительную информацию
    """
    try:
        await update.message.forward(chat_id=TARGET_CHANNEL)

        print(f"Переслано сообщение от {update.message.from_user.id}")

    except Exception as e:
        print(f"Произошла ошибка при пересылке: {e}")


async def main():
    # Application.builder() - создает конструктор приложения
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.ALL, forward_message))

    print("Бот запущен")

    # Запускаем бота в режиме polling (постоянный опрос серверов Telegram на наличие новых сообщений)
    # run_polling() - асинхронно запускает процесс получения обновлений
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
