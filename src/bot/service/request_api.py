import httpx

from datetime import date

from bot.error.api import APIBadRequest, NotFoundFLight, LittelDate, ManyRequestAPI, APIOtherStatusHTTP
from bot.schemas.flight import Flight, Forescast


class InternalAPI:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_data_flight(self, number: str, localDate: date) -> Flight:
        URL = "http://127.0.0.1:8080/api/filght/searech/number"
        params = {
            "number": number,
            "LocalDate": localDate
        }
        try:
            response = await self.client.get(URL, params=params)
            response.raise_for_status()
        except httpx.RequestError:
            raise APIBadRequest()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise NotFoundFLight()
            elif e.response.status_code == 400:
                raise LittelDate()
            elif e.response.status_code == 429:
                raise ManyRequestAPI()
            else:
                raise APIOtherStatusHTTP()

        result_api = response.json()
        flight = Flight.model_validate(result_api)
        
        return flight
    
    async def get_data_prediction(self, number: str, localDate: date) -> Forescast:
        URL = "http://127.0.0.1:8080/api/filght/forecast"
        params = {
            "number": number,
            "LocalDate": localDate
        }
        try:
            response = await self.client.get(URL, params=params)
            response.raise_for_status()
        except httpx.RequestError:
            raise APIBadRequest()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise NotFoundFLight()
            elif e.response.status_code == 400:
                raise LittelDate()
            elif e.response.status_code == 429:
                raise ManyRequestAPI()
            else:
                raise APIOtherStatusHTTP()

        result_api = response.json()
        prediction = Forescast(**result_api)
        
        return prediction