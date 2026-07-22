from .base_state import BaseState
import pygame

class PlayState(BaseState):
    def draw(self, screen):
        screen.fill((0, 255, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.next_state = "level_editor_state"
                self.done = True