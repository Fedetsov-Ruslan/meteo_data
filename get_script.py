import os
import requests
import asyncio

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import  AsyncSession

from database.orm_query import add_data
from database.engine import session_maker, create_db

load_dotenv()

WEATHER_KEY=os.getenv("WEATHER_KEY")
INTERVAL = int(os.getenv("INTERVAL"))

# запрос данных погоды через API openweathermap по координатам Сколтеха и добавление в БД через ORM
async def get_weather(session: AsyncSession):
    lat = 55.6985
    lon = 37.3595
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric', 
        'lang': 'ru',       
        'appid': WEATHER_KEY    
    }
    url = "http://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=params).json()
    await add_data(session=session, data=response)

# запуск программы и создание БД если её не существует
async def main():
    await create_db()
    while True:
        await get_weather(session=session_maker())
        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
