import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt


# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# Reflect Database
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to classes
Station = Base.classes.station
Measurement = Base.classes.measurement

# Session link from Python to database
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask routes

@app.route("/")
def welcome():

    return"""<html>
    <h1>Available Routes</h1>
    <ul>
    <br>
    <li>
    Return the JSON representation of dictionary(date, prcp):
    <br>
    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
    </li>
    <br>
    <li>
    Return a JSON list of stations from the dataset: 
    <br>
   <a href="/api/v1.0/stations">/api/v1.0/stations</a>
   </li>
    <br>
    <li>
    Return a JSON list of Temperature Observations (tobs) for the previous year:
    <br>
    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
    </li>
    <br>
    <li>
    Return a JSON list of tmin, tmax, tavg for the dates greater than or equal to the date provided:
    <br>
    <a href="/api/v1.0/2017-01-01">/api/v1.0/2017-01-01</a>
    </li>
    <br>
    <li>
    Return a JSON list of tmin, tmax, tavg for the dates in range of start date and end date inclusive:
    <br>
    <a href="/api/v1.0/2017-08-09/2017-08-16">/api/v1.0/2017-08-09/2017-08-16</a>
    </li>
    <br>
    </ul>
    </html>
    """


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query to retrieve the last 12 months of precipitation data
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    max_date = max_date[0]

   # Calculate date 1 year from max date
    date_year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    # Query to get date and precipitation scores
    precip_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_year_ago).order_by(Measurement.date).all()
    
    # Convert list to dict
    precip_dict = dict(precip_scores)

    return jsonify(precip_dict)
     
@app.route("/api/v1.0/stations")
def stations(): 

    # Query stations
    stations =  session.query(Measurement.station).group_by(Measurement.station).all()

    # Convert to list
    station_list = list(np.ravel(stations))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs(): 

    # Query to retrieve the last 12 months of precipitation data
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    max_date = max_date[0]

   # Calculate date 1 year from max date
    date_year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    # Query tobs
    results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= date_year_ago).all()

    # Convert to list
    tobs_list = list(results_tobs)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start=None):

    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    start_date_list=list(start_date)
    
    return jsonify(start_date_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    
    date_range = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    date_range_list=list(date_range)
    
    return jsonify(date_range_list)


if __name__ == '__main__':
    app.run(debug=True)