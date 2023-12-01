import settings
import requests
import logging
import json
from prometheus_client import start_http_server
from prometheus_client import Gauge
from prometheus_client import Counter


class Operations():

    def __init__(self) -> None:
        logging.info('Getting the weather station data.')

    def get_coords(self):

        co = []

        for ws in self.get_devices():
            co.append(ws['info']['coords'])
        
        return co
    
    def get_name(self):
        names = []

        for ws in self.get_devices():
            names.append(ws['info']['name'])
        
        return names

    def get_devices(self):

        self.url = f"{settings.amb_endpoint}/devices/?apiKey={settings.api_key}&applicationKey={settings.app_key}"

        return self._getvalue()

    def get_device(self,mac):
        
        self.url = f"{settings.amb_endpoint}/devices/{mac}?apiKey={settings.api_key}&applicationKey={settings.app_key}&limit=1&end_date={settings.current_time}"

        return self._getvalue() 

    def _getvalue(self):
        
        logging.info("Getting the url value.")
        
        try:
            payload = {}
            headers = {}
            response = requests.request("GET", self.url, headers=headers, data=payload)
        except Exception as e:
            logging.error(f"Could not get the device info: {e}")
            raise e

        return json.loads(response.text)[0]
    
class Prometheus():
    
    def __init__(self):
        logging.info("Starting Prometheus scrape endpoint")
        #start_http_server(9002)

    def start_server(self):
        start_http_server(9002)
        self.dewpoint = Gauge('dewpoint','The current dew point.',['name','location','mac'])
        self.tempinf = Gauge('current_temp','The current temperature.',['name','location','mac'])
        self.feelslike = Gauge('feels_like','Feels like temp',['name','location','mac'])
        self.humidity = Gauge('humidity','The current humidity',['name','location','mac'])
        self.lightningday = Gauge('lightning_day','Number of lighting strikes per day.',['name','location','mac'])
        self.weeklyrainin = Gauge('weekly_rain','The weekly amount of rain in inches.',['name','location','mac'])
        self.dailyrainin = Gauge('daily_rain','The daily amount of rain in inches.',['name','location','mac'])
        self.yearlyrainin = Gauge('yearly_rain','The yearly amount of rain in inches.',['name','location','mac'])
        self.monthlyrainin = Gauge('monthly_rain','The monthly amount of rain in inches.',['name','location','mac'])
        self.windspeedmph = Gauge('windspeed_mph','The current windspeed in mph.',['name','location','mac'])

    def current_readings(self,input_dict):
        """
        DESC: Emit the current ping success
        INPUT: input_dict - name
                          - location
                          - mac
                          - dewpoint
                          - 
        OUTPUT: None
        """
        try:
            logging.info("Emitting weather station metrics.")
            self.dewpoint.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['dewpoint'])
            self.tempinf.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['tempin'])
            self.feelslike.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['feelslike'])
            self.humidity.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['humidity'])
            self.lightningday.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['lightningday'])
            self.weeklyrainin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['weeklyrainin'])
            self.dailyrainin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['dailyrainin'])
            self.yearlyrainin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['yearlyrainin'])
            self.monthlyrainin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['monthlyrainin'])
            self.windspeedmph.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['windspeedmph'])
        except Exception as e:
            logging.error(e)
            logging.error("Could not emit the weather metrics.")
