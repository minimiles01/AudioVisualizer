from Controller.Handlers import *

class VisualBuilder:
    def __init__(self, serializer):
        InitEvent.publish(status="Initializing", payload="| | |-Initializing VisualBuilder...")

        self.serializer = serializer

        InitEvent.publish(status="Complete", payload="Done.\n")

    def build(self, recipe_path):
        recipe = self.serializer.deserialize(recipe_path)

        #Build the actual VisualProgram object here
        
        pass

class VisualSerializer:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="| | |-Initializing VisualSerializer...")

        InitEvent.publish(status="Complete", payload="Done.\n")
