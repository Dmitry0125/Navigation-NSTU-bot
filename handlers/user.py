from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from lexicon.lexicon import LEXICON_RU

from keyboards.start_kb import start
from keyboards.target_kb import target
from routes.navigation_service import NavigationService
from keyboards.continue_kb import continue_kb

# Инициализируем роутер уровня модуля
user_router = Router()

# Храним выбранный корпус в памяти (простой способ)
user_selections = {}

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

    await message.answer("Помогу найти аудиторию в 3а или 3б корпусе.\n"
             "Все маршруты начинаются от **1 корпуса**.\n\n"
             "**Выбери корпус:**", reply_markup=target, parse_mode="Markdown")

# Этот хэндлер срабатывает на сообщение "⬅ Главное меню"
@user_router.message(F.text == LEXICON_RU['back_to_main_menu'])
async def process_answer(message: Message):
    await message.answer(text=LEXICON_RU['back_to_main_menu_answer'], reply_markup=start)

# Выбор корпуса
@user_router.message(F.text.in_(["3a корпус", "3б корпус"]))
async def select_corpus(message: Message):
    # Определяем номер корпуса
    if "3a" in message.text:
        corpus = "3a"
    else:
        corpus = "3б"
    
    user_selections[message.from_user.id] = corpus
    
    await message.answer(
        text=f"✅ **Выбран {corpus} корпус**\n\n"
             f"**Введи номер аудитории:**\n"
             f"• 3 цифры (101, 201)\n"
             f"• Можно с русской буквой (101А, 203Б, 108В)\n\n",
        parse_mode="Markdown"
    )

# Кнопка "Найти другую аудиторию"
@user_router.message(F.text == "Найти другую аудиторию")
async def find_another_room(message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_selections:
        await message.answer(
            "⚠ **Сначала выбери корпус!**\n\n"
            "Нажми '3a корпус' или '3б корпус'",
            reply_markup=target,
            parse_mode="Markdown"
        )
        return
    
    corpus = user_selections[user_id]
    
    await message.answer(
        f"🔍 **Ищем аудиторию в {corpus} корпусе**\n\n"
        f"Введи номер аудитории:",
        parse_mode="Markdown"
    )

# Кнопка "Сменить корпус"
@user_router.message(F.text == "Сменить корпус")
async def change_corpus(message: Message):
    if message.from_user.id in user_selections:
        del user_selections[message.from_user.id]
    
    await message.answer(
        "**Выбери новый корпус:**",
        reply_markup=target,
        parse_mode="Markdown"
    )

# Обработка ввода номера аудитории
@user_router.message(F.text)
async def process_room_input(message: Message):
    user_id = message.from_user.id
    room_input = message.text.strip()
    
    # Проверяем, выбран ли корпус
    if user_id not in user_selections:
        await message.answer(
            "⚠ **Сначала выбери корпус!**\n\n"
            "Нажми '3a корпус' или '3б корпус'",
            reply_markup=target,
            parse_mode="Markdown"
        )
        return
    
    target_corpus = user_selections[user_id]
    
    # Получаем маршрут
    route_message, is_success = NavigationService.get_route_to_room(target_corpus, room_input)
    
    # Отправляем результат
    await message.answer(route_message, parse_mode="Markdown")
    
    # Предлагаем дальнейшие действия
    if is_success:
        await message.answer(
            f"**Что дальше?**\n\n"
            f"• Найти другую аудиторию в **{target_corpus}** корпусе\n"
            f"• Или сменить корпус",
            reply_markup=continue_kb,
            parse_mode="Markdown"
        )
    else:
        # Если ошибка, предлагаем ввести снова
        await message.answer(
            f"**Попробуй еще раз:**\n"
            f"Введи номер аудитории для {target_corpus} корпуса\n\n",
            parse_mode="Markdown"
        )
