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
        # torches = self.floor.get_torches()

        self.player.v_move()

        """
        for torch in torches:
            torch.tick(dt)
            for enemy in torch.enemies:
                enemy.v_move()
        """

        y_collide = self.player.collision_hitbox.collideobjects(tiles, key=lambda o : o.rect)
        if y_collide:
            self.player.handle_y_collide(y_collide.rect)

            y_collide = self.player.collision_hitbox.collideobjects(tiles, key=lambda o : o.rect)
            if y_collide:
                self.player.handle_y_collide(y_collide.rect)

        """
            for torch in torches:
                for enemy in torch.enemies:
                    #print(enemy)
                    y_collide = enemy.hitbox.collideobjects(tiles, key=lambda o : o.rect)
                    if y_collide:
                        enemy.handle_y_collide(y_collide.rect)
        """

        self.player.h_move()

        """
        for torch in torches:
            for enemy in torch.enemies:
                enemy.h_move()
        """

        """
        for torch in torches:
            for enemy in torch.enemies:
                x_collide = enemy.hitbox.collideobjects(tiles, key=lambda o : o.rect)
                if x_collide:
                    enemy.handle_x_collide(x_collide.rect)
        """

        x_collide = self.player.collision_hitbox.collideobjects(tiles, key=lambda o : o.rect)
        if x_collide:
            self.player.handle_x_collide(x_collide.rect)

        """
            for torch in torches:
                for enemy in torch.enemies:
                    x_collide = enemy.hitbox.collideobjects(tiles, key=lambda o : o.rect)
                    if x_collide:
                        enemy.handle_x_collide(x_collide.rect)
        """
        #camera
        cam_destination = (
            -self.player.rect.x + self.cam_x_off + (NATIVE_RESOLUTION[0] / 2) - 50,
            -self.player.rect.y + self.cam_y_off + (NATIVE_RESOLUTION[1] / 2) - 20,
        )
        cam_speed = 0.085
        self.cam_x += (cam_destination[0] - self.cam_x) * cam_speed
        self.cam_y += (cam_destination[1] - self.cam_y) * cam_speed

        keys = pygame.key.get_pressed()
        if keys[pygame.K_l]:
            self.cam_x_off-=5
        if keys[pygame.K_j]:
            self.cam_x_off+=5
        if keys[pygame.K_i]:
            self.cam_y_off+=5
        if keys[pygame.K_k]:
            self.cam_y_off-=5

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.inc_x_vel()
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.inc_x_vel()
        else:
            if round(self.player.x_vel, 1) != 0:
                self.player.inc_x_vel()
            else:
                self.player.x_vel = 0
                if self.player.x_accel < 0:
                    self.player.sprite.state = "r_idle"
                else:
                    self.player.sprite.state = "l_idle"
        
        self.player.inc_y_vel()
        self.player.y_accel = 0.1

        """
        for room in self.floor.rooms:
            torches = room.torches
            
            for torch in torches:
                for enemy in torch.enemies:
                    enemy.inc_y_vel()
                    enemy.inc_x_vel()
                    enemy.y_accel = 0.1
        """

    def draw(self, screen):
        screen.fill((75, 61, 68))
                    
        self.floor.draw(screen, self.cam_x, self.cam_y)
        """
        for room in self.floor.rooms:
            torches = room.torches
            for torch in torches:
                for enemy in torch.enemies:
                    enemy.advance()
                    screen.blit(self.spritesheet, enemy.rect.move(self.cam_x, self.cam_y), enemy.sprite.rect())
        """

        timer_display = self.timer.get_display()
        timer_rect = timer_display.get_rect(center=(NATIVE_RESOLUTION[0] // 2, 32))
        screen.blit(timer_display, timer_rect)

        self.player.sprite.advance()
        screen.blit(self.spritesheet, self.player.rect.move(self.cam_x,self.cam_y), self.player.sprite.rect())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "level_editor_state"
                self.done = True

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.x_accel = 0.1
                self.player.sprite.state = "r_walk"

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.x_accel = -0.1
                self.player.sprite.state = "l_walk"

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.player.grounded:
                    self.player.y_accel = -5
                self.player.grounded = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if self.player.x_vel > 0:
                    self.player.x_accel = -0.05

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if self.player.x_vel < 0:
                    self.player.x_accel = 0.05

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.player.y_vel < 0:
                    self.player.y_vel = 0