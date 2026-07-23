from .base_state import BaseState
import pygame
import level
import parser
import player
import enemy
import level

pygame.display.init()

class PlayState(BaseState):
    def __init__(self):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
        self.levels = [
            level.Level.load("assets/rooms/test.json"),
            level.Level.load("assets/rooms/big drop.json", (20, 0))
        ]
        self.player = player.Player()
        self.enemy = enemy.Enemy()
        self.enemies = [self.enemy]

        self.cam_x = 0
        self.cam_y = 0

    def update(self, dt):
        self.player.v_move()
        for enemy in self.enemies:
            enemy.v_move()
        for level in self.levels:
            tiles = level.get_tiles()

            y_collide = self.player.collision_hitbox.collideobjects(tiles, key=lambda o : o.rect)
            if y_collide:
                self.player.handle_y_collide(y_collide.rect)

            for enemy in self.enemies:
                y_collide = enemy.hitbox.collideobjects(tiles, key=lambda o : o.rect)
                if y_collide:
                    self.enemy.handle_y_collide(y_collide.rect)

        self.player.h_move()
        for enemy in self.enemies:
            enemy.h_move()
        for level in self.levels:
            tiles = level.get_tiles()

            x_collide = self.player.collision_hitbox.collideobjects(tiles, key=lambda o : o.rect)
            if x_collide:
                self.player.handle_x_collide(x_collide.rect)

            for enemy in self.enemies:
                x_collide = enemy.hitbox.collideobjects(tiles, key=lambda o : o.rect)
                if x_collide:
                    self.enemy.handle_x_collide(x_collide.rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_l]:
            self.cam_x-=5
        if keys[pygame.K_j]:
            self.cam_x+=5
        if keys[pygame.K_i]:
            self.cam_y-=5
        if keys[pygame.K_k]:
            self.cam_y+=5

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

        for enemy in self.enemies:
            enemy.inc_y_vel()
            enemy.inc_x_vel()
            enemy.y_accel = 0.1
            
    def enter(self, persistent_data):
        super().enter(persistent_data)

    def draw(self, screen):
        screen.fill((0, 255, 0))
        for level in self.levels:
            level.draw(screen, self.cam_x, self.cam_y)
        pygame.draw.rect(
            screen, 
            (255, 0, 0), 
            self.player.collision_hitbox.move(self.cam_x,self.cam_y), 
            2
        )
        self.player.sprite.advance()
        screen.blit(self.spritesheet, self.player.rect, self.player.sprite.rect())
        for enemy in self.enemies:
            enemy.advance()
            pygame.draw.rect(screen, (255, 0, 0), enemy.hitbox, 2)
            screen.blit(self.spritesheet, enemy.rect, enemy.sprite.rect())

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