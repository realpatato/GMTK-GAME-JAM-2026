import parser
from pygame import Rect, key
from pygame.locals import *

class Player():
    def __init__(self, x = 32, y = 0):
        self.sprite = self.gen_sprite()
        self.rect = Rect([x, y, 32, 32])

        self.damage_hitbox = Rect([0, 0, 8, 16])
        self.damage_hitbox_offsets = (12, 12)

        self.collision_hitbox = Rect([0, 0, 14, 16])
        self.collision_hitbox_offsets = (9, 16)

        self.friction = 0.93

        self.coyote_time_max = 0.18 # seconds until you can no longer jump with coyote time
        self.coyote_time = self.coyote_time_max

        self.grounded = False
        self.can_jump = False

        self.jump_height = 4
        self.jump_accel = 0.1
        self.fall_accel = 0.21

        self.max_x_vel = 2.5
        self.x_accel = 0
        self.x_vel = 0

        self.max_y_vel = 7
        self.y_accel = 0
        self.y_vel = 0

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_d or event.key == K_RIGHT:
                self.x_accel = 0.1
                self.sprite.state = "r_walk"

            if event.key == K_a or event.key == K_LEFT:
                self.x_accel = -0.1
                self.sprite.state = "l_walk"

            if event.key == K_w or event.key == K_UP:
                if self.can_jump:
                    self.can_jump = False
                    self.coyote_time = 0
                    self.y_vel = -self.jump_height

        if event.type == KEYUP:
            if event.key == K_d or event.key == K_RIGHT:
                if self.x_vel > 0:
                    self.x_accel = -0.05

            if event.key == K_a or event.key == K_LEFT:
                if self.x_vel < 0:
                    self.x_accel = 0.05

            if event.key == K_w or event.key == K_UP:
                if self.y_vel < -0.5:
                    self.y_vel = -0.5


    def update(self, dt, tiles):
        self.v_move()
        y_collide = self.collision_hitbox.collideobjects(tiles, key=lambda o : o.rect)
        if y_collide:
            self.handle_y_collide(y_collide.rect)

        self.h_move()
        x_collide = self.collision_hitbox.collideobjects(tiles, key=lambda o : o.rect)
        if x_collide:
            self.handle_x_collide(x_collide.rect)

        ground_check = self.collision_hitbox.copy()
        ground_check.y += 1
        self.grounded = any(ground_check.colliderect(tile) for tile in tiles)

        if self.grounded:
            self.coyote_time = self.coyote_time_max
        else:
            self.coyote_time-=dt

        self.can_jump = self.grounded
        if self.coyote_time > 0:
            self.can_jump = True

        keys = key.get_pressed()
        if keys[K_d] or keys[K_RIGHT]:
            self.inc_x_vel()
        elif keys[K_a] or keys[K_LEFT]:
            self.inc_x_vel()
        else:
            #no matter if this is positive or negative, just bring it down by this factor
            self.x_vel *= self.friction

            if abs(self.x_vel) < 0.3:
                if self.x_accel < 0:
                    self.sprite.state = "r_idle"
                else:
                    self.sprite.state = "l_idle"

        self.y_accel = self.fall_accel
        if (keys[K_w] or keys[K_UP]) and self.y_vel < 0:
            self.y_accel = self.jump_accel
        self.inc_y_vel()

        self.sprite.advance()

    def draw(self, screen, spritesheet, off_x, off_y):
        screen.blit(spritesheet, self.rect.move(off_x, off_y), self.sprite.rect())

    def inc_x_vel(self):
        self.x_vel += self.x_accel
        if self.x_vel > self.max_x_vel:
            self.x_vel = self.max_x_vel
        elif self.x_vel < -self.max_x_vel:
            self.x_vel = -self.max_x_vel

    def inc_y_vel(self):
        self.y_vel += self.y_accel
        if self.y_vel > self.max_y_vel:
            self.y_vel = self.max_y_vel
        elif self.y_vel < -self.max_y_vel:
            self.y_vel = -self.max_y_vel

    def h_move(self):
        self.rect.x += self.x_vel
        #update hitboxes
        self.collision_hitbox.x = self.rect.x + self.collision_hitbox_offsets[0]
        self.damage_hitbox.x = self.rect.x + self.damage_hitbox_offsets[0]

    def v_move(self):
        self.rect.y += self.y_vel
        #update hitboxes
        self.collision_hitbox.y = self.rect.y + self.collision_hitbox_offsets[1]
        self.damage_hitbox.y = self.rect.y + self.damage_hitbox_offsets[1]

    def handle_x_collide(self, rect):
        if self.x_vel > 0:
            self.collision_hitbox.right = rect.left
        if self.x_vel < 0:
            self.collision_hitbox.left = rect.right
        #hi this makes you bounce off walls! to undo this make it 0
        self.x_vel *= -1.1

        #update hitboxes
        self.rect.x = self.collision_hitbox.x - self.collision_hitbox_offsets[0]
        self.damage_hitbox.x = self.rect.x + self.damage_hitbox_offsets[0]

    def handle_y_collide(self, rect):
        if self.y_vel > 0:
            self.collision_hitbox.bottom = rect.top
        if self.y_vel < 0:
            self.collision_hitbox.top = rect.bottom
        self.y_vel = 0
        #update hitboxes
        self.rect.y = self.collision_hitbox.y - self.collision_hitbox_offsets[1]
        self.damage_hitbox.y = self.rect.y + self.damage_hitbox_offsets[1]

    def gen_sprite(self):
        anims = {"r_idle" : ((0, 2), 10), "r_walk" : ((1, 2, 3), 10), "l_idle" : ((7, 5), 10), "l_walk" : ((6, 5, 4), 10)}
        base_rect = [0, 16, 32, 32]
        return parser.AnimatedSprite(base_rect, 8, anims, "r_idle")