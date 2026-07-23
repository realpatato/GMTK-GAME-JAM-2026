import pygame
import json
from constants import *
from pathlib import Path
from parser import Sprite

class Tile():
    def __init__(self, rect, sprite):
        self.rect = rect
        self.sprite = sprite

class Level():
    def __init__(self, w = 20, h = 12, tiles = {}, name = 'untitled'):
        #give levels names. make button and inputbox so that we can set the name, lvl w/h, and click open file button
        self.tiles = tiles
        self.w = w
        self.h = h
        self.name = name
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
        self.sprites, self.rects = self.get_tiles_and_rects()

    def get_tiles_and_rects(self):
        sprites = []
        rects = []
        for pos, tiletype in self.tiles.items():
            x, y = [int(x) for x in pos.split(",")]

            if tiletype == "Ground":
                rects.append(pygame.Rect([x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE]))
                sprites.append(Sprite([32, 0, 16, 16]))

        return sprites, rects

    def draw(self, screen, off_x = 0, off_y = 0):
        for sprite in self.sprites:
            index = self.sprites.index(sprite)
            screen.blit(self.spritesheet, self.rects[index], sprite.rect())

    @classmethod
    def load(cls, path):
        level_data = None
        with open(path, 'r') as f:
            level_data = json.load(f)
        if level_data:
            return cls(
                w= level_data["size"]["width"], 
                h= level_data["size"]["height"], 
                tiles= level_data["tiles"], 
                name= level_data["name"]
            )
        else:
            print('could not load file')

    def save(self):
        path = _get_path(self.name)

        with open(path, 'w') as f:
            json.dump({
                "name": self.name,
                "size": { "width": self.w, "height": self.h },
                "tiles": self.tiles
            }, f, indent=4) 
        print('saved to '+path)

def _get_path(filename):
    dir_path = Path('assets/rooms')
    dir_path.mkdir(parents=True, exist_ok=True)

    return f'assets/rooms/{filename}.json'