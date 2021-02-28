import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to tables
measurement = Base.classes.measurement
station = Base.classes.station

# Flask set up
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)

    # Query dates and precipitation
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Convert to dictionary
    all_precipitation = []
    for date, precipitation in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = precipitation
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create the session
    session = Session(engine)

    # Query dates and precipitation
    results = session.query(station.station).all()

    session.close()

    # Convert to list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create the session
    session = Session(engine)

    # Queries

    # Get most active station
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()
    
    # Get dates for most active station
    latest_date = session.query(func.max(measurement.date)).filter(measurement.station == active_stations[0]).first()
    year_ago = dt.date(2017, 8 ,18) - dt.timedelta(days=365)
    
    # Get results
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == active_stations[0], measurement.date >= year_ago, measurement.date <= latest_date[0])

    session.close()
 
    # Convert to list
    all_temp = []
    
    for date,temp in results:
        all_temp.append(temp)

    return jsonify(all_temp)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create the session
    session = Session(engine)
    
    # Find Minimum, Maximum, and Average temperatures
    results = session.query(func.min(measurement.tobs).label('min'),func.max(measurement.tobs).\
                            label('max'),func.avg(measurement.tobs).label('average')).filter(measurement.date >= start)
    
    session.close()
    
    all_stations = list(np.ravel(results[0]))

    return        (f"Since {start}:<br/>"
                   f"Minimum temperature: {all_stations[0]}<br/>"
                   f"Maximum temperature: {all_stations[1]}<br/>"
                   f"Average temperature: {all_stations[2]}")


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    # Create the session
    session = Session(engine)
    
    # Find Minimum, Maximum, and Average temperatures
    results = session.query(func.min(measurement.tobs).label('min'),func.max(measurement.tobs).\
                            label('max'),func.avg(measurement.tobs).label('average')).filter(measurement.date >= start, measurement.date <= end)
    
    session.close()
    
    all_stations = list(np.ravel(results[0]))

    return        (f"Between {start} and {end}:<br/>"
                   f"Minimum temperature: {all_stations[0]}<br/>"
                   f"Maximum temperature: {all_stations[1]}<br/>"
                   f"Average temperature: {all_stations[2]}")

if __name__ == '__main__':
    app.run(debug=True)