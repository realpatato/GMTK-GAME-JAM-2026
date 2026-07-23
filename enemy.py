import parser
from pygame import Rect

class Enemy():
    def __init__(self):
        self.sprite = self.gen_sprite()
        self.rect = Rect([0, 0, 16, 16])

        self.hitbox = Rect([0, 0, 8, 8])
        self.hitbox_offsets = (4, 8)

        self.attack_cycle = list(self.sprite.anims.keys())
        self.attack_phase = 3
        self.attack_frame = 0

        self.max_y_vel = 5
        self.y_accel = 0
        self.y_vel = 0

    def advance(self):
        self.attack_frame = self.sprite.advance()
        if self.attack_frame == 0:
            self.attack_phase += 1
            if self.attack_phase == len(self.attack_cycle):
                self.attack_phase = 0
            self.sprite.state = self.attack_cycle[self.attack_phase]
            self.handle_switch()

    def handle_switch(self):
        if self.attack_phase == 1 or self.attack_phase == 3:
            self.y_accel = -5

    def inc_y_vel(self):
        self.y_vel += self.y_accel
        if self.y_vel > self.max_y_vel:
            self.y_vel = self.max_y_vel
        elif self.y_vel < -self.max_y_vel:
            self.y_vel = -self.max_y_vel

    def gen_sprite(self):
        anims = {"r_pre_jump" : ((1, -1), 30), "r" : ((0, -1), 360), "l_pre_jump" : ((2, -1), 30), "l" : ((3, -1), 360)}
        base_rect = [0, 48, 16, 16]
        return parser.AnimatedSprite(base_rect, 4, anims, "r")