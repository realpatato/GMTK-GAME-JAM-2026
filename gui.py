import pygame
#for things like text boxes, buttons, the likes

class Gui:
    def __init__():
        pass
    def handle_event(self, event):
        pass
    def update(self, dt):
        pass
    def draw(self, screen):
        pass

class InputBox(Gui):
    def __init__(self, x, y, w, font, placeholder_text = ''):
        self.placeholder_text = placeholder_text
        self.text = ''
        self.font = font
        self.placeholder_image = font.render(placeholder_text, True, (160, 160, 160))
        h = self.placeholder_image.get_height()
        self.rect = pygame.Rect(x,y,w,h+2)

    def get_value(self):
        return self.text

    def update(self, dt):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return
            self.text += event.unicode

    def draw(self, screen, focused):
        if focused:
            pygame.draw.rect(screen, (64, 64, 64), self.rect)
            pygame.draw.rect(screen, (96, 96, 96), self.rect, 1)
        else:
            pygame.draw.rect(screen, (32, 32, 32), self.rect)
            pygame.draw.rect(screen, (48, 48, 48), self.rect, 1)
        if not self.text:
            screen.blit(self.placeholder_image, (self.rect.x+2, self.rect.y))
        else:
            screen.blit(
                self.font.render(self.text, True, (255, 255, 255)),
                (self.rect.x+2, self.rect.y)
            )