# SQLalchemy Challenge

This code is divided in two parts. Part 1 is a jupyter notebook with Hawaii's precipitation and temperature analysis, where SQLalchemy is used to do hawaii.sqlite queries. Part 2 consists on a python script that creates a Flask API based on the queries previously developed on the jupyter notebook.

## Part 1

With SQLalchemy, we create an engine to hawaii.sqlite, then reflect the existing database into a new model, and then start the session. Initially filtering by dates, precipitation's data of each station is gathered and plotted using Pandas. Next, the most active station's data is used to make a histogram. It uses all the temperatures measured during the last 12 months, the data is also used to find the lowest, highest, and average temperatures.    

## Part 2

With Flask and SQLalchemy, this script creates an API that performs queries to hawayy.sqlite and returns the data in JSON format. 

The API has 5 routes:
- /api/v1.0/precipitation
- /api/v1.0/stations
- /api/v1.0/tobs
- /api/v1.0/start
- /api/v1.0/start/end

Where start and end are variables that the user can modify to select the dates where the data is taken.
