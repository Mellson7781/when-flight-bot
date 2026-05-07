# ✈️ WhenFlight Bot

Telegram-бот для поиска информации о рейсах и получения прогноза задержек.

Бот работает через пошаговый ввод данных (FSM) и обращается к локальному API для получения информации о рейсах и прогнозах.

---

## 🚀 Возможности

### ✈️ `/src` — поиск рейса

Команда позволяет получить подробную информацию о рейсе.

**Логика:**
1. Ввод `/src`
2. Ввод номера рейса
3. Ввод локальной даты
4. Получение информации о рейсе

**API:**

GET http://127.0.0.1:8080/api/flight/number/


---

### 📈 `/prediction` — прогноз рейса

Команда возвращает прогноз задержек и статистику по рейсу.

**Логика:**
1. Ввод `/prediction`
2. Ввод номера рейса
3. Ввод локальной даты
4. Получение прогноза

**API:**

GET http://127.0.0.1:8080/api/flight/forecast


---

### 📚 `/help` — справка

Показывает список доступных команд и описание их работы.

---

## 🧠 Логика работы (FSM)

Бот использует Finite State Machine:

- `waiting_for_flight_number` — ожидание номера рейса
- `waiting_for_flight_date` — ожидание даты рейса

Каждый сценарий:

команда → номер рейса → дата → ответ → очистка состояния


---

## 🌐 API

Бот работает с локальным backend:


http://127.0.0.1:8080/api/flight/


---

## ✈️ Flight search (/src)


GET /number/


### Параметры:

| name      | type | description     |
|----------|------|-----------------|
| number   | str  | номер рейса      |
| LocalDate| date | локальная дата   |

### Ответ:

class Flight:
    number: str
    status: str | None
    aircraft: str | None

    departure_iata: str | None
    departure_scheduledTime: datetime
    departure_scheduledTime_utc: datetime
    departure_municipality: str | None
    departure_revisedTime: datetime | None
    departure_revisedTime_utc: datetime | None

    arrival_iata: str | None
    arrival_scheduledTime: datetime
    arrival_scheduledTime_utc: datetime
    arrival_municipality: str | None
    arrival_revisedTime: datetime | None
    arrival_revisedTime_utc: datetime | None

    airline: str | None
    local_date: date | None

📈 Flight forecast (/prediction)
GET /forecast
Параметры:
name	type	description
number	str	номер рейса
LocalDate	date	локальная дата

Ответ:
class Forescast:
    chance_of_delay: StatusType
    departure_airoport: AiroportDelay
    arrival_airoport: AiroportDelay
🧩 Вложенные модели

TimeInfo
class TimeInfo:
    utc: datetime
    local: datetime

DelayInformation
class DelayInformation:
    numTotal: int | None
    numQualifiedTotal: int | None
    numCancelled: int | None
    medianDelay: timedelta | None
    delayIndex: float

AiroportDelay
class AiroportDelay:
    airportIcao: str
    from_: TimeInfo
    to: TimeInfo

    departuresDelayInformation: DelayInformation
    arrivalsDelayInformation: DelayInformation


###🛠 Технологии:
Python 3.11+
aiogram 3.x
FSM (Finite State Machine)
httpx (async)
Pydantic v2
📁 Структура
handlers/
services/
models/
config.py
main.py
▶️ Запуск
pip install -r requirements.txt
python main.py
📌 Особенности
Двухшаговые сценарии (номер → дата)
Асинхронные HTTP запросы
FSM управление диалогами
Локальный API backend