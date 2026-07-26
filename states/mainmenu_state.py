from .base_state import BaseState
import pygame
from constants import *

class MainMenuState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("assets/Bomby.ttf", 48)
            
    def enter(self, persistent_data):
        super().enter(persistent_data)

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)


        screen.blit(
            self.font.render(f"BOMBY - THE GAME", True, OFFWHITE_COLOR), 
            (0,0)
        )
        screen.blit(
            self.font.render(f"ENTER TO BEGIN", True, OFFWHITE_COLOR), 
            (0,200)
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_state = "play_state"
                self.done = True
            if event.key == pygame.K_ESCAPE:
                self.next_state = "level_editor_state"
                self.done = True