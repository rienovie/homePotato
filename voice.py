
import threading
import queue
import pyaudio
from piper import PiperVoice, SynthesisConfig


class TTSService:
    def __init__(self, voice_path):
        self.voice = PiperVoice.load(voice_path)
        self.config = SynthesisConfig()
        self.text_queue = queue.Queue()
        self.running = False
        self.thread = None
        self.stream = None
        self.p = None

    def set_config(self, **kwargs):
        # Update any SynthesisConfig field dynamically
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            else:
                raise ValueError(f"Invalid config option: {key}")

    def speak(self, text):
        self.text_queue.put(text)

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if self.p:
            self.p.terminate()
            self.p = None

    def _init_audio_stream(self, chunk):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(chunk.sample_width),
            channels=chunk.sample_channels,
            rate=chunk.sample_rate,
            output=True
        )

    def _worker(self):
        while self.running:
            try:
                text = self.text_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            # Piper synthesizes streaming chunks
            chunks = self.voice.synthesize(text, self.config)
            first_chunk = next(chunks, None)
            if first_chunk is None:
                continue

            # Init audio if needed
            if not self.stream:
                self._init_audio_stream(first_chunk)

            # Play chunks
            self.stream.write(first_chunk.audio_int16_bytes)
            for chunk in chunks:
                if not self.running:
                    break
                self.stream.write(chunk.audio_int16_bytes)

