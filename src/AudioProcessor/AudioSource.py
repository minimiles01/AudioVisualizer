from Controller.Handlers import *
import pyaudio
import soundcard
import numpy as np

class MicrophoneAudioCapture:
    def __init__(self, CONFIG):
        self.CHANNELS = CONFIG.MICROPHONE_CHANNELS  # Mono microphone input
        self.SAMPLE_RATE = CONFIG.AUDIO_SAMPLE_RATE # CD-quality sampling rate (Hz)
        self.SAMPLE_SIZE = CONFIG.AUDIO_SAMPLE_SIZE # Buffer size (number of samples per read)
        self.FORMAT = pyaudio.paFloat32

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.SAMPLE_RATE,
            input=True,              # Set to True to record microphone input
            frames_per_buffer=self.SAMPLE_SIZE
        )

    def __call__(self):
        audio_data = self.stream.read(self.SAMPLE_SIZE, exception_on_overflow=False)
        return audio_data
        
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class SoundcardAudioCapture:
    def __init__(self, CONFIG):

        self.SAMPLE_RATE = CONFIG.AUDIO_SAMPLE_RATE # CD-quality sampling rate (Hz)
        self.SAMPLE_SIZE = CONFIG.AUDIO_SAMPLE_SIZE # Buffer size (number of samples per read)
        
        self.default_speaker = soundcard.default_speaker()
        self.loopback_interface = soundcard.get_microphone(
            id=self.default_speaker.id, 
            include_loopback=True)

        self._recorder_context = self.loopback_interface.recorder(samplerate=self.SAMPLE_RATE)
        self.recorder = self._recorder_context.__enter__()

        try:
            import warnings
            # Suppress only the Soundcard data discontinuity warnings
            warnings.filterwarnings("ignore", category=soundcard.SoundcardRuntimeWarning)
        except Exception as e:
            ErrorEvent.publish(status="SoundcardAudioCapture_WarningSuppressFailed", payload=e)


    def __call__(self):
        audio_data = self.recorder.record(numframes=self.SAMPLE_SIZE)
        return np.sum(audio_data, axis=1)

    def __del__(self):
        self._recorder_context.__exit__(None, None, None)
