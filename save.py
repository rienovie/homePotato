
# for saving/loading options to a file

import json
import os

import voice
import weather

saveLocation = "resources/local/config"

if not os.path.exists(saveLocation):
    os.makedirs(saveLocation)


def save_voice_options():
    with open(f"{saveLocation}/voice_options.json", "w") as f:
        json.dump(voice.config.__dict__, f)


def load_voice_options():
    with open(f"{saveLocation}/voice_options.json", "r") as f:
        options = json.load(f)
    apply_voice_options(options)


def apply_voice_options(options):
    for k, v in options.items():
        if hasattr(voice.config, k):
            setattr(voice.config, k, v)
        else:
            print(f"Config key {k} not found")


def save_weather_cache():
    with open(f"{saveLocation}/weather_cache.json", "w") as f:
        json.dump(weather.weatherCache, f)


def load_weather_cache():
    with open(f"{saveLocation}/weather_cache.json", "r") as f:
        options = json.load(f)
    apply_weather_cache(options)


def apply_weather_cache(options):
    for k, v in options.items():
        if hasattr(weather.weatherCache, k):
            setattr(weather.weatherCache, k, v)
        else:
            print(f"Weather cache key {k} not found")
