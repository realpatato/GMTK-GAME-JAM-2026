import parser
from pygame import Rect, key, draw
import random
from pygame.locals import *

class Player():
    def __init__(self, x = 32, y = 0, sounds = {}):
        self.sprite = self.gen_sprite()
        self.rect = Rect([x, y, 32, 32])

        self.sounds = sounds

        self.damage_hitbox = Rect([0, 0, 8, 16])
        self.damage_hitbox_offsets = (12, 12)

        self.collision_hitbox = Rect([0, 0, 14, 16])
        self.collision_hitbox_offsets = (9, 16)

        self.parry_hitbox = Rect([0, 0, 18, 26])
        self.parry_hitbox_offsets = (6, 9)

        self.friction = 0.93

        self.coyote_time_max = 0.18 # seconds until you can no longer jump with coyote time
        self.coyote_time = 0

        self.grounded = False

        self.can_jump = False
        self.jump_height = 4
        self.jump_accel = 0.1
        self.fall_accel = 0.21

        self.iframes = 90
        self.iframes_elapsed = 0
        self.invincible = False

        self.can_parry = False
        self.is_parrying = False
        self.parry_duration = 0.12
        self.parry_elapsed = 0
        self.parry_cooldown_duration = 0.8
        self.parry_cooldown_elapsed = 0

        self.max_x_vel = 3.7
        self.x_accel = 0
        self.x_vel = 0

        self.max_y_vel = 7
        self.y_accel = 0
        self.y_vel = 0

        self.death_sprite = self.gen_death_sprite()
        self.death_over = False
        self.death_sound_played = False

    def play_sound(self, sound):
        if sound not in self.sounds:
            print('sound'+sound+' dont exist')

        self.sounds[sound].play()

    def move(self, x, y):
        self.rect.topleft = (x, y)
        self.collision_hitbox.topleft = (
            x + self.collision_hitbox_offsets[0], 
            y + self.collision_hitbox_offsets[1]
        )
        self.damage_hitbox.topleft = (
            x + self.damage_hitbox_offsets[0], 
            y + self.damage_hitbox_offsets[1]
        )
        self.parry_hitbox.topleft = (
            x + self.parry_hitbox_offsets[0],
            y + self.parry_hitbox_offsets[1]
        )

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                if self.can_jump:
                    self.can_jump = False
                    self.coyote_time = 0
                    self.y_vel = -self.jump_height
                    self.play_sound("jump")
                elif self.can_parry:
                    self.can_parry = False
                    self.is_parrying = True
                    self.parry_elapsed = 0
                    self.play_sound("parry")

        if event.type == KEYUP:
            if event.key == K_w or event.key == K_UP:
                if self.y_vel < -0.5:
                    self.y_vel = -0.5


    def update(self, dt, tiles, enemies, timer):
        if timer.has_ended:
            if not self.death_sound_played:
                self.play_sound("die")
                self.death_sound_played = True
            return self.death_sprite.advance(True)
        
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

        if self.is_parrying:
            self.parry_elapsed+=dt
            self.parry_cooldown_elapsed = 0
            if self.parry_elapsed >= self.parry_duration:
                self.is_parrying = False

            #actually parry
            parried_enemies = self.parry_hitbox.collidelistall(
                [enemy.hitbox for enemy in enemies]
            )
            if len(parried_enemies)>0:
                #PARRIED
                enemy = enemies[parried_enemies[0]]
                enemy.should_die = True
                self.y_vel = -self.jump_height
                self.play_sound("gaintime")
                self.x_vel *= 2
                timer.time += enemy.reward_time
        else:
            self.parry_cooldown_elapsed+=dt
            if self.parry_cooldown_elapsed >= self.parry_cooldown_duration:
                self.can_parry = True

        if self.grounded:
            self.parry_cooldown_elapsed = self.parry_cooldown_duration
            self.is_parrying = False
            self.can_parry = False
            
        keys = key.get_pressed()
        if keys[K_d] or keys[K_RIGHT]:
            self.inc_x_vel()
            self.sprite.state = "r_walk"
        elif keys[K_a] or keys[K_LEFT]:
            self.inc_x_vel()
            self.sprite.state = "l_walk"
        else:
            #no matter if this is positive or negative, just bring it down by this factor
            self.x_vel *= self.friction

            if abs(self.x_vel) < 0.3:
                if self.x_accel < 0:
                    self.sprite.state = "r_idle"
                else:
                    self.sprite.state = "l_idle"

        if self.is_parrying:
            self.sprite.state = "parry"

        self.y_accel = self.fall_accel
        if (keys[K_w] or keys[K_UP]) and self.y_vel < 0:
            self.y_accel = self.jump_accel
        self.inc_y_vel()
        

        if self.invincible:
            self.iframes_elapsed+=1
            if self.iframes_elapsed>self.iframes:
                self.invincible =False
                self.iframes_elapsed = 0
        else:
            #getting hurt
            attacking_enemies = self.damage_hitbox.collidelistall(
                [enemy.hitbox for enemy in enemies]
            )
            
            if len(attacking_enemies)>0:
                enemy = enemies[attacking_enemies[0]]
                self.y_vel = -1 * (random.randint(15, 35) / 10)
                self.x_vel = (random.randint(0, 1)* 2 -1) * 3
                self.play_sound("losetime")
                self.invincible = True

                timer.time -= enemy.penalty_time

        self.sprite.advance()

    def draw(self, screen, spritesheet, off_x, off_y, timer):
        if not timer.has_ended:
            if self.invincible:
                if (self.iframes_elapsed // 4) % 2 == 1:
                    screen.blit(spritesheet, self.rect.move(off_x, off_y), self.sprite.rect())
                return
            screen.blit(spritesheet, self.rect.move(off_x, off_y), self.sprite.rect())
        else:
            screen.blit(spritesheet, self.rect.move(off_x, off_y), self.death_sprite.rect())
            #draw.rect(screen, (0, 255,0), self.collision_hitbox.move(off_x,off_y))
            #draw.rect(screen, (255, 0,0), self.damage_hitbox.move(off_x,off_y))


    def inc_x_vel(self):
        keys = key.get_pressed()
        r = keys[K_d] or keys[K_RIGHT]
        l = keys[K_a] or keys[K_LEFT]

        direction = (r - l) 
        self.x_accel = direction * 0.1
        accel = self.x_accel
        
        if abs(self.x_vel) < self.max_x_vel or self.x_vel * direction < 0:
            if self.grounded:
                accel *= 2
            self.x_vel += accel

        if self.x_vel > self.max_x_vel:
            self.x_vel = max(self.max_x_vel, self.x_vel - 0.09)
        elif self.x_vel < -self.max_x_vel:
            self.x_vel = min(-self.max_x_vel, self.x_vel + 0.09)

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
        self.parry_hitbox.x = self.rect.x + self.parry_hitbox_offsets[0]

    def v_move(self):
        self.rect.y += self.y_vel
        #update hitboxes
        self.collision_hitbox.y = self.rect.y + self.collision_hitbox_offsets[1]
        self.damage_hitbox.y = self.rect.y + self.damage_hitbox_offsets[1]
        self.parry_hitbox.y = self.rect.y + self.parry_hitbox_offsets[1]

    def handle_x_collide(self, rect):
        if self.x_vel > 0:
            self.collision_hitbox.right = rect.left
        if self.x_vel < 0:
            self.collision_hitbox.left = rect.right
        #hi this makes you bounce off walls! to undo this make it 0
        self.x_vel *= -0.4

        #update hitboxes
        self.rect.x = self.collision_hitbox.x - self.collision_hitbox_offsets[0]
        self.damage_hitbox.x = self.rect.x + self.damage_hitbox_offsets[0]
        self.parry_hitbox.y = self.rect.x + self.parry_hitbox_offsets[0]

    def handle_y_collide(self, rect):
        if self.y_vel > 0:
            self.collision_hitbox.bottom = rect.top
        if self.y_vel < 0:
            self.collision_hitbox.top = rect.bottom
        self.y_vel = 0
        #update hitboxes
        self.rect.y = self.collision_hitbox.y - self.collision_hitbox_offsets[1]
        self.damage_hitbox.y = self.rect.y + self.damage_hitbox_offsets[1]
        self.parry_hitbox.y = self.rect.y + self.parry_hitbox_offsets[1]

    def gen_sprite(self):
        anims = {
            "r_idle" : ((0, 2), 10), 
            "r_walk" : ((1, 2, 3), 10), 
            "l_idle" : ((7, 5), 10), 
            "l_walk" : ((6, 5, 4), 10),
            "parry" : ((8, 8), 10),
        }
        base_rect = [0, 16, 32, 32]
        return parser.AnimatedSprite(base_rect, 9, anims, "r_idle")

    def gen_death_sprite(self):
        anims = {
            "explode" : ((0, 1, 2, 3,0, 1, 2, 3,0, 1, 2, 3), 3)
        }
        base_rect = [0, 64, 32, 32]
        return parser.AnimatedSprite(base_rect, 4, anims, "explode")