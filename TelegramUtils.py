from telegram.ext import ApplicationBuilder


async def send_post(bot_token: str, chat_id: str, image_path: str, caption: str, parse_mode):
    async with ApplicationBuilder().token(bot_token).build().bot as bot:
        await bot.send_photo(
            chat_id=chat_id,
            photo=image_path,
            caption=caption,
            parse_mode=parse_mode
        )
