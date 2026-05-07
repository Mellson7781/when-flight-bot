from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ChatAction
import asyncio

help_rt = Router()


@help_rt.message(Command("help"))
async def help_command(message: Message):
    text = (
        "📚 Справка по командам бота\n\n"
        "✈️ /src — поиск рейса\n"
        "После команды бот попросит ввести номер рейса, затем локальную дату.\n"
        "В результате вы получите информацию по рейсу.\n\n"
        "📈 /prediction — прогноз рейса\n"
        "После команды бот попросит ввести номер рейса, затем дату.\n"
        "В ответ будет сформирован прогноз рейса.\n\n"
        "ℹ️ Просто выберите нужную команду и следуйте инструкциям."
    )
    await message.chat.do(ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer(text)