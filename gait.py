from spider import Spider


class WalkingGait:
    def __init__(self, spider: Spider):
        self.spider = spider

    def walk_forward(self, stride_distance_cm=3):
        pass

    def walk_backward(self, stride_distance_cm=3):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass


class TripodGait(WalkingGait):
    def __init__(self, spider: Spider):
        super().__init__(spider)

    def walk_forward(self, stride_distance_cm=3):
        # Code to move three legs off ground at once
        pass