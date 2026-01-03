from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

button_audience = KeyboardButton(text=LEXICON_RU['audience'])

# Инициализируем билдер для клавиатуры
audience = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
audience.row(button_audience, width=1)

# Создаем клавиатуру с кнопками
audience: ReplyKeyboardMarkup = audience.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
