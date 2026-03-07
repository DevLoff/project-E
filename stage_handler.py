from pygame import Surface,Vector2

class StageHandler():
    def __init__(self):
        self.currentStage : dict

    def update(self) -> None:
        pass

    def execute(self) -> None:
        pass

    def render(self) -> Surface:
        return Surface(Vector2()) #temporary