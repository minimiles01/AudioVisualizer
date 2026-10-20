from Controller.Handlers import *
from AudioProcessor import AudioTools

class AudioProcessorAggregate:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="|-Initializing AudioProcessor...")

        self.AudioTransform = AudioTools.AudioTransform()
        self.AudioCapture = AudioTools.AudioCapture(transform=self.AudioTransform)

        InitEvent.publish(status="Complete", payload="Done.\n")

    def __call__(self):
        return self.AudioCapture()
