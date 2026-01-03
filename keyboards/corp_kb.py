from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

button_back = KeyboardButton(text=LEXICON_RU['back_to_main_menu'])
button_building1 = KeyboardButton(text=LEXICON_RU['building1'])

# Инициализируем билдер для клавиатуры
corp = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
corp.row(button_back, button_building1, width=2)

# Создаем клавиатуру с кнопками
corp: ReplyKeyboardMarkup = corp.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
