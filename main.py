import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Загружаем переменные из .env
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")

source_channel_id = int(os.getenv("SOURCE_CHANNEL_ID"))
target_group_id = int(os.getenv("TARGET_GROUP_ID"))

# Создаем клиента
client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    try:
        await event.forward_to(target_group_id)
        print(f'✅ Переслано сообщение: {event.id}')
    except Exception as e:
        print(f'❌ Ошибка при пересылке: {e}')

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ Сессия недействительна. Получи новую строку SESSION_STRING.")
        return

    print("🤖 Бот запущен и слушает сообщения...")
    await client.run_until_disconnected()

asyncio.run(main())