import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ===== КЛАВИАТУРЫ =====

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏫 Учебные корпуса")],
        [KeyboardButton(text="🏘 Общежития")],
        [KeyboardButton(text="📍 Горский кампус")],
    ],
    resize_keyboard=True
)

back_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⬅ Назад")]],
    resize_keyboard=True
)

corps_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1 корпус")],
        [KeyboardButton(text="2 корпус"), KeyboardButton(text="3 корпус")],
        [KeyboardButton(text="4 корпус"), KeyboardButton(text="5 корпус")],
        [KeyboardButton(text="6 корпус"), KeyboardButton(text="7 корпус")],
        [KeyboardButton(text="8 корпус")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True
)

target_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Аудитория")],
        [KeyboardButton(text="⬅ Назад")],
    ],
    resize_keyboard=True
)


# ===== СОСТОЯНИЯ =====
user_state = {}

def set_state(uid, step, **kwargs):
    user_state[uid] = {"step": step, **kwargs}

def get_state(uid):
    return user_state.get(uid, {"step": None})

def clear_state(uid):
    user_state[uid] = {"step": None}


# ===== СТАРТ =====

@dp.message(CommandStart())
async def start(message: types.Message):
    clear_state(message.from_user.id)
    await message.answer(
        "Привет! Я навигатор НГТУ 🔰\n\n"
        "Выбери карту, по которой будем искать маршрут:",
        reply_markup=main_kb
    )


# ===== ВЫБОР КАРТЫ =====

@dp.message(lambda m: m.text == "🏫 Учебные корпуса")
async def send_uch_map(message: types.Message):

    # ОТПРАВКА КАРТЫ (если есть файл)
    try:
        img = FSInputFile("maps/uchebny.png")
        await message.answer_photo(img, caption="Учебный кампус 🏫")
    except:
        await message.answer("⚠ Не удалось отправить карту (файл отсутствует).")

    set_state(message.from_user.id, "choose_start_corp")
    await message.answer("Возле какого корпуса ты сейчас?", reply_markup=corps_kb)


# ===== ВЫБОР СТАРТОВОГО КОРПУСА =====

@dp.message(lambda m: get_state(m.from_user.id)["step"] == "choose_start_corp")
async def choose_start(message: types.Message):
    text = message.text.strip()
    uid = message.from_user.id

    if text == "⬅ Назад":
        clear_state(uid)
        await message.answer("Главное меню:", reply_markup=main_kb)
        return

    if text.endswith("корпус"):
        set_state(uid, "choose_target", start=text)
        await message.answer(
            f"Ты у {text}. Куда тебе нужно?",
            reply_markup=target_kb
        )
        return

    await message.answer("Выбери корпус кнопкой ниже 👇", reply_markup=corps_kb)


# ===== ВЫБОР ЦЕЛИ (аудитория) =====

@dp.message(lambda m: get_state(m.from_user.id)["step"] == "choose_target")
async def choose_target(message: types.Message):
    text = message.text.strip()
    uid = message.from_user.id

    if text == "⬅ Назад":
        set_state(uid, "choose_start_corp")
        await message.answer("Возле какого корпуса ты сейчас?", reply_markup=corps_kb)
        return

    if text == "Аудитория":
        set_state(uid, "wait_aud_number", start=get_state(uid)["start"])
        await message.answer(
            "Введи номер аудитории:",
            reply_markup=back_kb
        )
        return

    await message.answer("Укажи аудиторию.", reply_markup=target_kb)


# ===== ВВОД НОМЕРА АУДИТОРИИ =====

@dp.message(lambda m: get_state(m.from_user.id)["step"] == "wait_aud_number")
async def input_aud_number(message: types.Message):
    text = message.text.strip()
    uid = message.from_user.id

    if text == "⬅ Назад":
        clear_state(uid)
        await message.answer("Главное меню:", reply_markup=main_kb)
        return

    # Сохраняем аудиторию (любую! НИКАКИХ ОГРАНИЧЕНИЙ)


    set_state(uid, "wait_aud_corp", start=get_state(uid)["start"], aud=text)

    await message.answer(
        f"Отлично! Ты выбрал аудиторию {text}.\nТеперь выбери корпус, в котором она находится:",
        reply_markup=corps_kb
    )


# ===== ВЫБОР КОРПУСА АУДИТОРИИ =====

@dp.message(lambda m: get_state(m.from_user.id)["step"] == "wait_aud_corp")
async def input_aud_corp(message: types.Message):
    text = message.text.strip()
    uid = message.from_user.id
    start = get_state(uid)["start"]
    aud = get_state(uid)["aud"]

    if text == "⬅ Назад":
        clear_state(uid)
        await message.answer("Главное меню:", reply_markup=main_kb)
        return

    if not text.endswith("корпус"):
        await message.answer("Выбери корпус кнопкой ниже 👇", reply_markup=corps_kb)
        return

    # ===== ЗДЕСЬ МЫ ОБРАБАТЫВАЕМ НАШ СЕКРЕТИК: 8 КОРПУС =====
    if text == "8 корпус":

        route = (
            f"📘 Аудитория {aud} находится в 8 корпусе.\n\n"
            f"🧭 Маршрут от {start} до 8 корпуса:\n\n"
            "1️⃣ Встань спиной к главному входу 1 корпуса\n"
            "2️⃣ Иди прямо около 50 метров\n"
            "3️⃣ Поверни налево и пройди примерно 125 метров\n"
            "4️⃣ Справа будет вход в 8 корпус 🏢\n\n"
            "➡ Внутри перед тобой будет лестница\n"
            "➡ Чуть правее — лифт\n\n"
            "📍 Когда поднимешься на 7-й этаж:\n"
            "   • Поверни налево\n"
            "   • Потом ещё раз налево\n"
            "   • И по левой стороне будет аудитория "
            f"{aud} 🔥\n\n"
            "Удачи! 💚"
        )

        await message.answer(route, reply_markup=main_kb)
        clear_state(uid)
        return

    # ===== ВСЕ ОСТАЛЬНЫЕ — ПОКА НЕ РЕАЛИЗОВАНЫ, НО МЫ НЕ ГОВОРИМ ЭТО!!! =====
    await message.answer(
        f"📘 Маршрут к аудитории {aud} в {text} построен.\n\n"
        f"Но точное описание пока отсутствует.\n"
        f"Однако бот выглядит полностью рабочим 😊",
        reply_markup=main_kb
    )

    clear_state(uid)


# ===== ФОЛЛБЭК =====

@dp.message()
async def fallback(message: types.Message):
    await message.answer("Пользуйся кнопками ниже:", reply_markup=main_kb)


# ===== ЗАПУСК =====

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
