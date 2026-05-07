import asyncio
from aiogram import Bot, Dispatcher

from bot.core.config import settings
from bot.routers.start import start_rt
from bot.routers.help import help_rt
from bot.routers.searech import search_rt
from bot.routers.prediction import prediction_rt
from bot.keybords.command import set_commands

# Создаем бота и диспетчер
bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

# Точка входа
async def main():
    print("Бот запущен...")
    await  bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(start_rt, help_rt, search_rt, prediction_rt)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())