README

### Matthew Irvin, WGU, D493 Scripting and Programming - Applications
## Python + SQLite

## ~ Weather Prediction Python Application

This is a small and useful APP that pulls historical weather for one US location and I chose one calendar day and the 
previous 5 years from that day. I chose San Diego, on Christmas day (December 24) which starts in 2024 since December 
2025 did not occur yet as I am writing this (by the time I submit this though we may be close! lol). We use this data to
compute rollups aka summary values like min, max, and average (aggregate values). We stash the results in SQLite so other
teams can take a look later and then we query the row back to prove we really landed in the DB.

## ~ What it Does ~ Quick Tour

The app calls the Open Meteo API for chosen latitude/longitude coordinates plus month/day across a 5 year span.
It computes one row to SQLite via SQLAlchemy and prints a formatted report/queries the row back to verify. Comes with 3 
unit test to verify it works (import unittest).

## ~ Requirements
Python 3.12+

Packages
requests>=2.32.5
SQLAlchemy>=2.0.43
greenlet==3.1.1
Optional - Virtual environment

## ~ Project

DATABASE.py
main.py
weather.py
test.py
requirements.txt
climate_results.db

## ~ Setup

Create and activate venv virtual environment and install dependencies

Mac/Linux
run this

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

Windows
run this

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

PyCharm is a great and allows you to create a venv as well if you chose!

## ~ Configuring your Location and Date

Inside the main.py, there is a small function called built_event() which creates the EventWeather object that tells
the program when and where to collect the weather data

Parameters of EventWeather can be edited for any coordinates you would like to know.
Parameters you can modify include Latitude (Lat), Longitude(lon), month, day, first_year. first_year is the anchor year, 
so it is currently set to 2024 and will fetch the previous 5 years from this. 

Units handled in weather.py
temperture = fahrenheit
wind = mph
precip = inches

## ~ Run the APP
python3 main.py

You will see a small report in the terminal that says five-year report for (coordinates you chose, mine are San Diego).
The average, min and max will post for the Temperature, Wind, and Precipitation for the chosen date (Mine is 12-25)

If you need a clean slate you can delete climate_results.db and run the app again "python3 main.py", and SQLite will
recreate climate_results.db. Basically it will recreate a brand new, empty databse file with the same tables just no 
data yet.

## ~ Run tests

To run the test use "python3 -m unittest test.py", and you want to see 
"Ran 3 tests in x.xxx's"
"OK"

## ~ To-Do's and important info

Make sure to install the packages required to run this app, use "python3 -m pip install -r requirements.txt", to 
install the packages.
Make sure to use python 3.12+, use "python3 -V", to check which version of python you are using.
Make sure to type in "python3", and not just "python", when running the app.
If program does not work, it could be an network issue/API hiccup, just try running again.
Too many rows after several uses? Delete climate_results.db to start fresh.

## ~ Changing time and/or location

Modify lat, lon, month, day, first_year in EventWeather located in main.py and you can run whatever day or location
you please.

## ~ References

Python Software Foundation. (n.d.). unittest — Unit testing framework. https://docs.python.org/3/library/unittest.html
Open-Meteo. (n.d.). Historical Weather API (ERA5). https://open-meteo.com/en/docs/historical-weather-api
SQLAlchemy. (n.d.). ORM quick start. https://docs.sqlalchemy.org/en/20/orm/quickstart.html