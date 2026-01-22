
# for saving/loading options to a file

import json
import voice
import weather


def save_voice_options():
    with open("resources/local/voice_options.json", "w") as f:
        json.dump(voice.config.__dict__, f)


def load_voice_options():
    with open("resources/local/voice_options.json", "r") as f:
        options = json.load(f)
    apply_voice_options(options)


def apply_voice_options(options):
    for k, v in options.items():
        if hasattr(voice.config, k):
            setattr(voice.config, k, v)
        else:
            print(f"Config key {k} not found")


def save_weather_cache():
    with open("resources/local/weather_options.json", "w") as f:
        json.dump(weather.weatherCache.__dict__, f)


def load_weather_cache():
    with open("resources/local/weather_options.json", "r") as f:
        options = json.load(f)
    apply_weather_cache(options)


def apply_weather_cache(options):
    for k, v in options.items():
        if hasattr(weather.weatherCache, k):
            setattr(weather.weatherCache, k, v)
        else:
            print(f"Weather cache key {k} not found")
