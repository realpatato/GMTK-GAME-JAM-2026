from .base_state import BaseState
import pygame
import parser

pygame.display.init()

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
        bomby = parser.AnimatedSprite(0, 16, 32, 32, 4, {"idle" : ((0, 2), 10), "walk" : ((1, 2, 3), 10)}, "idle")
        self.animated_sprites = [bomby]
        self.sprites = [bomby]

    def enter(self, persistent_data):
        super().enter(persistent_data)

    def draw(self, screen):
        screen.fill((0, 255, 0))
        for sprite in self.animated_sprites:
            sprite.advance()
        for sprite in self.sprites:
            screen.blit(self.spritesheet, (0, 0), sprite.rect())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.next_state = "level_editor_state"
                self.done = True

            if event.key == pygame.K_d:
                self.animated_sprites[0].state = "idle" if self.animated_sprites[0].state == "walk" else "walk"