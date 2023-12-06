import settings
import logging
import time

from connector_lib import Operations as op
from connector_lib import Prometheus as prom

pr = prom()
#o = op()

def main():
    pr.start_server()

    while  True:
        o = op()
        current = o.get_metrics()
        current['name'] = o.get_name()
        current['location'] = o.get_location()
        current['mac'] = o.get_mac()
        pr.current_readings(current)
        time.sleep(30)

if __name__ == "__main__":
    main()