from Controller.Handlers import *
from Visualizer import VisualBuilder
from OpenGL.GL import *
import numpy as np

class VisualProgramManager:
    def __init__(self, AudioChunk, CONFIG):
        
        InitEvent.publish(status="Initializing", payload="| |-Initializing VisualProgramManager...\n")
        self.VisualSerializer = VisualBuilder.VisualSerializer()
        self.VisualBuilder = VisualBuilder.VisualBuilder()
        self.VisualProgram = self.create_VisualProgram(AudioChunk, CONFIG)
        InitEvent.publish(status="Complete", payload="| | |/ VisualProgramManager Done.\n")

    def __call__(self, AudioChunk):
        self.VisualProgram.update_buffer(AudioChunk)
        self.VisualProgram.step_VisualProgram()
    
    def __del__(self):
        try:
            self.VisualProgram.delete()
        except Exception as e:
            ErrorEvent.publish(status="VisualProgram_DeleteFailed", payload=e)

    def create_VisualProgram(self, AudioChunk, CONFIG):
        try:
            keywords = CONFIG.model_dump()
            shader_source_list = self.VisualSerializer.load_shaders(CONFIG.SHADER_PATHS, keywords=keywords)
        except Exception as e:
            ErrorEvent.publish(status="VisualProgram_LoadShadersFailed", payload=e)
        try:
            VisualProgram = self.VisualBuilder.build(shader_source_list, AudioChunk)
            InitEvent.publish(status="VisualProgram_Created")
            return VisualProgram
        except Exception as e:
            ErrorEvent.publish(status="VisualProgram_BuildFailed", payload=e)
