from .base_state import BaseState
import pygame

class LevelEditorState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 30)

    def enter(self, persistent_data):
        super().enter(persistent_data)
        

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # Step 2: Render the text into a Surface object
        # (text, antialiasing, color)
        text_surface = self.font.render('Welcome to Level Editor', True, (255, 255, 255))

        # Step 3: Copy (blit) the text surface onto your main screen
        screen.blit(text_surface, (50, 50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.next_state = "play_state"
                self.done = True