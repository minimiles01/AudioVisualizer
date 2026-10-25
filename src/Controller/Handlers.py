from dataclasses import dataclass
import inspect

class Event:
    _observers = set()

    @classmethod
    def subscribe(cls, observer_func):
        cls._observers.add(observer_func)

    @classmethod
    def unsubscribe(cls, observer_func):
        cls._observers.pop(observer_func, None)

    @classmethod
    def publish(cls, **kwargs):
        caller = inspect.currentframe().f_back.f_code.co_qualname
        for observer in cls._observers:
            event_instance = cls(caller=caller, **kwargs)
            observer(event_instance)

@dataclass
class InitEvent(Event):
    caller: str
    status: str
    payload: str | None = None

@dataclass
class RuntimeEvent(Event):
    caller: str
    status: str
    payload: str | None = None

@dataclass
class ErrorEvent(Event):
    caller: str
    status: str
    payload: str | None = None

class InitHandler:
    def __init__(self, Controller):
        self.Controller = Controller
        InitEvent.subscribe(self.print_init_payload)
        InitEvent.subscribe(self.handle_init_event)

    def print_init_payload(self, event: InitEvent):
        print(event.payload, end="")

    def handle_init_event(self, event: InitEvent):
        if event.caller == "<module>":
            if event.status == "Create_VisualProgram":
                self.Controller.Visualizer.VisualProgramManager.create_VisualProgram(event.payload)
        else:
            print(event.caller)

class RuntimeHandler:
    def __init__(self, Controller):
        self.Controller = Controller
        RuntimeEvent.subscribe(self.print_runtime_event)
        RuntimeEvent.subscribe(self.handle_runtime_event)

    def print_runtime_event(self, event: RuntimeEvent):
        print(event)

    def handle_runtime_event(self, event: RuntimeEvent):
        if event.caller == "WindowManger.__call__":
            if event.payload == "Quit":
                self.Controller.running = False
                
class ErrorHandler:
    def __init__(self, Controller):
        self.Controller = Controller