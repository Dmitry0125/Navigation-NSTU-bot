from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

button_find_another_audience = KeyboardButton(text="Найти другую аудиторию")
button_change_corp = KeyboardButton(text="Сменить корпус")
button_back = KeyboardButton(text=LEXICON_RU['back_to_main_menu'])

# Инициализируем билдер для клавиатуры
continue_kb = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=2
continue_kb.row(button_find_another_audience, button_change_corp, button_back, width=2)

# Создаем клавиатуру с кнопками
continue_kb: ReplyKeyboardMarkup = continue_kb.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)
