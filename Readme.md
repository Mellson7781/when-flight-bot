# ✈️ WhenFlight Bot

Telegram-бот для поиска информации о рейсах и получения прогноза задержек.

Бот работает через пошаговый ввод данных (FSM) и взаимодействует с локальным API для получения информации о рейсах и прогнозов задержек.

---

## 🚀 Возможности

### ✈️ `/src` — поиск рейса

Команда позволяет получить подробную информацию о рейсе.

#### Логика работы

1. Пользователь вводит `/src`
2. Бот запрашивает номер рейса
3. Бот запрашивает локальную дату рейса
4. Бот отправляет информацию о рейсе

#### API

```http
GET http://127.0.0.1:8080/api/flight/number/
```

#### Параметры запроса

| Параметр | Тип | Описание |
|----------|------|----------|
| number | str | Номер рейса |
| LocalDate | date | Локальная дата рейса |

#### Ответ API

```python
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
```

---

### 📈 `/prediction` — прогноз задержки рейса

Команда возвращает прогноз задержек и статистику по рейсу.

#### Логика работы

1. Пользователь вводит `/prediction`
2. Бот запрашивает номер рейса
3. Бот запрашивает локальную дату рейса
4. Бот отправляет прогноз задержки

#### API

```http
GET http://127.0.0.1:8080/api/flight/forecast
```

#### Параметры запроса

| Параметр | Тип | Описание |
|----------|------|----------|
| number | str | Номер рейса |
| LocalDate | date | Локальная дата рейса |

#### Ответ API

```python
class Forecast:
    chance_of_delay: StatusType
    departure_airport: AirportDelay
    arrival_airport: AirportDelay
```

---

### 📚 `/help` — справка

Показывает список доступных команд и описание их работы.

---

## 🧩 Вложенные модели

### TimeInfo

```python
class TimeInfo:
    utc: datetime
    local: datetime
```

### DelayInformation

```python
class DelayInformation:
    numTotal: int | None
    numQualifiedTotal: int | None
    numCancelled: int | None
    medianDelay: timedelta | None
    delayIndex: float
```

### AirportDelay

```python
class AirportDelay:
    airportIcao: str

    from_: TimeInfo
    to: TimeInfo

    departuresDelayInformation: DelayInformation
    arrivalsDelayInformation: DelayInformation
```

---

## 🧠 FSM (Finite State Machine)

Бот использует FSM для управления диалогами.

### Состояния

- `waiting_for_flight_number` — ожидание номера рейса
- `waiting_for_flight_date` — ожидание даты рейса

### Сценарий работы

```text
команда → номер рейса → дата → ответ → очистка состояния
```

---

## 🌐 Backend API

Бот работает с локальным backend API:

```text
http://127.0.0.1:8080/api/flight/
```

---

## 🛠 Используемые технологии

- Python 3.11+
- aiogram 3.x
- FSM (Finite State Machine)
- httpx (async)
- Pydantic v2

---

## 📁 Структура проекта

```text
handlers/
services/
models/
config.py
main.py
```

---

## ▶️ Запуск проекта

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск бота

```bash
python main.py
```

---

## 📌 Особенности

- Пошаговые сценарии ввода данных
- Асинхронные HTTP-запросы
- FSM-управление диалогами
- Работа с локальным backend API
- Валидация данных через Pydantic
- Полностью асинхронная архитектура