import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_, or_

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///titanic.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Passenger = Base.classes.passenger
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/insert-start-date</br>"
        f"/api/v1.0/insert-start-date/insert-end-date</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of station precipitation values for last 365 days"""
    # Query for dates and temperature
    sel = [Measurement.date,
    Measurement.prcp]
    results = session.query(*sel).\
    filter(Measurement.date > '2016-08-23').\
    group_by (Measurement.date).\
    order_by (Measurement.date).all()

    # Create dictionary
    all_prcp = []
    for precip in results:
        precip_dict = {}
        precip_dict['date'] = precip.date
        precip_dict['temp'] = precip.prcp
        all_prcp.append(precip_dict)


    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return list of stations"""
    sel = [Station.name]
    results = session.query(*sel).all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/temp")
def temp():
    """Return a list of station temperatures for last 365 days"""
    # Query for dates and temperature
    sel = [Measurement.date,
    Measurement.tobs]
    results = session.query(*sel).\
    filter(Measurement.date > '2016-08-23').\
    order_by (Measurement.date).all()

    # Convert list of tuples into normal list
    temp365 = list(np.ravel(results))

    return jsonify(temp365)  

@app.route("/api/v1.0/<start>")
def date_start(start):
    """Return a min, max, avg temp greater than start date"""
    # Query for dates and min, avg, max temperature
    sel = [func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)] 
    results = session.query(*sel).\
    filter(Measurement.date > start).all()

    # Convert list of tuples into normal list
    temp_stat_start = list(np.ravel(results))

    return jsonify(temp_stat_start)

@app.route("/api/v1.0/<start>/<end>")
def date_start_end(start, end):
    """Return a min, max, avg temp greater than start date and less than end date"""
    # Query for dates and min, avg, max temperature
    sel = [func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)] 
    results = session.query(*sel).\
    filter(and_(Measurement.date > start), Measurement.date < end).all()

    # Convert list of tuples into normal list
    temp_stat_end = list(np.ravel(results))

    return jsonify(temp_stat_end)


if __name__ == '__main__':
    app.run(debug=True)
