# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
    return (f"Available routes<br/>"
            f"/api/v1.0/precipitation : list dates and precipitation"
            f"/api/v1.0/stations : list all stations from dataset"
            f"/api/v1.0/tobs : list dates and temperature from a year from the last data point (2017-08-23)"
            f"/api/v1.0/startdate : show min, average and max temperature after specified start date"
            f"/api/v1.0/startdate/enddate : show min, average and max temperature between specified start and end date"
            f"Start and end date should be formatted as 'YYYY-MM-DD'")









