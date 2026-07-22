import parser

class Player():
    def __init__(self):
        self.sprite = self.gen_sprite()
        self.pos = [0, 0]
        self.damage_hitbox = [12, 12, 8, 16]
        self.collision_hitbox = [9, 16, 14, 16]
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
        self.pos[0] += self.x_vel

    def gen_sprite(self):
        anims = {"r_idle" : ((0, 2), 10), "r_walk" : ((1, 2, 3), 10), "l_idle" : ((7, 5), 10), "l_walk" : ((6, 5, 4), 10)}
        base_rect = [0, 16, 32, 32]
        return parser.AnimatedSprite(base_rect, 8, anims, "r_idle")