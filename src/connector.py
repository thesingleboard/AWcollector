import settings
import logging
import time

from connector_lib import Operations as op
from connector_lib import Prometheus as prom

pr = prom()

def main():
    pr.start_server()

    while  True:
        logging.info(f"Collecting metrics from Ambiant weather. Timestamp: {settings.current_time}")
        o = op()
        current = o.get_metrics()
        current['name'] = o.get_name()
        current['location'] = o.get_location()
        current['mac'] = o.get_mac()
        pr.current_readings(current)
        time.sleep(settings.interval)

if __name__ == "__main__":
    logging.info("Starting the Ambiant weather collector.")
    main()