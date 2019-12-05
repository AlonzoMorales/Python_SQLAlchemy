# Python_SQLAlchemy

### Climate Analysis and Exploration
Analyse Sqlite file with climate data using SQLAlchemy ORM queries, Pandas, and Matplotlib.

#### Precipitation Analysis
* Design a query to retrieve 12 months of precipitation data.
* Load the query results into a Pandas DataFrame and set the index to the date column.
* Sort the DataFrame values by date.
* Plot the results using the DataFrame plot method.
* Use Pandas to print the summary statistics for the precipitation data.

#### Station Analysis
* Design a query to calculate the total number of stations.
* Design a query to find the most active stations.
  * List the stations and observation counts in descending order.
  * List the station that has the highest number of observations.
* Design a query to retrieve 12 months of temperature observation data.
  * Filter by the station with the highest number of observations.
  * Plot the results as a histogram.

#### Temperature Analysis
* Calculate and plot the min, avg, and max temperature from chosen date range as a bar chart.
  * Use the average temperature as the bar height.
  * Use the peak-to-peak value as the y error bar.

![precip](Precipitation.PNG)

![temp](Temp.PNG)

![avgtemp](Trip_avg_temp.PNG)
