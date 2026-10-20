from Visualizer import WindowManager
from Visualizer import VisualProgramManager

class VisualAggregate:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="|-Initializing Visualizer...\n")
        
        self.WindowManager = WindowManager.WindowManger()
        self.VisualProgramManager = VisualProgramManager.VisualProgramManager()

        InitEvent.publish(status="Complete", payload="| |/ Visualizer Done.\n")

    def __call__(self):
        self.VisualProgramManager()
        self.WindowManager()
