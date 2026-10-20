import pyaudio
import numpy as np
from dataclasses import dataclass

class AudioCapture:
    def __init__(self, transform):
        # --- CONFIGURATION PARAMETERS ---
        self.FORMAT = pyaudio.paInt16     # 16-bit resolution (standard for audio)
        self.CHANNELS = 1                 # Mono microphone input
        self.RATE = 44100                 # CD-quality sampling rate (Hz)
        self.CHUNK = 1024                 # Buffer size (number of samples per read)

        self.transform = transform
        self.p = pyaudio.PyAudio()

        # Open the microphone live stream
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,              # Set to True to record microphone input
            frames_per_buffer=self.CHUNK
        )

    def __call__(self):
        return self.transform(self.stream.read(self.CHUNK, exception_on_overflow=False))
        
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class AudioTransform:
    def __call__(self, raw_data):
        audio_data = np.frombuffer(raw_data, dtype=np.int16)
        fft_data = np.fft.fft(audio_data) #Need to convert to 1D float array rather than complex array
        amplitude = np.abs(audio_data)
        volume_level = np.average(amplitude)
        volume_meter = int(volume_level / 100)
        return self.AudioChunk(audio_data, fft_data, amplitude, volume_meter)

    @dataclass
    class AudioChunk:
        audio_data: np.int16
        fft_data: np.ndarray
        amplitude: list[np.int16]
        volume_meter: int