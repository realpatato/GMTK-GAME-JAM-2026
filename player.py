import parser

class Player():
    def __init__(self):
        self.sprite = self.gen_sprite()
        self.hitbox = []

    def gen_sprite(self):
        anims = {"idle" : ((0, 2), 10), "walk" : ((1, 2, 3), 10)}
        base_rect = [0, 16, 32, 32] #spritesheet position
        return parser.AnimatedSprite(base_rect, 4, anims, "idle")