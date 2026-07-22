from .base_state import BaseState
import pygame
import parser

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
        self.sssf = 2
        self.spritesheet = pygame.transform.scale_by(self.spritesheet, self.sssf)

    def enter(self, persistent_data):
        super().enter(persistent_data)

    def draw(self, screen):
        screen.fill((0, 255, 0))
        bg = parser.Sprite(0, 0, 16, 16, self.ssf)
        screen.blit(self.spritesheet, (0, 0), bg.rect())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.next_state = "level_editor_state"
                self.done = True