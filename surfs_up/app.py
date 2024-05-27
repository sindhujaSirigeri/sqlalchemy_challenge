# Import the dependencies.

from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import pandas as pd

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create a session


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# Home page. List all routes that are available.
@app.route("/")
def home():
    return (f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
            )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    # Query the last 12 months of precipitation data
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()
    dict_prcp = dict(prcp_data)
    session.close()
    return jsonify(dict_prcp)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    # Query all stations
    stations = session.query(Station.station).all()
    
    session.close()
    
    # Convert the query results to a list
    stations_list = [station[0] for station in stations]
    
    return jsonify(stations_list)


# Define the temperature observations route for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    # Get the most active station ID
    most_active_station = session.query(Measurement.station)\
                                 .group_by(Measurement.station)\
                                 .order_by(func.count(Measurement.station).desc())\
                                 .first().station
    
    # Query the last 12 months of temperature observation data for the most active station
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    one_year_ago = pd.to_datetime(latest_date) - pd.DateOffset(years=1)
    temperature_data = session.query(Measurement.date, Measurement.tobs)\
                              .filter(Measurement.station == most_active_station)\
                              .filter(Measurement.date >= one_year_ago.strftime('%Y-%m-%d')).all()
    
    session.close()
    
    # Convert the query results to a list
    temperature_list = [tobs for date, tobs in temperature_data]
    
    return jsonify(temperature_list)


# Define the route for temperature stats from a start date
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    session = Session(engine)
    
    # If no end date is provided, calculate stats for dates greater than or equal to the start date
    if not end:
        results = session.query(func.min(Measurement.tobs),
                                func.avg(Measurement.tobs),
                                func.max(Measurement.tobs))\
                         .filter(Measurement.date >= start).all()
    else:
        # Calculate stats for dates between the start and end date, inclusive
        results = session.query(func.min(Measurement.tobs),
                                func.avg(Measurement.tobs),
                                func.max(Measurement.tobs))\
                         .filter(Measurement.date >= start)\
                         .filter(Measurement.date <= end).all()
    
    session.close()
    
    # Convert the query results to a list
    temperature_stats_list = list(results[0])
    
    return jsonify(temperature_stats_list)



if __name__ == '__main__':
    app.run(debug=True)
