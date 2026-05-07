from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction
from aiogram.types import Message

import asyncio

start_rt = Router()


@start_rt.message(CommandStart())
async def start_command(message: Message):
    await message.chat.do(ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer(
        f"Приветствую, {message.from_user.first_name}! 👋\n"
        "💻Добро пожаловать в бота для отслежевания вашего рейса и прогноза его задержки!\n"
        "Воспользуйтесь меню команд ниже💬"
    )