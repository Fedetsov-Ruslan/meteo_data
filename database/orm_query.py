from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Weather

# функция конвертирования градусов в направление ветра. Так как от API мы получаем направление ветра в градусах
async def degrees_to_direction(deg):
    directions = [
        "Север", "Северо-восток", "Восток", "Юго-восток",
        "Юг", "Юго-запад", "Запад", "Северо-запад"
    ]
    idx = int((deg + 22.5) // 45) % 8
    return directions[idx]

# функция добавления данных в БД. Конвертируя полученные данные в нужный нам формат.
async def add_data(session: AsyncSession, data: dict):
    # В переменную rainfall записывается значение осадков, вне зависимости какие осадки. потому что тип осадков находится в переменной precipitation
    if 'rain' in data:
        rainfall = data.get('rain', {}).get('1h', 0)
    else:
        rainfall = data.get('snow', {}).get('1h', 0)
    wind_deg = await degrees_to_direction(data['wind']['deg'])
    obj = Weather(
        temperature=data['main']['temp'],
        wind_deg=wind_deg,
        wind_speed=data['wind']['speed'],
        atmospheric_pressure=data['main']['pressure'],
        precipitation=data['weather'][0]['description'],
        rainfall = rainfall
    )
    session.add(obj)
    await session.commit()

#получаем 10 последних записей из БД
async def get_data(session: AsyncSession):
    async with session.begin():
        query = select(Weather).order_by(desc(Weather.id)).limit(10)
        result = await session.execute(query)
        data = result.scalars().all()
        return data
    
    
