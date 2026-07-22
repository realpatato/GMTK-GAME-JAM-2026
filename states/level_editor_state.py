from .base_state import BaseState
import pygame

TILE_SIZE = 16 #pixels

class LevelEditorState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 30)

        self.cursor_x = 0
        self.cursor_y = 0

    def enter(self, persistent_data):
        super().enter(persistent_data)

    def update(self, dt):
        self.cursor_x, self.cursor_y = [
            x // TILE_SIZE for x in pygame.mouse.get_pos()
        ]

        print(self.cursor_x, self.cursor_y)

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
        pygame.draw.rect(screen, (255,255,255), (self.cursor_x * TILE_SIZE, self.cursor_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.next_state = "play_state"
                self.done = True