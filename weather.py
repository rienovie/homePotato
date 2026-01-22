
import python_weather
import asyncio
import os
import datetime

import save

global location, weatherCache
location: str = "Philadelphia"  # Default location

weatherCache = {
    "location": location,
    "last_updated": datetime.datetime.now(),
    "forecast": python_weather.Forecast
}


def load_weather():
    global location, weatherCache
    print("Loading weather cache")

    if not os.path.exists("resources/local/weather_cache.json"):
        print("No weather cache found creating one")
        weatherCache = get_weather_sync(location)
        save.save_weather_cache()

    save.load_weather_cache()


def get_weather_cache(_location):
    global location, weatherCache
    if location != _location:
        print("Location changed, updating cache")
        location = _location
        weatherCache = get_weather_sync(location)
        save.save_weather_cache()
    return weatherCache


def get_weather_sync(location):
    return asyncio.run(_get_weather(location))


async def _get_weather(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        Config = await client.get(location)
        return Config
