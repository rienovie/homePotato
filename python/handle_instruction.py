
import datetime
from numpy import random
import voice
import save
import update as update
from word2number import w2n

import weather

global Working, City
Working = False

# NOTE: put your city here
City = "Philadelphia"


def handle_instruction(instruction):

    global Working, City
    if Working or instruction.__len__() == 0:
        return

    Working = True

    # TODO: this does not feel very efficient but should work for now
    if instruction.__contains__("cancel" or "stop"):
        print("Cancelling")
        if instruction.__contains__("timer"):
            voice.speak("Timer is not implemented yet, but would be cancelled if it was")

    elif instruction.__contains__("system update"):
        voice.speak("Checking for updates")
        if update.check_for_updates():
            raise update.updateException
        else:
            voice.speak("The system is currently up to date")

    # 'set' as a command is easy for the voice to text to misinterpret
    # 'assign' also sucks :(
    elif instruction.__contains__("set option"):
        set_option(instruction)
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

        w = weather.get_weather_cache(City)["forecast"]

        voice.speak("In " + City + " it is currently " + w["description"] + " at " + w["temperature"].__str__() + " degrees")
        voice.speak("Today will have a high of " + w["daily_forecasts"][0]["highest_temperature"].__str__())
        voice.speak("and a low of " + w["daily_forecasts"][0]["lowest_temperature"].__str__())

    elif instruction.__contains__("rain"):
        voice.speak("Rain has not been implemented yet")

    elif instruction.__contains__("snow"):
        voice.speak("Snow has not been implemented yet")

    elif instruction.__contains__("play"):
        voice.speak("Playing has not been implemented yet")

    elif instruction.__contains__("time"):
        voice.speak("It is currently " + datetime.datetime.now().strftime("%-I %M %p, on %A %B %-d, %Y"))

    else:
        voice.speak("I'm not sure what the instruction quote" + instruction + "end quote means")
        print("Unknown instruction:", instruction)

    Working = False


def set_option(instruction):
    # TODO: this doesn't feel good to set the city this way, make it better
    # maybe will just have it be set manually instead of with your voice
    if instruction.__contains__("city"):
        value = instruction.split("city")[-1]

        # trim off 'to' for natural language "potato set city to X"
        if value.__contains__(" to "):
            value = value.split(" to ")[-1]

        voice.speak("Getting the weather for the new city " + value)
        weather.get_weather_sync(value)

        w = weather.get_weather_cache(City)["forecast"]

        voice.speak("In " + City + " it is currently " + w["description"] + " at " + w["temperature"].__str__() + " degrees")
        voice.speak("Today will have a high of " + w["daily_forecasts"][0]["highest_temperature"].__str__())
        voice.speak("and a low of " + w["daily_forecasts"][0]["lowest_temperature"].__str__())

    elif instruction.__contains__("voice"):
        value = instruction.split("voice")[-1]

        # trim off 'to' for natural language "potato set voice to X"
        if value.__contains__(" to "):
            value = value.split(" to ")[-1]

        value = w2n.word_to_num(value)

        # NOTE: for libritts, there are 904 values for speaker_id
        if value > 903 or value < 0:
            voice.speak("Voice ID must be between 0 and 903. You said '" + value.__str__() + "'")
            return
        voice.speak("Setting voice to '" + value.__str__() + "'")
        voice.set_config_values(
            speaker_id=int(value)
        )
        save.save_voice_options()
        voice.speak("This will be my new voice with id " + str(voice.config.speaker_id))

    elif instruction.__contains__("timer"):
        value = instruction.split("timer")[-1]
        voice.speak("Timer has not been implemented yet, but would be set to '" + value + "' if it was")
    else:
        voice.speak("I was unable to set an option. What I heard was: " + instruction)
