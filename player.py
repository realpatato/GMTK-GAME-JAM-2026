import parser
from pygame import Rect

class Player():
    def __init__(self):
        self.sprite = self.gen_sprite()
        self.rect = Rect([32, 0, 32, 32])
        self.damage_hitbox = Rect([0, 0, 8, 16]) #in reference to player
        self.damage_hitbox_offsets = (12, 12)
        self.collision_hitbox = Rect([0, 0, 14, 16]) #in reference to player
        self.collision_hitbox_offsets = (9, 16)
        self.max_x_vel = 2.5
        self.x_accel = 0
        self.x_vel = 0

    def inc_vel(self):
        self.x_vel += self.x_accel
        if self.x_vel > self.max_x_vel:
            self.x_vel = self.max_x_vel
        elif self.x_vel < -self.max_x_vel:
            self.x_vel = -self.max_x_vel

    def h_move(self):
        self.rect.x += self.x_vel
        #update hitboxes
        self.collision_hitbox.x = self.rect.x + self.collision_hitbox_offsets[0]
        self.damage_hitbox.x = self.rect.x + self.damage_hitbox_offsets[0]

    def handle_x_collide(self, rect):
        if self.x_vel > 0:
            self.collision_hitbox.right = rect.left
        if self.x_vel < 0:
            self.collision_hitbox.left = rect.right
        self.x_vel = 0
        #update hitboxes
        self.rect.x = self.collision_hitbox.x - self.collision_hitbox_offsets[0]
        self.damage_hitbox.x = self.rect.x + self.damage_hitbox_offsets[0]

    def gen_sprite(self):
        anims = {"r_idle" : ((0, 2), 10), "r_walk" : ((1, 2, 3), 10), "l_idle" : ((7, 5), 10), "l_walk" : ((6, 5, 4), 10)}
        base_rect = [0, 16, 32, 32]
        return parser.AnimatedSprite(base_rect, 8, anims, "r_idle")