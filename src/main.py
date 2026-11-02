from Controller.Handlers import *
from Controller import ControllerAggregate

if __name__ == "__main__":
    controller = ControllerAggregate.ControllerAggregate(config_paths=["Recipes/test4.json"])
    controller.run()