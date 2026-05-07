from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.enums import ChatAction
import asyncio

from bot.service.searech import SearechService
from bot.service.request_api import InternalAPI
from bot.core.client import client


search_rt = Router()
service = SearechService(api=InternalAPI(client=client))



class SearchFlightState(StatesGroup):
    waiting_for_flight_number = State()
    waiting_for_flight_date = State()


@search_rt.message(Command("src"))
async def src_command(message: Message, state: FSMContext):
    await state.set_state(SearchFlightState.waiting_for_flight_number)

    await message.chat.do(ChatAction.TYPING)
    await asyncio.sleep(0.5)
    await message.answer(
        "✈️ Введите номер рейса.\n"
        "Пример: SU1234"
    )


@search_rt.message(SearchFlightState.waiting_for_flight_number)
async def get_flight_number(message: Message, state: FSMContext):
    await state.update_data(flight_number=message.text)

    await state.set_state(SearchFlightState.waiting_for_flight_date)

    await message.chat.do(ChatAction.TYPING)
    await asyncio.sleep(0.5)
    await message.answer(
        "📅 Теперь введите локальную дату рейса.\n"
        "Пример: ГГГГ-ММ-ДД"
    )


@search_rt.message(SearchFlightState.waiting_for_flight_date)
async def get_flight_date(message: Message, state: FSMContext):
    data = await state.get_data()

    flight_number = data["flight_number"]
    flight_date = message.text

    await message.chat.do(ChatAction.TYPING)
    await asyncio.sleep(0.5)
    await message.answer(
        f"🔍 Поиск рейса:\n\n"
        f"✈️ Рейс: {flight_number}\n"
        f"📅 Дата: {flight_date}"
    )
    await message.chat.do(ChatAction.TYPING) 
    text = await service.searech(flight_number, flight_date)
    await asyncio.sleep(0.5)
    await message.answer(text)

    await state.clear()