from Controller.Handlers import *
from Controller import ControllerAggregate

if __name__ == "__main__":
    controller = ControllerAggregate.ControllerAggregate(
        config_paths=["Recipes/simple_circle.json"])
    #    config_paths=["Recipes/simple_line.json"])
    controller.run()