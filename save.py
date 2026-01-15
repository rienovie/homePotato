
# for saving/loading options to a file

import json
import voice

def save_voice_options():
    with open("voice_options.json", "w") as f:
        json.dump(voice.config.__dict__, f)

def load_voice_options():
    with open("voice_options.json", "r") as f:
        options = json.load(f)
    apply_voice_options(options)

def apply_voice_options(options):
    for k, v in options.items():
        if hasattr(voice.config, k):
            setattr(voice.config, k, v)
        else:
            print(f"Config key {k} not found")
