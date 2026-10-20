from Controller.Handlers import *
from Controller import ControllerAggregate

if __name__ == "__main__":
    controller = ControllerAggregate.ControllerAggregate()

    #Change this to an InitEvent and write startup logic
    RuntimeEvent.publish(status="Create_VisualProgram", payload="VisualRecipes/recipe1.json")
    
    controller.run()