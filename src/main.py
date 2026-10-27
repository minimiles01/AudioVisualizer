from Controller.Handlers import *
from Controller import ControllerAggregate

if __name__ == "__main__":
    controller = ControllerAggregate.ControllerAggregate()

    shader_paths = [("src/shaders/simple_vertex.glsl", "VERTEX"), ("src/shaders/test3.glsl", "FRAGMENT")]
    InitEvent.publish(status="Create_VisualProgram", payload=shader_paths)

    controller.run()