import quandl
import sys
import signal
import time
import ctypes
import ctypes.util
from prometheus_client import start_http_server, Gauge, Summary
from datetime import datetime

# -----------------------------------------------------------------------------
# This script grabs a dataset from quandl and imports it into a Prometheus TSDB
# -----------------------------------------------------------------------------

# Allow the program to be shut down gracefully
def sigtermHandler(signum, frame):
  sys.exit(0)

# Convert timestamps within the dataset into epoch format
def datetimeToTimestamp(dt):
  return (datetime.combine(dt, datetime.min.time()) - datetime(1970,1,1)).total_seconds()

if __name__ == '__main__':
  signal.signal(signal.SIGINT, sigtermHandler)
  signal.signal(signal.SIGTERM, sigtermHandler)

  # Authenticate the quandl queries using my API key
  quandl.ApiConfig.api_key = 'zq98P1dzTAXQnMYJFjUG'

  # Get tables for a few properties in the Federal Reserve Economic Data dataset
  nroust  = quandl.get('FRED/NROUST')        # Natural Rate of Unemployment (Short-Term)
  gdppot  = quandl.get('FRED/GDPPOT')        # Real Potential Gross Domestic Product
  ngdppot = quandl.get('FRED/NGDPPOT')       # Nominal Potential Gross Domestic Product
  nrou    = quandl.get('FRED/NROU')          # Natural Rate of Unemployment (Long-Term)
  ggnlbp  = quandl.get('FRED/GGNLBPUSA188N') # Projection of General gov't net lending/borrowing

  # Set up Prometheus metrics for the above tables
  nroustGauge  = Gauge('fred_nrou_st_val', 'Natural Rate of Unemployment (Short-Term)')
  nroustSum    = Summary('fred_nrou_st', 'Natural Rate of Unemployment (Short-Term)')
  gdppotGauge  = Gauge('fred_gdp_pot_val', 'Real Potential Gross Domestic Product')
  gdppotSum    = Summary('fred_gdp_pot', 'Real Potential Gross Domestic Product')
  ngdppotGauge = Gauge('fred_nom_gdp_pot_val', 'Nominal Potential Gross Domestic Product')
  ngdppotSum   = Summary('fred_nom_gdp_pot', 'Nominal Potential Gross Domestic Product')
  nrouGauge    = Gauge('fred_nrou_lt_val', 'Natural Rate of Unemployment (Long-Term)')
  nrouSum      = Summary('fred_nrou_lt', 'Natural Rate of Unemployment (Long-Term)')
  #ggnlbpGauge = Gauge('fred_ggnlb_proj', 'Projection of General gov\'t net lending/borrowing')
  #ggnlbpSum   = Summary('fred_ggnlb_proj', 'Projection of General gov\'t net lending/borrowing')


  # Start the Prometheus to expose metrics
  start_http_server(8000)

  # Associate each dataset with its metric
  data = [(nroust, nroustGauge, nroustSum), 
          (gdppot, gdppotGauge, gdppotSum), 
          (ngdppot, ngdppotGauge, ngdppotSum),
          (nrou, nrouGauge, nrouSum)]#,
          #(ggnlbp, ggnlbpGauge, ggnlbpSum)]

  try:
    print '\n\nSetup complete. Ctrl-C to kill server.\n'
    # Continuously publish data, wrapping back to the beginning when the end is reached.
    while True:
        # Go through each table and transfer its data to the corresponding Prometheus metric
        timestamps = nroust.index.date
        for i in range(0, len(nroust)): 
            # datetimeToTimestamp(timestamps[i]) # TODO: Set the time of observation
            for (table, gauge, summary) in data:
              # Observe the datapoint in prometheus
              gauge.set(table.iat[i, 0]) 
              summary.observe(table.iat[i, 0])
            time.sleep(5)
  finally:
    print "Exiting\n"