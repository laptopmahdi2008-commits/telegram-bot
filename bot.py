import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ChatMemberUpdated
from aiogram.filters import CommandStart
from config import TOKEN, WELCOME_GIF_ID, BAD_WORDS
import logging
import random

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply("ربات با موفقیت فعال شد.")

@dp.message()
async def filter_messages(message: types.Message):
    if message.text:
        text = message.text.lower()
        # پاسخ به سلام ربات
        if "سلام ربات" in text:
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
            if word in text:
                await message.delete()
                await message.answer(f"{message.from_user.mention_html()} مشتی بد بد حرف نزن 😡")
                return

@dp.chat_member()
async def welcome_or_bye(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    if event.old_chat_member.status != "left" and event.new_chat_member.status == "left":
        await bot.send_message(event.chat.id, f"{user.mention_html()} راه باز، جاده دراز 🏃‍♂️")
    elif event.old_chat_member.status == "left" and event.new_chat_member.status == "member":
        await bot.send_animation(event.chat.id, animation=WELCOME_GIF_ID)
        await bot.send_message(event.chat.id, f"{user.mention_html()} سلام جیگر 😍")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
