import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

# flask setup
app = Flask(__name__)

# flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a query of the last 12 months of precipitation data"""
    date = dt.datetime(2016,8,23)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= date).all()

    # make a dictionary
    prcp_list =[]
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations
    results = session.query(Measurement.station,func.count(Measurement.tobs)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.tobs).desc()).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def stations():
    """Return a list of tobs over the last 12 months"""
    # Query
    date = dt.datetime(2016,8,23)
    temp_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= date).all()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(temp_data))

    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)

