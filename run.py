#!/usr/bin/env python3

import argparse
from logging import error
import os
import queue
import sys
import sounddevice as sd
import simpleaudio as sa

import handle_instruction as handle
import save
import voice
import weather

from vosk import Model, KaldiRecognizer, json

q = queue.Queue()
keyword = "potato"

wakeWav = sa.WaveObject.from_wave_file("resources/public/sounds/wake.wav")
endWav = sa.WaveObject.from_wave_file("resources/public/sounds/end.wav")


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


# TODO: right now this is called twice, spilt into two functions
# one for early loading and one for after insitalization loading
# the voice options should be loaded after initialization of the voice
def loadUserOptions():
    print("Loading user options")

    if not os.path.exists(f"{save.saveLocation}/voice_options.json"):
        # default voice options
        voice.set_config_values(
            speaker_id=2,
            length_scale=1.0,
            noise_scale=0.667,
            noise_w_scale=0.8,
            normalize_audio=True,
            volume=1.0
        )
        save.save_voice_options()
    else:
        save.load_voice_options()

    if not os.path.exists(f"{save.saveLocation}/weather_cache.json"):
        weather.load_weather()
        save.save_weather_cache()
    else:
        save.load_weather_cache()


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    loadUserOptions()

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])

    if args.model is None:
        # NOTE: put your model here
        model = Model(
            "resources/local/vosk-models/vosk-model-small-en-us-0.15")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(
            samplerate=args.samplerate,
            blocksize=8000,
            device=args.device,
            dtype="int16",
            channels=1,
            callback=callback
    ):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        active = False

        loadUserOptions()

        # TODO: make sure this doesn't set off it's self
        voice.speak("Welcome to homePotato")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                final = json.loads(rec.FinalResult()).get("text", "")

                if active:
                    endWav.play()
                    active = False

                    # the first index is everything after the first keyword uesed
                    sFinal = str.split(final, keyword, 1)[1]

                    handle.handle_instruction(sFinal)

            # NOTE: 20 is the length when no value is there, instead of running json.loads every check this works
            # the result is a string in json so that's why the formatting is weird
            elif rec.PartialResult().__len__() > 20:

                # NOTE: Partial result is not cleared until complete result is received
                parRes = json.loads(rec.PartialResult()).get("partial", "")

                if not active and parRes.__contains__(keyword):
                    active = True
                    wakeWav.play()

            if dump_fn is not None:
                dump_fn.write(data)


except KeyboardInterrupt:
    voice.speak("Goodbye")
    print("\nDone")
    parser.exit(0)
except Exception as e:
    voice.speak("Oops, I have crashed")
    error(e)
    parser.exit(1)
