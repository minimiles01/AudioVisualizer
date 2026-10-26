from Controller.Handlers import *
import pyaudio
import soundcard
import numpy as np

class MicrophoneAudioCapture:
    def __init__(self):
        # --- CONFIGURATION PARAMETERS ---
        self.FORMAT = pyaudio.paFloat32     # 16-bit resolution (standard for audio)
        self.CHANNELS = 1                 # Mono microphone input
        self.RATE = 44100                 # CD-quality sampling rate (Hz)
        self.CHUNK = 1024                 # Buffer size (number of samples per read)

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
        audio_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        return audio_data
        
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class SoundcardAudioCapture:
    def __init__(self):
        self.BLOCK_SIZE = 1024  # Polling rate sample size
        self.SAMPLE_RATE = 44100

        self.default_speaker = soundcard.default_speaker()

        self.loopback_interface = soundcard.get_microphone(
            id=self.default_speaker.id, 
            include_loopback=True
        )

        self._recorder_context = self.loopback_interface.recorder(samplerate=self.SAMPLE_RATE)
        
        self.recorder = self._recorder_context.__enter__()

        try:
            import warnings
            # Suppress only the Soundcard data discontinuity warnings
            warnings.filterwarnings("ignore", category=soundcard.SoundcardRuntimeWarning)
        except Exception as e:
            ErrorEvent.publish(status="SoundcardAudioCapture_WarningSuppressFailed", payload=e)


    def __call__(self):
        audio_data = self.recorder.record(numframes=self.BLOCK_SIZE)
        return np.sum(audio_data, axis=1)

    def __del__(self):
        self._recorder_context.__exit__(None, None, None)

class AudioTransform:
    def __init__(self):
        self.fft_bins = 100
        self.fft_decay_array = np.zeros(self.fft_bins)
        self.decay_rate = 0.01
        self.fft_list = [np.zeros(self.fft_bins)]*7

    def __call__(self, raw_data):
        audio_data = np.frombuffer(raw_data, dtype=np.float32)
        buffer_data = self.calculate_buffer_data(audio_data)
        AudioChunk = self.prepare_for_buffer(*buffer_data)
        return AudioChunk

    def calculate_buffer_data(self, audio_data):
        fft_data = np.fft.fft(audio_data)
        fft_mapped = self.calculate_log_bins(fft_data, 44100, num_bars=self.fft_bins)
        fft_normalized = self.normalize_fft(fft_mapped)
        fft_smoothed = self.smooth_fft(fft_normalized)
        self.fft_decay(fft_smoothed)

        amplitude = np.abs(audio_data)
        volume_level = np.average(amplitude)
        return volume_level, audio_data, fft_smoothed, self.fft_decay_array

    def prepare_for_buffer(self, *args):
        flat_list = []
        for i in args:
            if type(i) is np.ndarray:
                flat_list.extend(np.ravel(i))
            else:
                flat_list.append(i)
        return np.array(flat_list, dtype=np.float32)

    def normalize_fft(self, fft_data):
        fft_abs = np.abs(fft_data)
        fft_clamped = np.clip(fft_abs, 0, 1)
        fft_no_nan = np.nan_to_num(fft_clamped, nan=1.0)
        return fft_no_nan

    def smooth_fft(self, fft_data):
        self.fft_list.pop(0)
        self.fft_list.append(fft_data)
        return np.average(self.fft_list, axis=0).astype(np.float32)

    def fft_decay(self, fft_data):
        self.fft_decay_array = np.maximum(fft_data, self.fft_decay_array - self.decay_rate)

    def calculate_log_bins(self, fft_magnitudes, sample_rate, num_bars=100, min_freq=160, max_freq=20000):
        fft_size = (len(fft_magnitudes) - 1) * 2
        # Example: index 0 = 0Hz, index 512 = 22050Hz (at 44.1kHz sample rate)
        fft_frequencies = np.fft.rfftfreq(fft_size, d=1.0/sample_rate)
        bin_edges = np.logspace(np.log10(min_freq), np.log10(max_freq), num_bars + 1)
        
        bars_display = np.zeros(num_bars)
        for i in range(num_bars):
            lower_limit = bin_edges[i]
            upper_limit = bin_edges[i + 1]
            in_band_indices = np.where((fft_frequencies >= lower_limit) & (fft_frequencies < upper_limit))[0]    
            if len(in_band_indices) > 0:
                bars_display[i] = np.mean(fft_magnitudes[in_band_indices])
            else:
                # Edge case: For ultra-low bass frequencies, the log bands might be narrower 
                # than a single linear FFT bin width. If empty, grab the closest single bin.
                closest_idx = np.argmin(np.abs(fft_frequencies - lower_limit))
                bars_display[i] = fft_magnitudes[closest_idx]
                
        bars_display_db = np.log10(bars_display + 1e-5)
        return bars_display_db
