import parser
from pygame import Rect

class Enemy():
    def __init__(self):
        self.sprite = parser.Sprite
        self.rect = Rect([128, 32, 16, 16])

    def gen_sprite(self):
        anims = {"r_pre_jump" : ((1), 5), "r" : ((0), 5), "l_pre_jump" : ((2), 5), "l" : ((3), 5)}
        base_rect = [0, 48, 16, 16]
        return parser.AnimatedSprite(base_rect, 4, anims, "r")