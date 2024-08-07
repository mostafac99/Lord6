import asyncio
import logging

from pyrogram import Client, idle, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from config import Config

from util import get_random_mail, emails_task

app = Client(
    "Catdns",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TG_BOT_TOKEN,
    skip_updates=True,
    sleep_threshold=30
)

logging.basicConfig(level=logging.INFO)

@app.on_message(filters.command("start") & filters.private)
async def welcome_message(_, m: Message) -> Message:
    message = (
        "**- مرحبا بك عزيزي 🫂.**\n"
        "**- في بوت إنشاء إيميل وهمي 🥇**\n"
        "**- يقوم بعمل ايميل وهمي لك بكل سهوله 📧**\n"
        "**- لـ إنشاء ايميل وهمي جديد ارسل:** /temp\n\n"
        "**- مطور البوت: @K7EEE 🧑🏻‍💻**"
    )
    return await m.reply(
        text=message,
        quote=True,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

@app.on_message(filters.command("temp") & filters.private)
async def get_temp_mail(_, m: Message) -> Message:
    random_mail = get_random_mail(m.from_user.id)
    return await m.reply(
        "**• تم انشاء ايميل لك .. بنجاح ✅**\n **- الايميل 📧:** `{}`\n\n**- الايميل متاح لساعة فقط من الان ⏳**\n**- سوف تصلك الرسائل تلقائياً 📬".format(random_mail),
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("عرض في المتصفح 🌐", url="https://email.catdns.in/{}".format(random_mail.split("@catdns.in")[0]))
                ]
            ]
        )
    )

async def main():
    await app.start()
    asyncio.create_task(emails_task(app=app))
    await idle()
    await app.stop()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=loop)

    loop.run_until_complete(main())