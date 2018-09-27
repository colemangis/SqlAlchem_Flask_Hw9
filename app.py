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
        f"/api/v1.0/date_stat</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of station precipitation values for last 365 days"""
    # Query for dates and temperature
    sel = [Measurement.date,
    Measurement.prcp]
    results = session.query(*sel).\
    filter(Measurement.date > '2016-08-23').\
    order_by (Measurement.date).all()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return list of stations"""
    sel = [Station.station,
    Station.name]
    results = session.query(*sel).all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
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

@app.route("/api/v1.0/date_stat")
def date_stat():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query for dates and min, avg, max temperature
    sel = [Measurement.date, 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)] 
    results = session.query(*sel).\
    group_by (Measurement.date).\
    sort_by (Measurement.date).all()

    # Convert list of tuples into normal list
    temp_stat = list(np.ravel(results))

    return jsonify(temp_stat)


if __name__ == '__main__':
    app.run(debug=True)
