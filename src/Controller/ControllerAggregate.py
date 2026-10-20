from Controller.Handlers import *
from AudioProcessor import AudioProcessorAggregate
from Visualizer import VisualAggregate

class ControllerAggregate:
    def __init__(self):
        IH = InitHandler(self)
        InitEvent.publish(status="Initializing", payload="Initializing Controller...\n")
        
        self.AudioProcessor = AudioProcessorAggregate.AudioProcessorAggregate()
        self.Visualizer = VisualAggregate.VisualAggregate()
        self.running = True

        InitEvent.publish(status="Complete", payload="|/ Controller Done.\n\n")

    def run(self):
        RH = RuntimeHandler(self)
        while self.running:
            AudioChunk = self.AudioProcessor()
            self.Visualizer(AudioChunk)