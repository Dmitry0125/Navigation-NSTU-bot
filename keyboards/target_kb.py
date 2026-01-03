from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

# button_back = KeyboardButton(text=LEXICON_RU['back'])
button_building3a = KeyboardButton(text=LEXICON_RU['building3a'])
button_building3b = KeyboardButton(text=LEXICON_RU['building3b'])

# Инициализируем билдер для клавиатуры
target = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
target.row(button_building3a, button_building3b, width=2)

# Создаем клавиатуру с кнопками
target: ReplyKeyboardMarkup = target.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
