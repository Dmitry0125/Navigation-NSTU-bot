from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

button_academic_buildings = KeyboardButton(text=LEXICON_RU['academic_buildings'])
button_dormitories = KeyboardButton(text=LEXICON_RU['dormitories'])
button_Gorsky_Campus = KeyboardButton(text=LEXICON_RU['Gorsky_Campus'])

# Инициализируем билдер для клавиатуры
start = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
start.row(button_academic_buildings, button_dormitories, button_Gorsky_Campus, width=1)

# Создаем клавиатуру с кнопками
start: ReplyKeyboardMarkup = start.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
