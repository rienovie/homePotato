
import python_weather
import asyncio
import os
import datetime

import save

global location, weatherCache
location: str = "Philadelphia"  # Default location

weatherCache = {
    "location": location,
    "last_updated": datetime.datetime,
    "forecast": None
}


def load_weather():
    global location, weatherCache
    print("Loading weather cache")

    if not os.path.exists(f"{save.saveLocation}/weather_cache.json"):
        print("No weather cache found creating one")
        fore = get_weather_sync(location)
        weatherCache["location"] = fore.location
        weatherCache["last_updated"] = datetime.datetime.now()
        weatherCache["forecast"] = fore
        save.save_weather_cache()

    save.load_weather_cache()


def get_weather_cache(_location):
    global location, weatherCache
    if location != _location:
        print("Location changed, updating cache")
        location = _location
        fore = get_weather_sync(location)
        weatherCache["location"] = fore.location
        weatherCache["last_updated"] = datetime.datetime.now()
        weatherCache["forecast"] = fore
        save.save_weather_cache()
    return weatherCache


def get_weather_sync(location):
    print("Getting weather")
    return asyncio.run(_get_weather(location))


async def _get_weather(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        foreC = await client.get(location)
        return foreC
