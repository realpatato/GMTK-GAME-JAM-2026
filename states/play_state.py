from .base_state import BaseState
import pygame
import parser

pygame.display.init()

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()

    def enter(self, persistent_data):
        super().enter(persistent_data)

    def draw(self, screen):
        screen.fill((0, 255, 0))
        bomby = parser.Sprite(0, 16, 32, 32, self.sssf)
        screen.blit(self.spritesheet, (0, 0), bomby.rect())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.next_state = "level_editor_state"
                self.done = True