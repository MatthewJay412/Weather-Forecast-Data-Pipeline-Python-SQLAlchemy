# Matthew Irvin, WGU, D493 Scripting and Programming Applications
# weather.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict
import requests
from datetime import date
from urllib.parse import urlencode

# API URL
OPEN_METEO = "https://archive-api.open-meteo.com/v1/era5"

# Wait 20 seconds for a reply from the sever until give up
_DEFAULT_TIMEOUT = 20
# User agent so the server knows why we are trying to access it
_HEADERS = {"User-Agent": "WGU Student Project"}

@dataclass
class EventWeather:
    """
    Holds weather data for one location and one calendar day
    Fetches the past 5 years from the API and summarizes the temperature, wind and precipitation
    The results are stored as attributes for later use
    """

    # C1: coordinates of location
    lat: float
    lon: float
    month: int
    day: int
    first_year: int  # most recent year in the five year window

    # Five-year rollups
    t_avg_f: Optional[float] = None
    t_min_f: Optional[float] = None
    t_max_f: Optional[float] = None

    wind_avg_mph: Optional[float] = None
    wind_min_mph: Optional[float] = None
    wind_max_mph: Optional[float] = None

    precip_sum_in: Optional[float] = None
    precip_min_in: Optional[float] = None
    precip_max_in: Optional[float] = None

    # Stops bad inputs, for example: day = 45. For future use of program if we change
    # location/coordinates in main.py
    def __post_init__(self):
        if not (-90 <= self.lat <= 90 and -180 <= self.lon <= 180):
            raise ValueError("Latitude/Longitude OUT OF RANGE.")
        if not (1 <= self.month <= 12 and 1 <= self.day <= 31):
            raise ValueError("Month/day OUT OF RANGE.")

    # C2 : fetches 5 years, crunches numbers, and save them on the object
    def five_year_summary(self) -> None:
        """
        Shortcut instead of calling temp, wind and precipitation one by one we just grab the same day across 5 years in
        a single loop. It collects daily temp, wind, and precipitation from the API and calculates the 5 year average,
        min, and max. Stores values on this object for the Database later.
        """
        temp: List[float] = []
        wind: List[float] = []
        precipitate: List[float] = []

        for year in range(self.first_year, self.first_year - 5, -1):
            daily = self._get_day(year)
            temp.append(daily["temperature_2m_mean"])
            wind.append(daily["wind_speed_10m_max"])
            precipitate.append(daily["precipitation_sum"])
            # Loop from anchor year back 5 years.

        # Five year summary for Temperature (Fahrenheit)
        self.t_avg_f = round(sum(temp) / len(temp), 2)
        self.t_min_f = round(min(temp), 2)
        self.t_max_f = round(max(temp), 2)

        # Five year summary for Wind (MPH)
        self.wind_avg_mph = round(sum(wind) / len(wind), 2)
        self.wind_min_mph = round(min(wind), 2)
        self.wind_max_mph = round(max(wind), 2)

        # Five year summary for Precipitation (inches)
        self.precip_sum_in = round(sum(precipitate), 2)
        self.precip_min_in = round(min(precipitate), 2)
        self.precip_max_in = round(max(precipitate), 2)

    def get_mean_temperature_f(self, year: int) -> float:
        return self._get_day(year)["temperature_2m_mean"]

    def get_max_wind_mph(self, year: int) -> float:
        return self._get_day(year)["wind_speed_10m_max"]

    def get_precip_sum_in(self, year: int) -> float:
        return self._get_day(year)["precipitation_sum"]

    # Helper, to fetch one exact calendar day for a given year
    def _get_day(self, year: int) -> Dict[str, float]:
        day_str = date(year, self.month, self.day).isoformat()

        # Build exact query string for 1 day
        query = {
            "latitude": self.lat,
            "longitude": self.lon,
            "start_date": day_str,
            "end_date": day_str,
            "daily": "temperature_2m_mean,wind_speed_10m_max,precipitation_sum",
            "temperature_unit": "fahrenheit",
            "windspeed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
        }
        full_url = f"{OPEN_METEO}?{urlencode(query)}"

        # Make API call and get the data back
        resp = requests.get(full_url, headers=_HEADERS, timeout=_DEFAULT_TIMEOUT)
        resp.raise_for_status()
        payload = resp.json()

        daily = payload.get("daily", {})
        if not daily or not daily.get("time"):
            raise ValueError(f"No daily data returned for {day_str} at {self.lat},{self.lon}")

        def first(key: str) -> float:
            vals = daily.get(key)
            if not vals or vals[0] is None:
                raise ValueError(f"Missing {key} for {day_str}")
            return float(vals[0])

        return {
            "temperature_2m_mean": first("temperature_2m_mean"),
            "wind_speed_10m_max": first("wind_speed_10m_max"),
            "precipitation_sum": first("precipitation_sum"),
        }

