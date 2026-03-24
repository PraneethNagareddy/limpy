from core.spider import Spider



class WalkingGait:
    def __init__(self):
        self.spider = Spider.get()

    def walk_forward(self, stride_distance_cm=3):
        pass

    def walk_backward(self, stride_distance_cm=3):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def step_left(self):
        pass

    def step_right(self):
        pass

    def walk_omni(self, x: float, y: float, stride_factor: float = 1.0):
        pass

    def turn_omni(self, rx: float, ry: float, turn_factor: float = 1.0):
        pass