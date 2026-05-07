from datetime import date, datetime
from bot.service.request_api import InternalAPI
from bot.schemas.flight import  Flight
from bot.error.api import ManyRequestAPI, APIBadRequest, APIOtherStatusHTTP, NotFoundFLight


class SearechService:
    def __init__(self, api: InternalAPI):
        self.api = api

    async def searech(self, number: str, date: date) -> str:
        try:
            flight = await self.api.get_data_flight(number, date)
            text = await self._format_flight(flight)
        except ManyRequestAPI:
            text = "🕚Упс, слишком много запросов, попробуйте позже!"
        except APIBadRequest:
            text = "❌Упс, что то сломалось! Наша команда уже работает над проблемой."
        except NotFoundFLight:
            text = "⚠️Рейс не найден!"
        except APIOtherStatusHTTP:
            text = "😔Мы не располагаем информацией об этом рейсе!"

        return text

    async def _fmt(self, value):
        return value if value is not None else "Неизвестно"

    async def _fmt_dt(self, value: datetime | None):
        return value.strftime("%d.%m.%Y %H:%M") if value else "Неизвестно"

    async def _fmt_date(self, value: date | None):
        return value.strftime("%d.%m.%Y") if value else "Неизвестно"

    async def _format_flight(self, flight: Flight) -> str:
        return (
            f"✈️ Рейс: {await self._fmt(flight.number)}\n"
            f"📊 Статус: {await self._fmt(flight.status)}\n"
            f"🛩 Самолёт: {await self._fmt(flight.aircraft)}\n\n"

            f"🛫 Вылет:\n"
            f"• IATA: {await self._fmt(flight.departure_iata)}\n"
            f"• Город: {await self._fmt(flight.departure_municipality)}\n"
            f"• Запланировано (локально): {await self._fmt_dt(flight.departure_scheduledTime)}\n"
            f"• Запланировано (UTC): {await self._fmt_dt(flight.departure_scheduledTime_utc)}\n"
            f"• Изменено (локально): {await self._fmt_dt(flight.departure_revisedTime)}\n"
            f"• Изменено (UTC): {await self._fmt_dt(flight.departure_revisedTime_utc)}\n\n"

            f"🛬 Прибытие:\n"
            f"• IATA: {await self._fmt(flight.arrival_iata)}\n"
            f"• Город: {await self._fmt(flight.arrival_municipality)}\n"
            f"• Запланировано (локально): {await self._fmt_dt(flight.arrival_scheduledTime)}\n"
            f"• Запланировано (UTC): {await self._fmt_dt(flight.arrival_scheduledTime_utc)}\n"
            f"• Изменено (локально): {await self._fmt_dt(flight.arrival_revisedTime)}\n"
            f"• Изменено (UTC): {await self._fmt_dt(flight.arrival_revisedTime_utc)}\n\n"

            f"🏢 Авиакомпания: {await self._fmt(flight.airline)}\n"
            f"📅 Локальная дата: {await self._fmt_date(flight.local_date)}"
        )