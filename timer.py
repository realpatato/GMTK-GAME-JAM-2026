import pygame
from constants import *

class Timer:
    def __init__(self):
        self.total_time = 30.00
        self.time = self.total_time
        self.font = pygame.font.Font("assets/Bomby.ttf", 48)

        self.has_ended = False

    def get_display(self):
        text = self.font.render(f"{self.time:.2f}",True,self.get_color())
        outline = self.font.render(f"{self.time:.2f}",True,BACKGROUND_COLOR)

        surface = pygame.Surface(
            (text.get_width() + 2, text.get_height() + 2),
            pygame.SRCALPHA
        )

        surface.blit(outline, (0, 1))
        surface.blit(outline, (2, 1))
        surface.blit(outline, (1, 0))
        surface.blit(outline, (1, 2))

        surface.blit(text, (1, 1))

        return surface

    def decrease(self, dec):
        if not self.has_ended:
            self.time -= dec
            if self.time <= 0:
                self.time = 0
                self.has_ended = True

    def get_color(self):
        start = OFFWHITE_COLOR
        end = (255, 0, 0) 

        ratio = min(1.0, max(0.0, (10 - self.time) / 10))

        return tuple(
            int(start[i] + (end[i] - start[i]) * ratio)
            for i in range(3)
        )