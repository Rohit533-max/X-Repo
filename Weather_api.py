import os
from dotenv import dotenv_values,load_dotenv
import requests

load_dotenv()
key = os.getenv("Weather_key")

city = input("Enter the city: ")

url = "https://api.openweathermap.org/data/2.5/weather"
p = {"q": city, "appid": key, "units": "metric"}
try:
    r = requests.get(url,params=p)
    r.raise_for_status()
    data = r.json()
    print(f"{city}: {data['main']['temp']}°C {data['weather'][0]['description']}")
    


except requests.exceptions.RequestException as e:
    print(e)
