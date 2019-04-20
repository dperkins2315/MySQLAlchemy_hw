from flask import Flask,jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
# set-up DB connection

engine = create_engine("sqlite:///hawaii.sqlite",connect_args={'check_same_thread':False})
Base = automap_base()
Base.prepare(engine, reflect=True)

#build table classes

Measurement = Base.classes.measurement
Station = Base.classes.station

#initiate db session

session = Session(engine,autoflush=True)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return"""<html>
     <h1>List of all available Honolulu, HI API routes</h1>
    <ul>
    <br>
    <li>
    Return a list of precipitations from last year:
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
    <br>Replace &ltstart&gt with a date in Year-Month-Day format.
    <br>
    <a href="/api/v1.0/2017-01-01">/api/v1.0/2017-01-01</a>
    </li>
    <br>
    <li>
    Return a JSON list of tmin, tmax, tavg for the dates in range of start date and end date inclusive:
    <br>
    Replace &ltstart&gt and &ltend&gt with a date in Year-Month-Day format. 
    <br>
    <br>
    <a href="/api/v1.0/2017-01-01/2017-01-07">/api/v1.0/2017-01-01/2017-01-07</a>
    </li>
    <br>
    </ul>
    </html>
    """
@app.route("/api/v1.0/precipitation")
def precipitation():
   """Return a list of precipitations from last year"""
   # Query to retrieve the last 12 months of precipitation data and plot the results
   max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

   # Get the first element of the tuple
   max_date = max_date[0]

   # Calculate the date 1 year ago from today
   #year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
   # Perform a query to retrieve the data and precipitation scores
   #results_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
   results_precipitation = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

   # Convert list of tuples into normal list
   precipitation_dict = dict(results_precipitation)

   return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():

   """Return a JSON list of stations from the dataset."""
   # Query all stations
   results_stations = session.query(Measurement.station).group_by(Measurement.station).all()

   # Convert list of tuples into normal list
   stations_list = list(np.ravel(results_stations))

   return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

   # Design a query to retrieve the last 12 months of precipitation data and plot the results
   max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

   # Get forst element of tuple
   max_date = max_date[0]

   # The days are equal 366 so that the first day of the year is included
   year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=365)

   # Query Tobs
   results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()

   # Convert list of tuples into normal list
   tobs_list = list(results_tobs)

   return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start1_end(start=None):
   # Docstring
   """Return a JSON list of tmin, tmax, tavg for the dates in range of start date and end date inclusive"""
    
   between_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
   between_dates_list=list(between_dates)
   return jsonify(between_dates_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
   # Docstring
   """Return a JSON list of tmin, tmax, tavg for the dates in range of start date and end date inclusive"""
    
   between_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
   between_dates_list=list(between_dates)
   return jsonify(between_dates_list)


if __name__ == '__main__':
   app.run(debug=True)