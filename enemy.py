import parser
from pygame import Rect

class Enemy():
    def __init__(self):
        self.sprite = self.gen_sprite()
        self.rect = Rect([128, 32, 16, 16])

        self.hitbox = Rect([0, 0, 8, 8])
        self.hitbox_offsets = (4, 8)

        self.attack_cycle = list(self.sprite.anims.keys())
        self.attack_phase = 3
        self.attack_frame = 0

        self.max_y_vel = 5
        self.y_accel = 0
        self.y_vel = 0

        self.max_x_vel = 2.5
        self.x_accel = 0
        self.x_vel = 0

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
            if self.attack_phase == 1:
                self.x_accel = -0.1
            else:
                self.x_accel = 0.1

    def inc_y_vel(self):
        self.y_vel += self.y_accel
        if self.y_vel > self.max_y_vel:
            self.y_vel = self.max_y_vel
        elif self.y_vel < -self.max_y_vel:
            self.y_vel = -self.max_y_vel

    def inc_x_vel(self):
        self.x_vel += self.x_accel
        if self.x_vel > self.max_x_vel:
            self.x_vel = self.max_x_vel
        elif self.x_vel < -self.max_x_vel:
            self.x_vel = -self.max_x_vel

    def v_move(self):
        self.rect.y += self.y_vel
        #update hitboxes
        self.hitbox.y = self.rect.y + self.hitbox_offsets[1]

    def h_move(self):
            self.rect.x += self.x_vel
            #update hitboxes
            self.hitbox.x = self.rect.x + self.hitbox_offsets[0]

    def handle_y_collide(self, rect):
        if self.y_vel > 0:
            self.hitbox.bottom = rect.top
            self.x_accel = 0
            self.x_vel = 0
        if self.y_vel < 0:
            self.hitbox.top = rect.bottom
        self.y_vel = 0
        #update hitboxes
        self.rect.y = self.hitbox.y - self.hitbox_offsets[1]

    def handle_x_collide(self, rect):
        if self.x_vel > 0:
            self.hitbox.right = rect.left
        if self.x_vel < 0:
            self.hitbox.left = rect.right
        self.x_vel *= -1

    def gen_sprite(self):
        anims = {"r_pre_jump" : ((1, -1), 30), "r" : ((0, -1), 360), "l_pre_jump" : ((2, -1), 30), "l" : ((3, -1), 360)}
        base_rect = [0, 48, 16, 16]
        return parser.AnimatedSprite(base_rect, 4, anims, "r")