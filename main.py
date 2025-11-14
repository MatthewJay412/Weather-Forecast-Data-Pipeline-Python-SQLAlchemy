# Matthew Irvin, WGU, D493 Scripting and Programming Applications
# main.py
from weather import EventWeather
from DATABASE import DBSession, init_db, Weather

init_db()

def build_event() -> EventWeather:
    # My location is San Diego on December 25, 2025 (christmas day)
    # The latitude is 32.7157 and the longitude is -117.1647
    return EventWeather(
        lat=32.7157, # latitude coordinates for San Diego, pulled from METEO API
        lon=-117.1647, # longitude coordinates for San Diego, pulled from METEO API
        month=12, # month = December
        day=25, # The 25th
        first_year=2024  #2024 is the "first year" and we will query 2024, 2023, 2022, 2021, and 2020
    )

# This is the main app's entry point which prints a simple report of averages
# mins, max's
if __name__ == "__main__":
    event = build_event()
    event.five_year_summary()
    print(f"Five-year Report for {event.lat},{event.lon} on {event.month:02d}-{event.day:02d}")
    print(f"Temperature [Fahrenheit]: avg={event.t_avg_f}, min={event.t_min_f}, max={event.t_max_f}")
    print(f"Wind [mph]: avg={event.wind_avg_mph}, min={event.wind_min_mph}, max={event.wind_max_mph}")
    print(f"Precipitation [inches]: sum={event.precip_sum_in}, min={event.precip_min_in}, max={event.precip_max_in}")

    # C5 insert one row into SQLite
    # We take numbers pulled from API stored in EventWeather object and
    # pack them into a Weather row that matches the table schema.
    row = Weather(
        lat=event.lat,
        long=event.lon,
        month=event.month,
        day=event.day,
        yr=event.first_year,
        five_year_avg_temp_f=event.t_avg_f,
        five_year_min_temp_f=event.t_min_f,
        five_year_max_temp_f=event.t_max_f,
        five_year_avg_wind_mph=event.wind_avg_mph,
        five_year_min_wind_mph=event.wind_min_mph,
        five_year_max_wind_mph=event.wind_max_mph,
        five_year_sum_precip_inches=event.precip_sum_in,
        five_year_min_precip_inches=event.precip_min_in,
        five_year_max_precip_inches=event.precip_max_in,
    )
    # DBSession will handle the conversation with SQLite, named DBSessions as x
    # We drop the new row in, commit, and data is saved
    with DBSession() as x:
        x.add(row)
        x.commit()
        print(f"Inserted Weather row id={row.id_number}")
    # C6 Query back the data we just stored
    # This is a way to double check myself, new session, pull the rows, and
    # print them nicely for a screenshot
    with DBSession() as x:
        results = x.query(Weather).all()
        for r in results:
            print(
                f"DB Row → id={r.id_number}, "
                f"lat={r.lat}, long={r.long}, "
                f"date={r.month:02d}-{r.day:02d}-{r.yr}, "
                f"temp_avg={r.five_year_avg_temp_f}, "
                f"wind_avg={r.five_year_avg_wind_mph}, "
                f"precip_total={r.five_year_sum_precip_inches}"
            )


