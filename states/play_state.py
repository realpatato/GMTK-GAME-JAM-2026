from .base_state import BaseState
import pygame
import level
import parser
import player
import level

pygame.display.init()

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
        self.level = level.Level.load("assets/rooms/test.json")
        self.player = player.Player()
        self.sprites = [self.player.sprite]

    def update(self, dt):
        self.player.v_move()

        y_collide = self.player.collision_hitbox.collidelist(self.level.rects)

        if y_collide != -1:
            self.player.handle_y_collide(self.level.rects[y_collide])

        self.player.h_move()

        x_collide = self.player.collision_hitbox.collidelist(self.level.rects)

        if x_collide != -1:
            self.player.handle_x_collide(self.level.rects[x_collide])

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.inc_x_vel()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.inc_x_vel()
        else:
            if round(self.player.x_vel, 1) != 0:
                self.player.inc_x_vel()
            else:
                self.player.x_vel = 0
                if self.player.x_accel < 0:
                    self.player.sprite.state = "r_idle"
                else:
                    self.player.sprite.state = "l_idle"
        self.player.inc_y_vel()
        self.player.y_accel = 0.1    
            
    def enter(self, persistent_data):
        super().enter(persistent_data)

    def draw(self, screen):
        screen.fill((0, 255, 0))
        self.level.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), self.player.collision_hitbox, 2)
        for sprite in self.sprites:
            if type(sprite) == parser.AnimatedSprite:
                sprite.advance()
            screen.blit(self.spritesheet, self.player.rect, sprite.rect())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "level_editor_state"
                self.done = True

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.x_accel = 0.1
                self.player.sprite.state = "r_walk"

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.x_accel = -0.1
                self.player.sprite.state = "l_walk"

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.player.grounded:
                    self.player.y_accel = -5
                self.player.grounded = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if self.player.x_vel > 0:
                    self.player.x_accel = -0.05

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if self.player.x_vel < 0:
                    self.player.x_accel = 0.05

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.player.y_vel < 0:
                    self.player.y_vel = 0