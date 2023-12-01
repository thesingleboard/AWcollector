import settings
import logging

from connector_lib import Operations as op
from connector_lib import Prometheus as prom

pr = prom()
o = op()

def get_data():
    data = o.get_devices()

    return {'dewpoint':data['lastData']['dewPointin'],
            'tempin':data['lastData']['tempinf'],
            'feelslike':data['lastData']['feelsLikein'],
            'humidity':data['lastData']['humidityin'],
            'lightningday':data['lastData']['lightning_day'],
            'weeklyrainin':data['lastData']['weeklyrainin'],
            'dailyrainin':data['lastData']['dailyrainin'],
            'yearlyrainin':data['lastData']['yearlyrainin'],
            'monthlyrainin':data['lastData']['monthlyrainin'],
            'windspeedmph':data['lastData']['windspeedmph']}

def get_id():
    coords = o.get_coords()
    name = o.get_name()

def main():
    pr.start_server()

    while  True:
        current = get_data()
        pr.current_readings(current)

if __name__ == "__main__":
    main()