from .base_state import BaseState
import pygame
import parser

class PlayState(BaseState):
    def start(self, persistent_data):
        super.start(persistent_data)

    def draw(self, screen):
        screen.fill((0, 255, 0))
        screen.blit(parser.parse())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.next_state = "level_editor_state"
                self.done = True