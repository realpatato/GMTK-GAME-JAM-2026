import pygame
#for things like text boxes, buttons, the likes

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x,y,w,h)

class InputBox:
    pass