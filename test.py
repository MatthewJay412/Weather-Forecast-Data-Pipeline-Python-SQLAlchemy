# test.py
# Section D
# Unit testing, 3 quick tests to run against my code
# Tests were structured with help from the official unittest document
# https://docs.python.org/3/library/unittest.html
# To run test (python3 -m unittest test.py)

import unittest # what we use to test our code
from weather import EventWeather # app code, pulls the weather and summerizes
from DATABASE import init_db, DBSession, Weather

class WeatherTester(unittest.TestCase):

# Set up location and date(San Diego, December 25th 2024, this runs before every test
    def setUp(self):
        self.event = EventWeather(
            lat=32.7157,
            lon=-117.1647,
            month=12,
            day=25,
            first_year=2024 # Anchor year, so 2024 and 5 years back from this
        )
        init_db() # Creates a table if needed

    # Test 1: Make sure API method returns a float
    def test_verify_temp_is_float(self):
        value = self.event.get_mean_temperature_f(2024)
        self.assertIsInstance(value, float)

    # Test 2: Ensure average is between min and max
    def test_check_five_yr_summary(self):
        self.event.five_year_summary()
        self.assertGreaterEqual(self.event.t_avg_f, self.event.t_min_f)
        self.assertLessEqual(self.event.t_avg_f, self.event.t_max_f)

    # Test 3: Check DB insert/query works
    def test_verify_database_insert(self):
        self.event.five_year_summary()
        row = Weather(
            lat=self.event.lat,
            long=self.event.lon,
            month=self.event.month,
            day=self.event.day,
            yr=self.event.first_year,
            five_year_avg_temp_f=self.event.t_avg_f,
            five_year_min_temp_f=self.event.t_min_f,
            five_year_max_temp_f=self.event.t_max_f,
            five_year_avg_wind_mph=self.event.wind_avg_mph,
            five_year_min_wind_mph=self.event.wind_min_mph,
            five_year_max_wind_mph=self.event.wind_max_mph,
            five_year_sum_precip_inches=self.event.precip_sum_in,
            five_year_min_precip_inches=self.event.precip_min_in,
            five_year_max_precip_inches=self.event.precip_max_in,
        )
        # Open a fresh DB session, add a row, commit to save and run query to confirm
        # you can read it back
        with DBSession() as session:
            session.add(row)
            session.commit()
            results = session.query(Weather).all()
            # Not to validate exact numbers, we just assert there is atleast one row
            # present after insert/commit
            self.assertGreaterEqual(len(results), 1)

if __name__ == "__main__":
    unittest.main()
