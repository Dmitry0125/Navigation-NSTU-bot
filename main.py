import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from handlers.user import user_router
from handlers.other import other_router
from keyboards.menu_commands import set_main_menu

# Функция конфигурирования и запуска бота
async def main():
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(other_router)

    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # Запускаем polling
    await dp.start_polling(bot)

asyncio.run(main())
