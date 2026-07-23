class Tile():
    def __init__(self, rect, sprite, type):
        self.rect = rect
        self.sprite = sprite
        self.type = type

class Torch(Tile):
    def __init__(self, rect, sprite, type):
        super().__init__(rect, sprite, type)
        self.time = 0

    def tick(self, dt):
        self.time += dt
        if self.time > 2:
            self.spawn()

    def spawn(self):
        pass