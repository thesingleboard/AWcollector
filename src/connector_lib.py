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
        self.device = self._get_devices()

    def get_coords(self):
        
        return self.device['info']['coords']['coords']
    
    def get_location(self):
        
        return self.device['info']['coords']['location']
    
    def get_name(self):
        
        return self.device['info']['name']
    
    def get_mac(self):

        return self.device['macAddress']

    def get_metrics(self):

        return {
                'aw_dewpoint':self.device['lastData']['dewPointin'],
                'aw_tempin':self.device['lastData']['tempinf'],
                'aw_feelslike':self.device['lastData']['feelsLikein'],
                'aw_humidity':self.device['lastData']['humidityin'],
                'aw_lightningday':self.device['lastData']['lightning_day'],
                'aw_lightninghour':self.device['lastData']['lightning_hour'],
                'aw_lightningtime':self.device['lastData']['lightning_time'],
                'aw_lightningdistance':self.device['lastData']['lightning_distance'],
                'aw_dailyrainin':self.device['lastData']['dailyrainin'],
                'aw_weeklyrainin':self.device['lastData']['weeklyrainin'],
                'aw_monthlyrainin':self.device['lastData']['monthlyrainin'],
                'aw_yearlyrainin':self.device['lastData']['yearlyrainin'],
                'aw_maxgust':self.device['lastData']['maxdailygust'],
                'aw_solarradiation':self.device['lastData']['solarradiation'],
                'aw_windspeedmph':self.device['lastData']['windspeedmph'],
                'aw_barametric':self.device['lastData']['baromabsin'],
                'aw_winddir':self.device['lastData']['winddir']
                }
    
    def _get_devices(self):

        self.url = f"{settings.amb_endpoint}/devices/?apiKey={settings.api_key}&applicationKey={settings.app_key}"

        return self._getvalue()

    def _get_device(self,mac):
        
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

    def start_server(self):
        start_http_server(9028)
        self.aw_dewpoint = Gauge('aw_dewpoint','The current dew point.',['name','location','mac'])
        self.aw_tempin = Gauge('aw_tempin','The current temperature.',['name','location','mac'])
        self.aw_feelslike = Gauge('aw_feelslike','Feels like temp',['name','location','mac'])
        self.aw_humidity = Gauge('aw_humidity','The current humidity',['name','location','mac'])
        self.aw_lightningday = Gauge('aw_lightningday','Number of lighting strikes per day.',['name','location','mac'])
        self.aw_lightninghour = Gauge('aw_lightninghour','Number of lighting strikes per hour.',['name','location','mac'])
        self.aw_lightningtime = Gauge('aw_lightningtime','Time of the last lightning strike in unix epoc.',['name','location','mac'])
        self.aw_lightningdistance = Gauge('aw_lightningdistance','The distance of the last lightning strike in miles.',['name','location','mac'])
        self.aw_weeklyrainin = Gauge('aw_weeklyrainin','The weekly amount of rain in inches.',['name','location','mac'])
        self.aw_dailyrainin = Gauge('aw_dailyrainin','The daily amount of rain in inches.',['name','location','mac'])
        self.aw_yearlyrainin = Gauge('aw_yearlyrainin','The yearly amount of rain in inches.',['name','location','mac'])
        self.aw_monthlyrainin = Gauge('aw_monthlyrainin','The monthly amount of rain in inches.',['name','location','mac'])
        self.aw_windspeedmph = Gauge('aw_windspeedmph','The current windspeed in mph.',['name','location','mac'])
        self.aw_maxgust = Gauge('aw_maxgust','The maximum daily wind gust speed.',['name','location','mac'])
        self.aw_solarradiation = Gauge('aw_solarradiation','Solar radiation for the day.',['name','location','mac'])
        self.aw_barametric = Gauge('aw_barametric','Absolute barametric pressure measured in bars.',['name','location','mac'])
        self.aw_winddir = Gauge('aw_winddir','Wind direction in degrees.',['name','location','mac'])

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
            self.aw_dewpoint.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_dewpoint'])
            self.aw_tempin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_tempin'])
            self.aw_feelslike.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_feelslike'])
            self.aw_humidity.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_humidity'])
            self.aw_lightninghour.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_lightninghour'])
            self.aw_lightningday.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_lightningday'])
            self.aw_lightningtime.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_lightningtime'])
            self.aw_lightningdistance.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_lightningdistance'])
            self.aw_dailyrainin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_dailyrainin'])
            self.aw_weeklyrainin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_weeklyrainin'])
            self.aw_monthlyrainin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_monthlyrainin'])
            self.aw_yearlyrainin.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_yearlyrainin'])
            self.aw_windspeedmph.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_windspeedmph']) 
            self.aw_maxgust.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_maxgust'])
            self.aw_solarradiation.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_solarradiation'])
            self.aw_barametric.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_barametric'])
            self.aw_winddir.labels(input_dict['name'],input_dict['location'],input_dict['mac']).set(input_dict['aw_winddir'])
        except Exception as e:
            logging.error(e)
            logging.error("Could not emit the weather metrics.")