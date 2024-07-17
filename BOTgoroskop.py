
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import BeautifulSoup
import requests
import lxml

import os


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()
router = Router()
startp = 'https://avatars.dzeninfra.ru/get-zen_doc/1587994/pub_626d24ec3a1abb7854568247_626d25cc689829359d323a42/scale_1200'

d = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text=f'♈ Овен', callback_data= 'but_0'),
            types.InlineKeyboardButton(text=f' ♉ Телец', callback_data='but_1'),
            types.InlineKeyboardButton(text=f'♊ Близнецы', callback_data='but_2')
        ],
        [
            types.InlineKeyboardButton(text=f'♋ Рак', callback_data='but_3'),
            types.InlineKeyboardButton(text=f'♌ Лев', callback_data='but_4'),
            types.InlineKeyboardButton(text=f'♍ Дева', callback_data='but_5')
        ],
        [
            types.InlineKeyboardButton(text = f'♎ Весы', callback_data='but_6'),
            types.InlineKeyboardButton(text = f'♏Скорпирн', callback_data='but_7'),
            types.InlineKeyboardButton(text = f'♐ Стрелец', callback_data='but_8')
        ],
        [
            types.InlineKeyboardButton(text=f'♑ Козерог', callback_data='but_9'),
            types.InlineKeyboardButton(text=f'♒ Водолей', callback_data='but_10'),
            types.InlineKeyboardButton(text=f'♓ Рыбы', callback_data='but_11')
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await bot.send_photo(message.chat.id, startp,
                         caption="Гороскоп на сегодня для всех знаков Задиака",
                         reply_markup = get_keyboard())
@dp.callback_query(F.data.startswith('but_'))

async def first(callback: types.CallbackQuery):
    r = int(callback.data.split('_')[1])
    url = f'https://www.thevoicemag.ru/horoscope/daily/{d[r]}/'  # после слэша занак задиака и закрывающий слэш
    res = requests.get(url)
    bs = BeautifulSoup(res.text,"lxml")
    qq = bs.find_all('div', class_='sign__description-text')
    for q in qq:
        await callback.message.answer(q.text)


if __name__ == '__main__':
    dp.run_polling(bot)
