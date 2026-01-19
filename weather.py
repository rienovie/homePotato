
import python_weather
import asyncio


def get_weather_sync(location):
    return asyncio.run(_get_weather(location))


async def _get_weather(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        return await client.get(location)
