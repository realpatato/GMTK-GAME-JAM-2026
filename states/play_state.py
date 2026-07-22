from .base_state import BaseState
import pygame
import parser
import player

pygame.display.init()

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
        self.player = player.Player()
        self.sprites = [self.player.sprite]

    def enter(self, persistent_data):
        super().enter(persistent_data)

    def draw(self, screen):
        screen.fill((0, 255, 0))
        for sprite in self.sprites:
            if type(sprite) == parser.AnimatedSprite:
                sprite.advance()
            screen.blit(self.spritesheet, (0, 0), sprite.rect())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.next_state = "level_editor_state"
                self.done = True

            if event.key == pygame.K_d:
                self.player.sprite.state = "idle" if self.player.sprite.state == "walk" else "walk"