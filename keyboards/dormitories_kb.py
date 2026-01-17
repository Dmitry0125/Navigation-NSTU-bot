from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

button_dormitorie1 = KeyboardButton(text=LEXICON_RU['dormitorie1'])
button_dormitorie2 = KeyboardButton(text=LEXICON_RU['dormitorie2'])
button_dormitorie3 = KeyboardButton(text=LEXICON_RU['dormitorie3'])
button_dormitorie4 = KeyboardButton(text=LEXICON_RU['dormitorie4'])
button_dormitorie5 = KeyboardButton(text=LEXICON_RU['dormitorie5'])
button_dormitorie7 = KeyboardButton(text=LEXICON_RU['dormitorie7'])
button_dormitorie8 = KeyboardButton(text=LEXICON_RU['dormitorie8'])
button_dormitorie10 = KeyboardButton(text=LEXICON_RU['dormitorie10'])
button_back = KeyboardButton(text=LEXICON_RU['back_to_main_menu'])

# Инициализируем билдер для клавиатуры
dormitories = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=3
dormitories.row(button_dormitorie1, button_dormitorie2, button_dormitorie3, button_dormitorie4, button_dormitorie5, button_dormitorie7, button_dormitorie8, button_dormitorie10, width=3)
dormitories.row(button_back)

# Создаем клавиатуру с кнопками
dormitories: ReplyKeyboardMarkup = dormitories.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
