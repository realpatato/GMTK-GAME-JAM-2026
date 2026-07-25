from enemies import *

class Tile():
    def __init__(self, rect, sprite, type):
        self.rect = rect
        self.sprite = sprite
        self.type = type

class Spawner(Tile):
    pass

class Torch(Spawner):
    def __init__(self, rect, sprite, type):
        super().__init__(rect, sprite, type)
        self.time = 0
        self.enemies = []
        self.max_enemies = 5
        self.enemies_has_spawned = 0

    def tick(self, dt):
        for enemy in self.enemies:
            if enemy.should_die:
                self.enemies.remove(enemy)
                
        self.time += dt
        if self.time > 2:
            if self.enemies_has_spawned < self.max_enemies:
                self.spawn()
                self.time = 0

    def spawn(self):
        self.enemies_has_spawned += 1
        self.enemies.append(Flamey(self.rect[0], self.rect[1]))

class Faucet(Spawner):
    def __init__(self, rect, sprite, type):
        super().__init__(rect, sprite, type)
        self.time = 0
        self.enemies = []
        self.max_enemies = 2

    def tick(self, dt):
        self.time += dt
        if self.time > 3:
            if len(self.enemies) < self.max_enemies:
                self.spawn()
                self.time = 0

    def spawn(self):
        self.enemies.append(WaterBlob(self.rect[0], self.rect[1]))