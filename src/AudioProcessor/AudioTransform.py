from Controller.Handlers import *
import numpy as np

class AudioTransform:
    def __init__(self, CONFIG):

        self.SAMPLE_RATE = CONFIG.AUDIO_SAMPLE_RATE
        self.FFT_BINS = CONFIG.AUDIO_FFT_BINS
        self.FFT_DECAY_RATE = CONFIG.AUDIO_FFT_DECAY_RATE
        self.MIN_FREQ = CONFIG.AUDIO_MIN_FREQUENCY
        self.MAX_FREQ = CONFIG.AUDIO_MAX_FREQUENCY

        self.fft_decay_array = np.zeros(self.FFT_BINS)
        self.fft_list = [np.zeros(self.FFT_BINS)]*CONFIG.AUDIO_FFT_SMOOTH_WINDOW

    def __call__(self, raw_data):
        audio_data = np.frombuffer(raw_data, dtype=np.float32)
        buffer_data = self.calculate_buffer_data(audio_data)
        AudioChunk = self.prepare_for_buffer(*buffer_data)
        return AudioChunk

    def calculate_buffer_data(self, audio_data):
        fft_data = np.fft.fft(audio_data)
        fft_mapped = self.calculate_log_bins(fft_data)
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
        self.fft_decay_array = np.maximum(fft_data, self.fft_decay_array - self.FFT_DECAY_RATE)

    def calculate_log_bins(self, fft_magnitudes):
        #sample_rate, num_bars=100, min_freq=160, max_freq=20000):
        fft_size = (len(fft_magnitudes) - 1) * 2
        # Example: index 0 = 0Hz, index 512 = 22050Hz (at 44.1kHz sample rate)
        fft_frequencies = np.fft.rfftfreq(fft_size, d=1.0/self.SAMPLE_RATE)
        bin_edges = np.logspace(np.log10(self.MIN_FREQ), np.log10(self.MAX_FREQ), self.FFT_BINS + 1)
        
        bars_display = np.zeros(self.FFT_BINS)
        for i in range(self.FFT_BINS):
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
