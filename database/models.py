from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, String, func, Float


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Weather(Base):
    __tablename__ = "weather"
    id: Mapped[int] = mapped_column(primary_key=True)
    temperature: Mapped[float] = mapped_column(Float)
    wind_deg: Mapped[str] = mapped_column(String(255))
    wind_speed: Mapped[float] = mapped_column(Float)
    atmospheric_pressure: Mapped[float] = mapped_column(Float)
    precipitation: Mapped[str] = mapped_column(String(255))
    rainfall: Mapped[float] = mapped_column(Float)