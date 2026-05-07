from datetime import date, datetime, timedelta
from bot.service.request_api import InternalAPI
from bot.error.api import ManyRequestAPI, APIBadRequest, APIOtherStatusHTTP, NotFoundFLight, LittelDate


class PredictionService:
    def __init__(self, api: InternalAPI):
        self.api = api

    async def prediction(self, number: str, date: date) -> str:
        try:
            prediction = await self.api.get_data_prediction(number, date)
            text = await self._format_forecast(prediction)
        except ManyRequestAPI:
            text = "🕚Упс, слишком много запросов, попробуйте позже!"
        except APIBadRequest:
            text = "❌Упс, что то сломалось! Наша команда уже работает над проблемой."
        except NotFoundFLight:
            text = "⚠️Рейс не найден!"
        except APIOtherStatusHTTP:
            text = "😔Мы не располагаем информацией об этом рейсе!"
        except LittelDate:
            text = "⚠️Пока не получается сделать прогноз. Слишком мало данных"

        return text

    async def _fmt(self, v):
        return v if v is not None else "Неизвестно"


    async def _fmt_dt(self, dt: datetime | None):
        return dt.strftime("%d.%m.%Y %H:%M") if dt else "Неизвестно"


    async def _fmt_td(self, td: timedelta | None):
        if td is None:
            return "Неизвестно"

        total_seconds = int(td.total_seconds())

        sign = "-" if total_seconds < 0 else ""
        total_seconds = abs(total_seconds)

        minutes = total_seconds // 60
        hours = minutes // 60
        minutes = minutes % 60

        if hours:
            return f"{sign}{hours} ч {minutes} мин"
        return f"{sign}{minutes} мин"


    async def _format_delay_info(self, title: str, d):
        return (
            f"{title}\n"
            f"• Всего рейсов: {await self._fmt(d.numTotal)}\n"
            f"• Подтверждённых: {await self._fmt(d.numQualifiedTotal)}\n"
            f"• Отменённых: {await self._fmt(d.numCancelled)}\n"
            f"• Средняя задержка: {await self._fmt_td(d.medianDelay)}\n"
            f"• Индекс задержек: {await self._fmt(d.delayIndex)}\n"
        )


    async def _format_airport_delay(self, title: str, a):
        return (
            f"{title}\n"
            f"🛫 ICAO: {await self._fmt(a.airportIcao)}\n\n"

            f"⏱ Период:\n"
            f"• С: {await self._fmt_dt(a.from_.utc)} (UTC) / {await self._fmt_dt(a.from_.local)} (локально)\n"
            f"• До: {await self._fmt_dt(a.to.utc)} (UTC) / {await self._fmt_dt(a.to.local)} (локально)\n\n"

            f"{await self._format_delay_info('📊 Вылеты:', a.departuresDelayInformation)}\n"
            f"{await self._format_delay_info('📊 Прилёты:', a.arrivalsDelayInformation)}"
        )


    async def _format_forecast(self, f):
        status_map = {
            "low": "🟢 Низкий",
            "medium": "🟡 Средний",
            "high": "🔴 Высокий"
        }

        status = status_map.get(f.chance_of_delay.value, "Неизвестно")

        return (
            f"🌤 Прогноз задержек рейсов\n\n"
            f"⚠️ Шанс задержек: {status}\n\n"
            f"{await self._format_airport_delay('🏢 Аэропорт вылета:', f.departure_airoport)}\n\n"
            f"{await self._format_airport_delay('🏁 Аэропорт прибытия:', f.arrival_airoport)}"
        )