from Controller.Handlers import *
from Visualizer import VisualTools

class VisualProgramManager:
    def __init__(self):
        pass
        InitEvent.publish(status="Initializing", payload="| |-Initializing VisualProgramManager...\n")
        
        self.VisualSerializer = VisualTools.VisualSerializer()
        self.VisualBuilder = VisualTools.VisualBuilder(serializer=self.VisualSerializer)
        self.VisualPrograms = {}

        InitEvent.publish(status="Complete", payload="| | |/ VisualProgramManager Done.\n")

    def create_VisualProgram(self, VisualRecipe_paths):
        pass
        for VisualRecipe_path in VisualRecipe_paths:
            try:
                self.VisualPrograms[VisualRecipe_paths] = self.VisualBuilder.build(VisualRecipe_path)
                RuntimeEvent.publish(status="Running", payload=str(VisualRecipe_path)+" VisualProgram created.\n")
            except:
                ErrorEvent.publish(status="VisualProgram_CreationFailed", payload=str(VisualRecipe_path)+" VisualProgram creation failed.\n")

    def delete_VisualProgram(self, VisualRecipe_paths):
        pass
        for VisualRecipe_path, VisualProgram in self.VisualPrograms.items():
            try:
                _ = self.VisualPrograms.pop(VisualRecipe_paths, None)
                RuntimeEvent.publish(status="Running", payload=str(VisualRecipe_path)+" VisualProgram deleted.\n")
            except:
                ErrorEvent.publish(status="VisualProgram_DeletionFailed", payload=str(VisualRecipe_path)+" VisualProgram deletion failed.\n")

    def __call__(self, AudioChunk):
        for VisualRecipe_path, VisualProgram in self.VisualPrograms.items():
            VisualProgram(AudioChunk)
