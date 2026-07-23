from enemy import Enemy

class Tile():
    def __init__(self, rect, sprite, type):
        self.rect = rect
        self.sprite = sprite
        self.type = type

class Torch(Tile):
    def __init__(self, rect, sprite, type):
        super().__init__(rect, sprite, type)
        self.time = 0
        self.enemies = []
        self.max_enemies = 5

    def tick(self, dt):
        self.time += dt
        if self.time > 2:
            if len(self.enemies) < self.max_enemies:
                self.spawn()
                self.time = 0

    def spawn(self):
        self.enemies.append(Enemy(self.rect[0], self.rect[1]))