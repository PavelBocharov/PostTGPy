import asyncio
import logging
import os
import time

import schedule
from dotenv import load_dotenv

import FileUtils
import TelegramUtils

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CONST_TEXT = os.getenv("CONST_TEXT")
TIMEOUT_MIN = int(os.getenv("TIMEOUT_MIN"))
ROOT_DIR = os.getenv("ROOT_DIR")
WATERMARK = os.getenv("WATERMARK")


def __create_caption(root_path: str, img_path: str, const_text: str):
    _, suff = os.path.splitext(img_path)
    tokens = (img_path
              .removeprefix(root_path)
              .removesuffix(suff)
              .replace("\\", "/")
              .split('/'))
    title = tokens[len(tokens) - 1]
    tokens.remove(title)
    tags = ""
    set_tokens = set(tokens)
    for token in set_tokens:
        tag = token.strip()
        if len(tag) > 0:
            tags += "#" + tag + " "

    if len(tags) == 0:
        return "<code>" + title + "</code> \n\n" + const_text
    else:
        return "<code>" + title + "</code> \n\n" + tags + "\n" + const_text


def job():
    imgs = FileUtils.get_list_images(root_dir=ROOT_DIR)
    for img in imgs:
        img_with_wm = FileUtils.add_watermark(ROOT_DIR, img, WATERMARK)
        try:
            asyncio.run(TelegramUtils.send_post(
                bot_token=BOT_TOKEN,
                chat_id=CHAT_ID,
                image_path=img_with_wm,
                caption=__create_caption(ROOT_DIR, img, CONST_TEXT),
                parse_mode="HTML"
            ))
            os.remove(img)
        except Exception as e:
            print("Error, but need work. Error: %s" % e)
            os.replace(img, img + ".error")
        finally:
            os.remove(img_with_wm)


if __name__ == '__main__':
    schedule.every(TIMEOUT_MIN).minute.do(job)
    just_work = True
    while just_work:
        try:
            schedule.run_pending()
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nEND script")
            just_work = False