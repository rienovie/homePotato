
import datetime
from logging import StrFormatStyle
from os import times
from numpy import random
import numpy
import voice
import save

Working = False

def handle_instruction(instruction):

    global Working
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
        voice.speak("Weather has not been implemented yet")
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
