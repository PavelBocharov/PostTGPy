from telegram import Bot
import asyncio

async def main():
    bot_token = input("Введите токен бота: ")
    bot = Bot(token=bot_token)
    
    updates = await bot.get_updates()
    print("\nДоступные чаты:")
    for update in updates:
        if update.message:
            chat = update.message.chat
            print(f"Название: {chat.title if chat.title else chat.first_name}")
            print(f"ID: {chat.id}")
            print("---")

if __name__ == "__main__":
    asyncio.run(main())