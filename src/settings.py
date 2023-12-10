import os
import time

api_key = os.getenv('AMBIENT_API_KEY',None)
app_key = os.getenv('AMBIENT_APPLICATION_KEY',None)
amb_endpoint = os.getenv('AMBIENT_ENDPOINT','https://api.ambientweather.net/v1')

current_time = int(time.time())