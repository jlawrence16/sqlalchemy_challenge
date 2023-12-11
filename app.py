# Import the dependencies.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import numpy as np
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################

engine = create_engine(r"sqlite:///C:/Users\tamhl\OneDrive\Documents\Bootcamp\sqlalchemy_challenge\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
    """List all available api routes.<br/>"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        f"Please enter all dates in format YYYY-MM-DD"
    )

# Return JSON list of dates & precipitation values from last 12 months.  
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Get dates to filter by last 12 months 
    
        # Get dates to filter by last 12 months    
    recent_date = session.query(func.max(Measurement.date)).first()
    recent_date=str(recent_date).\
    replace(',', '').\
    replace('(', '').\
    replace(')', '').\
    replace("'", '')
    
    recent_date = dt.strptime(recent_date, '%Y-%m-%d').date()
    previous_year = recent_date - relativedelta(years=1)
    
    # Query date and percipitation values from last 12 months
    recent_precip = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date < recent_date).\
                    filter(Measurement.date > previous_year).all()

    
    session.close()

    # Convert list of tuples into normal list and return
    precip_list = list(np.ravel(recent_precip))

    return jsonify(precip_list)

# Return JSON list of stations
@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    # Query stations
    
    stations = session.query(Measurement.station.distinct()).all()
    
    session.close()

    # Convert list of tuples into normal list and return
    station_list = list(np.ravel(stations))

    return jsonify(station_list)


# Return a JSON list of temperature observations from most active station for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Find most active station
    active_station = session.query(Measurement.station, func.count(Measurement.prcp)).\
                            group_by(Measurement.station).\
                            order_by(func.count(Measurement.prcp).desc()).\
                            all()
                            
    most_active_id = active_station[0]
    most_active_id = most_active_id[0]
    
    # Get dates to filter by last 12 months    
    recent_date = session.query(func.max(Measurement.date)).first()
    recent_date=str(recent_date).\
    replace(',', '').\
    replace('(', '').\
    replace(')', '').\
    replace("'", '')
    
    recent_date = dt.strptime(recent_date, '%Y-%m-%d').date()
    previous_year = recent_date - relativedelta(years=1)
 
    # Query date & temperature values from most active station over last 12 months
    temps =session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == most_active_id).\
                filter(Measurement.date <= recent_date).\
                filter(Measurement.date >= previous_year).all()
    
    session.close()

    # Convert list of tuples into normal list and return
    temps_list = list(np.ravel(temps))

    return jsonify(temps_list)


# Return a JSON list of the minimum temperature, the average temperature, and the 
# maximum temperature for a specified start date

@app.route("/api/v1.0/<string:start>")
def summary_temp_start(start):

    #Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Calculate most recent date  
    recent_date = session.query(func.max(Measurement.date)).first()
    recent_date=str(recent_date).\
    replace(',', '').\
    replace('(', '').\
    replace(')', '').\
    replace("'", '')
    
    recent_date = dt.strptime(recent_date, '%Y-%m-%d').date()
    
    #Query min, avg, max temperature values from start date specified
    summary_temps_start =session.query(func.min(Measurement.tobs),
                                 func.avg(Measurement.tobs),
                                 func.max(Measurement.tobs)).\
                filter(Measurement.date < recent_date).\
                filter(Measurement.date > start).all()
    
    session.close()

    # Convert list of tuples into normal list and return
    summary_temps_start_list = list(np.ravel(summary_temps_start))

    return jsonify(summary_temps_start_list)


# Return a JSON list of the minimum temperature, the average temperature, and the 
# maximum temperature for a specified start and end date

@app.route("/api/v1.0/<string:start>/<string:end>")
def summary_temp_startend(start, end):
        
    #Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Query min, avg, max temperature values from start date specified
    summary_temps =session.query(func.min(Measurement.tobs),
                                 func.avg(Measurement.tobs),
                                 func.max(Measurement.tobs)).\
                filter(Measurement.date < end).\
                filter(Measurement.date > start).all()
    
    session.close()

    # Convert list of tuples into normal list and return
    summary_temps_list = list(np.ravel(summary_temps))

    return jsonify(summary_temps_list)
    
if __name__ == '__main__':
    app.run(debug=True)