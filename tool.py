from llama_index.core.tools import FunctionTool
import requests
import os
from dotenv import load_dotenv
load_dotenv()

url="https://api.openweathermap.org/data/2.5/weather"
api_key= os.getenv("WEATHER_API_KEY")

def get_Weather(city):
    """This function fetches the current weather for a given city using the OpenWeatherMap API."""
    units="metric"
    params={
        'q': city,
        'appid': api_key,
        'units': units
    }
    response=requests.get(url,params=params)
    result= response.json()
    return result

weather_tool=FunctionTool.from_defaults(
    fn=get_Weather,
    name="get_Weather",
    description="Get the current weather for a given city.",
)