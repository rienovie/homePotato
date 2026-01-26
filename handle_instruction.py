
import datetime
from numpy import random
import voice
import save

import weather

global Working, City
Working = False

# NOTE: put your city here
City = "Philadelphia"

# TODO: for the weather, I think the best way would have it auto-fetch it every hour or so and then just use the latest


def handle_instruction(instruction):

    global Working, City
    if Working or instruction.__len__() == 0:
        return

    Working = True

    # TODO: this does not feel very efficient but should work for now
    if instruction.__contains__("cancel" or "stop"):
        print("Cancelling")

    elif instruction.__contains__("random voice"):
        voice.speak("Setting voice to a random value")
        voice.set_config_values(
            # NOTE: for libritts, there are 904 values for speaker_id
            speaker_id=random.randint(0, 903)
        )
        save.save_voice_options()
        voice.speak("This will be my new voice with id " + str(voice.config.speaker_id))

    elif instruction.__contains__("weather"):
        voice.speak("Getting the weather")

        w = weather.get_weather_sync(City)

        response = (
            f"In {City} it is currently {w.description} at {w.temperature} degrees. "
            f"Today will have a high of {w.daily_forecasts[0].highest_temperature} "
            f"and a low of {w.daily_forecasts[0].lowest_temperature}"
        )

        voice.speak(response)

    elif instruction.__contains__("rain"):
        voice.speak("Rain has not been implemented yet")

    elif instruction.__contains__("snow"):
        voice.speak("Snow has not been implemented yet")

    elif instruction.__contains__("play"):
        voice.speak("Playing has not been implemented yet")

    elif instruction.__contains__("timer"):
        voice.speak("Timer has not been implemented yet")

    elif instruction.__contains__("time"):
        voice.speak("It is currently " + datetime.datetime.now().strftime("%-I %M %p, on %A %B %-d, %Y"))

    else:
        voice.speak("I'm not sure what the instruction quote" + instruction + "end quote means")
        print("Unknown instruction:", instruction)

    Working = False
