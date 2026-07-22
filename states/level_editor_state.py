from .base_state import BaseState
from level import Level
import pygame
from constants import *

class LevelEditorState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font('assets/Bomby.ttf', 16)

        self.level = Level()

        self.tile_type = "Ground"

        self.cursor_x = 0
        self.cursor_y = 0

        self.cam_x = 0
        self.cam_y = 0

    def enter(self, persistent_data):
        super().enter(persistent_data)

    def update(self, dt):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.cursor_x, self.cursor_y = [
            ((mouse_x / SCALE_FACTOR) - self.cam_x) // TILE_SIZE,
            ((mouse_y / SCALE_FACTOR) - self.cam_y) // TILE_SIZE
        ]

    def draw(self, screen):
        screen.fill((0, 0, 0))

        pygame.draw.rect(
            screen, 
            (40, 40, 40), 
            (
                self.cam_x, 
                self.cam_y, 
                self.level.w * TILE_SIZE, 
                self.level.h * TILE_SIZE
            )
        )

        #draw levle
        self.level.draw(screen, self.cam_x, self.cam_y)

        # cursor 
        rect_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        rect_surface.fill((255, 255, 255, 64)) 
        screen.blit(
            rect_surface, 
            (
                self.cursor_x * TILE_SIZE + self.cam_x, 
                self.cursor_y * TILE_SIZE + self.cam_y
            )
        )

    
        # place thigns
        if 0 <= self.cursor_x < self.level.w and 0 <= self.cursor_y < self.level.h:
            x, y = int(self.cursor_x), int(self.cursor_y)
            key = f'{x},{y}'
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                self.level.tiles[key] = self.tile_type
            if mouse_buttons[2]:
                if key in self.level.tiles:
                    del self.level.tiles[key]



        #info text
        screen.blit(
            self.font.render(
                f'{self.level.name} (width: {self.level.w}, height: {self.level.h})', 
                True, 
                (255, 255, 255)
            ),
            (0, 0)
        )


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "play_state"
                self.done = True

            if event.key == pygame.K_RETURN:
                self.level.save(self.level.name)

        if event.type == pygame.MOUSEMOTION:
            # event.rel returns the (x, y) distance moved since the last event
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[1]:
                dx, dy = [x / SCALE_FACTOR for x in event.rel] 

                self.cam_x += dx
                self.cam_y += dy

            