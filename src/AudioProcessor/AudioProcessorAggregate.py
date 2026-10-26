from Controller.Handlers import *
from AudioProcessor import AudioTools

class AudioProcessorAggregate:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="|-Initializing AudioProcessor...")
        #self.AudioCapture = AudioTools.MicrophoneAudioCapture()
        self.AudioCapture = AudioTools.SoundcardAudioCapture()
        self.AudioTransform = AudioTools.AudioTransform()
        InitEvent.publish(status="Complete", payload="Done.\n")

    def __call__(self):
        try:
            audio_data = self.AudioCapture()
            AudioChunk = self.AudioTransform(audio_data)
            return AudioChunk
        except Exception as e:
            ErrorEvent.publish(status="AudioChunk_FetchFailed", payload=e)
