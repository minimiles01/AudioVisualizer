from Controller.Handlers import *
from Visualizer import VisualTools
from OpenGL.GL import *
import numpy as np

class VisualProgramManager:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="| |-Initializing VisualProgramManager...\n")
        
        self.VisualSerializer = VisualTools.VisualSerializer()
        self.VisualBuilder = VisualTools.VisualBuilder(serializer=self.VisualSerializer)
        self.VisualProgram = None

        InitEvent.publish(status="Complete", payload="| | |/ VisualProgramManager Done.\n")

    def __call__(self, AudioChunk):
        self.VisualProgram.update_buffer(AudioChunk)
        self.VisualProgram.step_VisualProgram()
    
    def __del__(self):
        try:
            self.VisualProgram.delete()
        except Exception as e:
            ErrorEvent.publish(status="VisualProgram_DeleteFailed", payload=e)

    def create_VisualProgram(self, shader_paths, AudioChunk):
        try:
            self.VisualProgram = self.VisualBuilder.build(shader_paths, AudioChunk)
            InitEvent.publish(status="VisualProgram_Created")
        except Exception as e:
            ErrorEvent.publish(status="VisualProgram_CreationFailed", payload=e)
