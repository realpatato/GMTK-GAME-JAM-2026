from .base_state import BaseState
from constants import *
import pygame
import player
import floor
import timer
import random

pygame.display.init()

#notes to self:
#ONLY update room player is in. this will save SO much time
#ALSO only DRAW room player is in, + one after, + one before.
#ALSO make flameys spawn in their respective rooms.
#rooms are responsible for enemies they contain.

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/bomby_sprite_sheet.png").convert_alpha()
        pygame.mixer.init()
        self.sounds = {
            "jump": pygame.mixer.Sound("assets/sounds/jump.ogg"),
            "die": pygame.mixer.Sound("assets/sounds/explosion.ogg"),
            "parry": pygame.mixer.Sound("assets/sounds/parry.ogg"),
            "gaintime": pygame.mixer.Sound("assets/sounds/hitEnemy.ogg"),
            "nextfloor": pygame.mixer.Sound("assets/sounds/powerUp.ogg"),
            "losetime": pygame.mixer.Sound("assets/sounds/hitHurt.ogg"),
            "bounce": pygame.mixer.Sound("assets/sounds/footstep.ogg"),
        }
            
    def enter(self, persistent_data):
        super().enter(persistent_data)

        self.timer = timer.Timer()
        self.player = player.Player(sounds = self.sounds)

        self.cam_x = 0
        self.cam_y = 0
        self.cam_x_off = 0
        self.cam_y_off = 0

        self.base_room_count = 3
        self.room_count_mult_per_floor = 1.3 #keep increasing by this factor
        self.current_room_count = self.base_room_count


        pygame.mixer.music.load(f'assets/music/floorvariant{random.randint(1,3)}.ogg')
        pygame.mixer.music.play(-1, 0.0)
        self.volume = 1

        self.paused = False

        self.next_floor()

    def next_floor(self):
        
        print(f'current floor has {self.current_room_count} rooms!!')
        self.floor = floor.Floor(
            self.spritesheet,
            int(self.current_room_count)
        )

        enter_pos = self.floor.rooms[0].enter_pos
        self.player.move(
            (enter_pos[0] - 0.5) * TILE_SIZE,
            (enter_pos[1] - 1) * TILE_SIZE
        )

        self.current_room = None

        #used to see if we reached the last room
        self.prev_room = None

    def update(self, dt):
        if self.paused: return
        
        pygame.mixer.music.set_volume(self.volume)
        if (
            self.current_room is None 
            or not self.current_room.bounds.collidepoint(
                self.player.collision_hitbox.center 
            )
        ):
            self.prev_room = self.current_room
            self.current_room = self.floor.find_room(self.player)
            if self.current_room is None and self.prev_room == self.floor.rooms[-1]:

                self.current_room_count = (
                    self.current_room_count * self.room_count_mult_per_floor
                )
                
                self.timer.time += 5

                old_x = self.player.rect.x
                old_y = self.player.rect.y

                self.next_floor()
                self.sounds["nextfloor"].play()
                dx = self.player.rect.x - old_x
                dy = self.player.rect.y - old_y

                self.cam_x -= dx
                self.cam_y -= dy
                return

        tiles = []
        spawners = []
        if self.current_room:
            tiles = self.current_room.create_tile_objs()
            spawners = self.current_room.get_spawners()

        for spawner in spawners:
            spawner.tick(dt)
            for enemy in spawner.enemies:
                enemy.update(dt, tiles)

        res = self.player.update(dt, tiles, 
            [enemy for spawner in spawners for enemy in spawner.enemies],
            self.timer
        )

        if res == "END":
            self.next_state = "mainmenu_state"
            self.done = True
            pygame.mixer.music.fadeout(1)

        #"""
        #camera
        cam_destination = (
            -self.player.rect.x + self.cam_x_off + (NATIVE_RESOLUTION[0] / 2) - 50,
            -self.player.rect.y + self.cam_y_off + (NATIVE_RESOLUTION[1] / 2) - 20,
        )
        cam_speed = 0.085
        self.cam_x += (cam_destination[0] - self.cam_x) * cam_speed
        self.cam_y += (cam_destination[1] - self.cam_y) * cam_speed
        
        self.timer.decrease(dt)
        if self.current_room is None:
            self.timer.time = 0
            '''
        if self.timer.has_ended:
            self.next_state = "mainmenu_state"
            self.done = True'''
        
    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
                    
        self.floor.draw(screen, self.cam_x, self.cam_y)

        for room in self.floor.rooms:
            for spawner in room.spawners:
                for enemy in spawner.enemies:
                    enemy.draw(screen, self.spritesheet, self.cam_x, self.cam_y)

        timer_display = self.timer.get_display()
        timer_rect = timer_display.get_rect(center=(NATIVE_RESOLUTION[0] // 2, 32))
        screen.blit(timer_display, timer_rect)

        self.player.draw(screen, self.spritesheet, self.cam_x, self.cam_y, self.timer)

        
        if self.paused: 
            overlay = pygame.Surface(NATIVE_RESOLUTION, pygame.SRCALPHA)
            pygame.draw.rect(overlay, (*BACKGROUND_COLOR, 200), (0, 0, NATIVE_RESOLUTION[0], NATIVE_RESOLUTION[1]))
            screen.blit(overlay,(0,0))
            screen.blit(self.timer.font.render("YOU ARE PAUSED", True,OFFWHITE_COLOR), (0,150))
            return

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            inc = 0.2
            if event.key == pygame.K_EQUALS:
                self.volume = min(1, self.volume + inc)
            if event.key == pygame.K_MINUS:
                self.volume = max(0, self.volume - inc)

            if event.key == pygame.K_RETURN:
                self.paused = not self.paused
                if self.paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            if self.paused:
                if event.key == pygame.K_ESCAPE:
                    self.next_state="mainmenu_state"
                    self.done = True

                if event.key == pygame.K_r:
                    self.next_state ="play_state"
                    self.done = True

        self.player.handle_event(event)