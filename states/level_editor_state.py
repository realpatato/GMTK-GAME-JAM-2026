from .base_state import BaseState
import pygame
from constants import *

class LevelEditorState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font('assets/Bomby.ttf', 16)

        self.cursor_x = 0
        self.cursor_y = 0

    def enter(self, persistent_data):
        super().enter(persistent_data)

    def update(self, dt):
        self.cursor_x, self.cursor_y = [
            (x / SCALE_FACTOR) // TILE_SIZE for x in pygame.mouse.get_pos()
        ]

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(
            self.font.render(
                'Welcome to Level Editor', 
                True, 
                (255, 255, 255)
            ),
            (0, 0)
        )

        rect_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        rect_surface.fill((255, 255, 255, 128)) 
        screen.blit(
            rect_surface, 
            (
                self.cursor_x * TILE_SIZE, 
                self.cursor_y * TILE_SIZE, 
            )
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "play_state"
                self.done = True