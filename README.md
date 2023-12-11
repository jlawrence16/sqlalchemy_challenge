# sqlalchemy_challenge

In this project, I was taked with analysing the climate of Hawaii using SQLAlchemy ORM queries, Pandas abd Matplotlib. I then designed a Flask API based on the queries developed above.

# Part 1: Analyze and Explore the Climate Data

Used the SQLAlchemy create_engine() function to connect to the SQLite database.

Used the SQLAlchemy automap_base() function to reflect the tables into classes, and then save references to the classes named station and measurement.

Link Python to the database by creating a SQLAlchemy session.

Precipitation Analysis
Find the most recent date in the dataset. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data. Plot the results by using the DataFrame plot method, print summary stats using Pandas.

Station Analysis

Design a query to calculate the total number of stations in the dataset.
Design a query to find the most-active stations (that is, the stations that have the most rows).
Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id.
Design a query to get the previous 12 months of temperature observation (TOBS) data and plot as a histogram.


# Part 2: Design the Climate App

Creat a Flas API with the following routes

/
List all the available routes.

/api/v1.0/precipitation
Return JSON representation of query results from precipitation analysis

/api/v1.0/stations
Return a JSON list of stations from the dataset.

/api/v1.0/tobs
Return a JSON list of temperature observations from the most-active station over the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>
Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.