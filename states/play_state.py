from .base_state import BaseState
from constants import *
import pygame
import player
import floor
import timer

pygame.display.init()

#notes to self:
#ONLY update room player is in. this will save SO much time
#ALSO only DRAW room player is in, + one after, + one before.
#ALSO make flameys spawn in their respective rooms.
#rooms are responsible for enemies they contain.

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
            
    def enter(self, persistent_data):
        super().enter(persistent_data)
        self.floor = floor.Floor(10)

        enter_pos = self.floor.rooms[0].enter_pos

        self.player = player.Player(
            (enter_pos[0] + 2) * TILE_SIZE,
            (enter_pos[1] - 1) * TILE_SIZE
        )
        self.timer = timer.Timer()


        self.cam_x = 0
        self.cam_y = 0
        self.cam_x_off = 0
        self.cam_y_off = 0

    def update(self, dt):
        self.timer.decrease(dt)
        if self.timer.has_ended:
            print("lose")
            self.next_state = "play_state"
            self.done = True

        tiles = self.floor.get_tiles()
        torches = self.floor.get_torches()

        self.player.update(dt, tiles)

        #"""
        for torch in torches:
            torch.tick(dt)
            for enemy in torch.enemies:
                enemy.update(dt, tiles)

        #camera
        cam_destination = (
            -self.player.rect.x + self.cam_x_off + (NATIVE_RESOLUTION[0] / 2) - 50,
            -self.player.rect.y + self.cam_y_off + (NATIVE_RESOLUTION[1] / 2) - 20,
        )
        cam_speed = 0.085
        self.cam_x += (cam_destination[0] - self.cam_x) * cam_speed
        self.cam_y += (cam_destination[1] - self.cam_y) * cam_speed
        
    def draw(self, screen):
        screen.fill((75, 61, 68))
                    
        self.floor.draw(screen, self.cam_x, self.cam_y)

        for room in self.floor.rooms:
            torches = room.torches
            for torch in torches:
                for enemy in torch.enemies:
                    enemy.draw(screen, self.spritesheet, self.cam_x, self.cam_y)

        timer_display = self.timer.get_display()
        timer_rect = timer_display.get_rect(center=(NATIVE_RESOLUTION[0] // 2, 32))
        screen.blit(timer_display, timer_rect)

        self.player.draw(screen, self.spritesheet, self.cam_x, self.cam_y)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "level_editor_state"
                self.done = True

        self.player.handle_event(event)