from .base_state import BaseState
from level import Level
import pygame
from gui import *
from constants import *
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

class LevelEditorState(BaseState):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font('assets/Bomby.ttf', 12)

        self.level = Level()

        self.gui = {
            "level title": InputBox(30, 1, 60, self.font, "untitled"),
            "level width": InputBox(128, 1, 22, self.font, "20"),
            "level height": InputBox(196, 1, 22, self.font, "12"),
        }
        self.focused_gui = None

        self.tile_type_i = 0

        self.cursor_x = 0
        self.cursor_y = 0

        self.cam_x = 0
        self.cam_y = 0

    def enter(self, persistent_data):
        super().enter(persistent_data)

    def update(self, dt):

        if self.focused_gui:
            self.focused_gui.update(dt)
        self.level.name = self.gui["level title"].get_value() or "untitled"

        w_value = self.gui["level width"].get_value()
        if w_value.isdigit(): self.level.w = int(w_value)
        h_value = self.gui["level height"].get_value()
        if h_value.isdigit(): self.level.h = int(h_value)

        # place thigns
        if not self.focused_gui:
            if (
                    0 <= self.cursor_x < self.level.w 
                and 0 <= self.cursor_y < self.level.h
            ):
                x, y = int(self.cursor_x), int(self.cursor_y)
                key = f'{x},{y}'
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:
                    self.level.tile_data[key] = TILE_TYPES[self.tile_type_i % len(TILE_TYPES)]
                if mouse_buttons[2]:
                    if key in self.level.tile_data:
                        del self.level.tile_data[key]

    def draw(self, screen):
        screen.fill((0, 0, 0))

        #draw levle
        self.level.draw(screen, math.floor(self.cam_x), math.floor(self.cam_y), True)

        # cursor 
        rect_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        rect_surface.fill((255, 255, 255, 64)) 
        screen.blit(
            rect_surface, 
            (
                self.cursor_x * TILE_SIZE + math.floor(self.cam_x), 
                self.cursor_y * TILE_SIZE + math.floor(self.cam_y)
            )
        )



        #info text
        screen.blit(self.font.render("name:", True, (255, 255, 255)),(0, 1))
        screen.blit(self.font.render("width:", True, (255, 255, 255)),(90, 1))
        screen.blit(self.font.render("height:", True, (255, 255, 255)),(150, 1))

        screen.blit(self.font.render("tile type: "+TILE_TYPES[self.tile_type_i % len(TILE_TYPES)], True, (255, 255, 255)),(150, 16))

        for elmnt in self.gui.values():
            elmnt.draw(screen, self.focused_gui == elmnt)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            mouse_x /= SCALE_FACTOR
            mouse_y /= SCALE_FACTOR
            self.cursor_x, self.cursor_y = [
                (mouse_x - self.cam_x) // TILE_SIZE,
                (mouse_y - self.cam_y) // TILE_SIZE
            ]
            self.focused_gui = next(
                (
                    elmnt 
                    for elmnt in self.gui.values()
                        if elmnt.rect.collidepoint((mouse_x, mouse_y))
                ), 
                None
            )

        #GUI HANDLE EVENT
        if self.focused_gui:
            self.focused_gui.handle_event(event)
            return

        #STATE EVENTS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "play_state"
                self.done = True

            if event.key == pygame.K_UP:
                self.tile_type_i+=1
            if event.key == pygame.K_DOWN:
                self.tile_type_i-=1

                #clear
            if event.key == pygame.K_0:
                self.level = Level()

            #load
            if event.key == pygame.K_BACKSLASH:
                file_path = filedialog.askopenfilename()
                if isinstance(file_path, str):
                    self.level = Level.load(file_path)
                else: print("something went wrong ok?")

            if event.key == pygame.K_RETURN:
                self.level.save()

        if event.type == pygame.MOUSEMOTION:
            # event.rel returns the (x, y) distance moved since the last event
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[1]:
                dx, dy = [x / SCALE_FACTOR for x in event.rel] 

                self.cam_x += dx
                self.cam_y += dy

            