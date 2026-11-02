from Controller.Handlers import *
from AudioProcessor import AudioProcessorAggregate
from Visualizer import VisualAggregate
import json
from pydantic import BaseModel, Field

class ControllerAggregate:
    def __init__(self, config_paths):
        IH = InitHandler(self)
        InitEvent.publish(status="Initializing", payload="Initializing Controller...\n")

        self.CONFIG = self.load_configuration(config_paths)
        self.AudioProcessor = AudioProcessorAggregate.AudioProcessorAggregate(self.CONFIG)
        AudioChunk = self.AudioProcessor()
        self.Visualizer = VisualAggregate.VisualAggregate(AudioChunk, self.CONFIG)
        self.running = True

        InitEvent.publish(status="Complete", payload="|/ Controller Done.\n\n")

    def run(self):
        RH = RuntimeHandler(self)
        while self.running:
            AudioChunk = self.AudioProcessor()
            self.Visualizer(AudioChunk)

    def load_configuration(self, config_paths):
        config = {}
        for path in config_paths:
            with open(path, "r") as file:
                
                clean_lines = []
                for line in file:
                    if line.strip().startswith("//"):
                        continue
                    clean_lines.append(line)

                clean_json_string = "".join(clean_lines)
                config = {**config, **json.loads(clean_json_string)}

        return AudioVisualizerConfig(**config)

class AudioVisualizerConfig(BaseModel):
    AUDIO_SOURCE: str = "MICROPHONE"
    MICROPHONE_CHANNELS: int = 1
    AUDIO_SAMPLE_RATE: int = 44100
    AUDIO_SAMPLE_SIZE: int = 1024
    
    AUDIO_FFT_BINS: int = 100
    AUDIO_FFT_DECAY_RATE: float = 0.01
    AUDIO_FFT_SMOOTH_WINDOW: int = 7
    AUDIO_MIN_FREQUENCY: int = 160
    AUDIO_MAX_FREQUENCY: int = 20000
    
    SCREEN_SIZE: list | None = None
    MAX_CLOCK_RATE: int = 60
    SHADER_PATHS: list
