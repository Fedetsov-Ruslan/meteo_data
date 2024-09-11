import pandas as pd
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.orm_query import get_data

# функция для экспорта данных в эксель
async def export_to_excels(session: AsyncSession):
    data = await get_data(session)
    data_list =[
        {
            'id': row.id,
            'temperature': row.temperature,
            'wind_deg': row.wind_deg,
            'wind_speed': row.wind_speed,
            'atmospheric_pressure': row.atmospheric_pressure,
            'precipitation': row.precipitation,
            'rainfall': row.rainfall,
            'date_time': row.created
        }
        for row in data
    ]   
    df = pd.DataFrame(data_list, columns=['id', 'temperature', 'wind_deg', 'wind_speed', 'atmospheric_pressure', 'precipitation', 'rainfall', 'date_time'])
    df.to_excel("weather_data.xlsx", index=False)

# запуск скрипта
async def main():
    await export_to_excels(session=session_maker())
    

if __name__ == "__main__":
    asyncio.run(main())
