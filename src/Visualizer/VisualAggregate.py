from Controller.Handlers import *
from Visualizer import WindowManager
from Visualizer import VisualProgramManager

class VisualAggregate:
    def __init__(self, AudioChunk, CONFIG):
        InitEvent.publish(status="Initializing", payload="|-Initializing Visualizer...\n")
        self.WindowManager = WindowManager.WindowManger(CONFIG)
        self.VisualProgramManager = VisualProgramManager.VisualProgramManager(AudioChunk, CONFIG)
        InitEvent.publish(status="Complete", payload="| |/ Visualizer Done.\n")

    def __call__(self, AudioChunk):
        self.VisualProgramManager(AudioChunk)
        self.WindowManager()