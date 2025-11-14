# Matthew Irvin, WGU, D493 Scripting and Programming Applications
# DATABASE.py

from __future__ import annotations
from sqlalchemy import create_engine, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# This line spins up the database engine, if we did not have this SQlite would create one
database_engine = create_engine("sqlite:///climate_results.db", echo=False, future=True)

# Base is what every table class will lean on and keeps everything wired into SQLAlchemy.
class Base(DeclarativeBase):
    pass

# This is the blueprint for a table called "Weather" and each field down below becomes a column for that table
class Weather(Base):
    __tablename__ = "Weather"

    # Every row gets designated a unique ID (primary key) and autoincrements
    id_number: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Location and date details, latitude, longitude, month, day, and anchor year.
    lat:  Mapped[float] = mapped_column(Float, nullable=False)
    long: Mapped[float] = mapped_column(Float, nullable=False)
    month:     Mapped[int]   = mapped_column(Integer, nullable=False)
    day:       Mapped[int]   = mapped_column(Integer, nullable=False)
    yr:      Mapped[int]   = mapped_column(Integer, nullable=False)

    # Five-year temperature (°F)
    five_year_avg_temp_f: Mapped[float] = mapped_column(Float, nullable=False)
    five_year_min_temp_f: Mapped[float] = mapped_column(Float, nullable=False)
    five_year_max_temp_f: Mapped[float] = mapped_column(Float, nullable=False)

    # Five-year wind (mph)
    five_year_avg_wind_mph: Mapped[float] = mapped_column(Float, nullable=False)
    five_year_min_wind_mph: Mapped[float] = mapped_column(Float, nullable=False)
    five_year_max_wind_mph: Mapped[float] = mapped_column(Float, nullable=False)

    # Five-year precipitation (in)
    five_year_sum_precip_inches: Mapped[float] = mapped_column(Float, nullable=False)
    five_year_min_precip_inches: Mapped[float] = mapped_column(Float, nullable=False)
    five_year_max_precip_inches: Mapped[float] = mapped_column(Float, nullable=False)

    # A way to make rows print nicely in logs and saves you from staring at raw object IDs
    def __repr__(self) -> str:
        return (f"<Weather id={self.id_number} "
                f"lat={self.lat} long={self.long} "
                f"date={self.month:02d}-{self.day:02d}-{self.yr}>")

# The tool we will use to open and close conversations with the database
DBSession = sessionmaker(bind=database_engine, autoflush=False, autocommit=False, future=True)

def init_db() -> None:
    # Create table in SQLite if it is missing and if it's already there, nothing breaks and it just keeps going
    Base.metadata.create_all(database_engine)
if __name__ == "__main__":
    Base.metadata.create_all(database_engine)
