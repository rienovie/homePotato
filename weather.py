
import python_weather
import asyncio
import os
import datetime

import save

global location, weatherCache
location: str = "Philadelphia"  # Default location


class fc_json:
    def __init__(self, forCas):
        self.data["description"] = forCas.description
        self.data["temperature"] = forCas.temperature
        self.data["feels_like"] = forCas.feels_like
        self.data["daily_forecasts"] = []
        for d in forCas.daily_forecasts:
            self.data["daily_forecasts"].append({
                "date": datetime.datetime.strftime(d.date, "%Y.%m.%d"),
                "highest_temperature": d.highest_temperature,
                "lowest_temperature": d.lowest_temperature
            })

    data = {
        "description": str,
        "temperature": int,
        "feels_like": int,
        "daily_forecasts": [
            {
                "date": str,
                "highest_temperature": int,
                "lowest_temperature": int
            }
        ],
    }


weatherCache: dict = {
    "location": str,
    "last_updated": datetime.datetime,
    "forecast": fc_json.data
}


def update_weather():
    global location, weatherCache
    fore = get_weather_sync(location)
    weatherCache["location"] = fore.location
    weatherCache["last_updated"] = datetime.datetime.now()
    weatherCache["forecast"] = fc_json(fore).data
    save.save_weather_cache()


def check_weather():
    global location, weatherCache
    if weatherCache["last_updated"] + datetime.timedelta(hours=1) < datetime.datetime.now():
        update_weather()


def load_weather():
    global location, weatherCache
    print("Loading weather cache")

    if not os.path.exists(f"{save.saveLocation}/weather_cache.json"):
        print("No weather cache found creating one")
        update_weather()

    save.load_weather_cache()


def get_weather_cache(_location):
    global location, weatherCache
    if location != _location:
        print("Location changed, updating cache")
        location = _location
        fore = get_weather_sync(location)
        weatherCache["location"] = fore.location
        weatherCache["last_updated"] = datetime.datetime.now()
        weatherCache["forecast"] = fc_json(fore).data
        save.save_weather_cache()
    return weatherCache


def get_weather_sync(location):
    print("Getting weather")
    return asyncio.run(_get_weather(location))


async def _get_weather(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        foreC = await client.get(location)
        return foreC
