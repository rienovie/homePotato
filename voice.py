
import pyaudio
from piper import PiperVoice, SynthesisConfig

voice = PiperVoice.load("resources/piper-voices/en_US-libritts_r-medium.onnx")
config = SynthesisConfig()

def set_config_values(**kwargs):
    for k, v in kwargs.items():
        if hasattr(config, k):
            setattr(config, k, v)
        else:
            print(f"Config key {k} not found")

def speak(text):
    # Get first chunk so we know sample format
    gen = voice.synthesize(text, config)
    first_chunk = next(gen)

    # Setup PyAudio stream for the format Piper uses
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(first_chunk.sample_width),
        channels=first_chunk.sample_channels,
        rate=first_chunk.sample_rate,
        output=True
    )

    # Play first chunk
    stream.write(first_chunk.audio_int16_bytes)

    # Play remaining chunks
    for chunk in gen:
        stream.write(chunk.audio_int16_bytes)

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

