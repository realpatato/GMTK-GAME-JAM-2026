from .base_state import BaseState
import pygame
import level
import parser
import player
import level
import json

pygame.display.init()

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
        self.level = level.Level.load("test")
        self.player = player.Player()
        self.sprites = [self.player.sprite]

    def update(self, dt):
        self.player.h_move()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.player.inc_vel()
        elif keys[pygame.K_a]:
            self.player.inc_vel()
        else:
            if round(self.player.x_vel, 1) != 0:
                self.player.inc_vel()
            else:
                self.player.x_vel = 0
                if self.player.x_accel < 0:
                    self.player.sprite.state = "r_idle"
                else:
                    self.player.sprite.state = "l_idle"
            
    def enter(self, persistent_data):
        super().enter(persistent_data)

    def draw(self, screen):
        screen.fill((0, 255, 0))
        for sprite in self.sprites:
            if type(sprite) == parser.AnimatedSprite:
                sprite.advance()
            screen.blit(self.spritesheet, self.player.rect, sprite.rect())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "level_editor_state"
                self.done = True

            if event.key == pygame.K_d:
                self.player.x_accel = 0.1
                self.player.sprite.state = "r_walk"

            if event.key == pygame.K_a:
                self.player.x_accel = -0.1
                self.player.sprite.state = "l_walk"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                if self.player.x_vel > 0:
                    self.player.x_accel = -0.05

            if event.key == pygame.K_a:
                if self.player.x_vel < 0:
                    self.player.x_accel = 0.05