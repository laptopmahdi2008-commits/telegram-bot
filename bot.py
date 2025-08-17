# bot.py
import asyncio
import random
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ChatMemberUpdated
from aiogram.filters.command import CommandStart
from config import TOKEN, WELCOME_GIF_ID, BAD_WORDS

# تنظیمات اولیه
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# لیست پاسخ‌های سلام عامیانه
HELLO_RESPONSES = [
    "سلام مشتی جخبر؟ 😎",
    "چطوری رفیق؟ 👋",
    "سلامتی، خوبی؟ 😁",
    "هی سلام، چه خبر؟ 🤙",
    "سلام خوشتیپ! 😎"
]

# پاسخ به دستور /start
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply("🤖 ربات با موفقیت فعال شد.")

# هندلر پیام‌ها برای سلام و فیلتر ناسزا
@dp.message()
async def handle_messages(message: types.Message):
    if message.text:
        text = message.text.lower()

        # بررسی سلام با Regex (حذف حساسیت به فاصله و علائم)
        if re.search(r"سلام[^\w]*", text):
            await message.reply(random.choice(HELLO_RESPONSES), reply_to_message_id=message.message_id)
            return

        # بررسی "سلام ربات" با Regex
        if re.search(r"سلام[^\w]*ربات", text):
            replies = [
                "سلام مشتی، جخبر؟ 😎",
                "درود بر داش مشتی! 🌟",
                "سَلَام داشی! چطوری؟ 💥",
                "اومدی روشنم کنی؟ 😏",
                "قربون اون سلام گفتنت 🤝"
            ]
            await message.reply(random.choice(replies), reply_to_message_id=message.message_id)
            return

        # فیلتر ناسزا
        for word in BAD_WORDS:
            if re.search(rf"\b{re.escape(word.lower())}\b", text):
                await message.delete()
                await message.answer(f"{message.from_user.mention_html()} مشتی بد بد حرف نزن 😡")
                return

# خوش‌آمدگویی و خداحافظی کاربران
@dp.chat_member()
async def welcome_or_bye(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    # کاربر ترک کرد
    if event.old_chat_member.status != "left" and event.new_chat_member.status == "left":
        await bot.send_message(event.chat.id, f"{user.mention_html()} راه باز، جاده دراز 🏃‍♂️")
    # کاربر وارد شد
    elif event.old_chat_member.status == "left" and event.new_chat_member.status == "member":
        if WELCOME_GIF_ID:
            await bot.send_animation(event.chat.id, animation=WELCOME_GIF_ID)
        await bot.send_message(event.chat.id, f"{user.mention_html()} سلام جیگر 😍")

# اجرای ربات
async def main():
    logging.info("🤖 ربات با موفقیت راه‌اندازی شد!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
