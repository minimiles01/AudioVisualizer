from Controller.Handlers import *
from AudioProcessor import AudioTransform
from AudioProcessor import AudioSource

class AudioProcessorAggregate:
    def __init__(self, CONFIG):

        InitEvent.publish(status="Initializing", payload="|-Initializing AudioProcessor...")
        if CONFIG.AUDIO_SOURCE == "SPEAKER":
            self.AudioCapture = AudioSource.SoundcardAudioCapture(CONFIG)
        elif CONFIG.AUDIO_SOURCE == "MICROPHONE":
            self.AudioCapture = AudioSource.MicrophoneAudioCapture(CONFIG)
        self.AudioTransform = AudioTransform.AudioTransform(CONFIG)
        InitEvent.publish(status="Complete", payload="Done.\n")

    def __call__(self):
        try:
            audio_data = self.AudioCapture()
            AudioChunk = self.AudioTransform(audio_data)
            return AudioChunk
        except Exception as e:
            ErrorEvent.publish(status="AudioChunk_FetchFailed", payload=e)
