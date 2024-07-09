import asyncio
import logging
import sys
import requests

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)

TOKEN = "7002675047:AAFpyadN9TfkEkcVtDLKtMJjqTc1CzS-bHA"
bot = Bot(token=TOKEN)
dp = Dispatcher()
res = requests.get("http://127.0.0.1:8000/api/books").json()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=f"Salom {message.chat.full_name},\n\nbu bot yordamida kitoblar yuklab olishingiz mumkin",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Kategoriyalar", callback_data="category")]
            ]
        ),
    )
    
@dp.callback_query(F.data == "category")
async def category(callback: CallbackQuery):
    btn = InlineKeyboardBuilder()
    s = set()
    for i in res:
        s.add(i['category'])
    for x in s:
        btn.add(InlineKeyboardButton(text=f"{x}", callback_data=f"slug##{x}"))
        
    await callback.message.answer(
        text="Kategoriyalardan birini tanlang",
        reply_markup=btn.as_markup()
        )
    
@dp.callback_query(F.data.startswith("slug##"))
async def slug(callback: CallbackQuery):
    categ = callback.data.split("##")[1]
    btn = InlineKeyboardBuilder()
    for i in res:
        if str(i["category"]) == str(categ):
            btn.add(InlineKeyboardButton(text=f"{i['name']}", callback_data=f"info##{categ}##{i['name']}"))
        
    await callback.message.answer(
        text=f"Kategoriya: {categ}\n\nMarhamat kerakli kitobni tanlang.",
        reply_markup=btn.as_markup()
    )
    
@dp.callback_query(F.data.startswith("info##"))
async def info(callback: CallbackQuery):
    action = callback.data.split("##")
    categ = action[1]
    name = action[2]
    for i in res:
        if str(i["category"]) == str(categ):
            if i["name"] == str(name):
                await callback.message.answer_photo(
                    photo=f"{i["rasm"]}",
                    caption=f"""Kategoriya: {categ}
                    
Kitob nomi: {name}

Ma'lumot: {i["info"]}""",
reply_markup=InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Yuklab olish", callback_data="tr")
        ]
    ]
)
                )
        



async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
