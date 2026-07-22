from pygame import (Surface, image)

class Sprite():
    def parse(self, y, w, ct):
        spritesheet = image.load("assets/Spritesheet.png")
        sprites = []
        for i in range(ct):
            sprite = Surface((w, w))
            sprite.blit(spritesheet, (16 * y, w * i))
        return sprites

class LevelSprites(Sprite):
    def __init__(self):
        self.sprites = super().parse(0, 16, 3)