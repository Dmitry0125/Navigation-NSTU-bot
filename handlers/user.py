from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from lexicon.lexicon import LEXICON_RU

from keyboards.start_kb import start
from keyboards.corp_kb import corp
from keyboards.target_kb import target
from keyboards.audience_kb import audience

# Инициализируем роутер уровня модуля
user_router = Router()

# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=start)

# Этот хэндлер срабатывает на команду /help
@user_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

# Этот хэндлер срабатывает на сообщение "🏫 Учебные корпуса"
@user_router.message(F.text == LEXICON_RU['academic_buildings'])
async def process_answer(message: Message):
    try:
        img = FSInputFile("maps/uchebny.png")
        await message.answer_photo(img, caption=LEXICON_RU['academic_campus'])
    except:
        await message.answer("⚠ Не удалось отправить карту (файл отсутствует).")

    await message.answer("Возле какого корпуса ты сейчас?", reply_markup=corp)

# Этот хэндлер срабатывает на сообщение "1 корпус"
@user_router.message(F.text == LEXICON_RU['building1'])
async def process_answer(message: Message):
    await message.answer(text=LEXICON_RU['building1_answer'], reply_markup=audience)

# Этот хэндлер срабатывает на сообщение "⬅ Главное меню"
@user_router.message(F.text == LEXICON_RU['back_to_main_menu'])
async def process_answer(message: Message):
    await message.answer(text=LEXICON_RU['back_to_main_menu_answer'], reply_markup=start)

# Этот хэндлер срабатывает на сообщение "Аудитория"
@user_router.message(F.text == LEXICON_RU['audience'])
async def process_answer(message: Message):
    await message.answer(text=LEXICON_RU['audience_answer'])
