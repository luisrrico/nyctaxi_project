# Databricks notebook source
import urllib.request
import shutil
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta

# COMMAND ----------

# Get current date
today = datetime.today()

# Calculate start month (current month - 3 months)
start_month = today - relativedelta(months=3)

# Generate the last 6 months from start_month going backwards
dates_to_process = [
    (start_month - relativedelta(months=i)).strftime("%Y-%m")
    for i in range(6)
]

# Optional: sort from oldest to most recent
dates_to_process = sorted(dates_to_process)

print(dates_to_process)

# COMMAND ----------

for date in dates_to_process:
    
    # Construct the URL for the Parquet file corresponding to this month
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{date}.parquet"

    # Open a connection and stream the remote file
    response = urllib.request.urlopen(url)

    # Define and create the local directory for this date's data
    dir_path = f"/Volumes/nyctaxi/00_landing/data_sources/nyctaxi_yellow/{date}"
    os.makedirs(dir_path, exist_ok=True)

    # Define the full path for the downloaded file
    local_path = f"{dir_path}/yellow_tripdata_{date}.parquet"

    # Save the streamed content to the local file in binary mode
    with open(local_path, 'wb') as f:
        shutil.copyfileobj(response, f)  # Copy data from response to file