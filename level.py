import pygame
import json
from constants import *
from pathlib import Path
from parser import Sprite

class Tile():
    def __init__(self, rect, sprite, type):
        self.rect = rect
        self.sprite = sprite
        self.type = type

class Level():
    def __init__(self, w = 20, h = 12, tiles = {}, name = 'untitled'):
        #give levels names. make button and inputbox so that we can set the name, lvl w/h, and click open file button
        self.tile_data = tiles
        self.w = w
        self.h = h
        self.name = name
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()

    def get_tiles(self):
        tiles = []
        for r in range(self.w):
            for c in range(self.h):
                key = str(r) + "," + str(c)
                if key in self.tile_data.keys():
                    if self.tile_data[key] == "Ground":
                        rect = pygame.Rect([r * TILE_SIZE, c * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                        sprite = Sprite([32, 0, 16, 16])
                        tiles.append(Tile(rect, sprite, "Ground"))
                    if self.tile_data[key] == "Enter":
                        rect = pygame.Rect([r * TILE_SIZE, c * TILE_SIZE, 0, 0])
                        sprite = Sprite([0, 0, 16, 16])
                        tiles.append(Tile(rect, sprite, "Enter"))
                    if self.tile_data[key] == "Exit":
                        rect = pygame.Rect([r * TILE_SIZE, c * TILE_SIZE, 0, 0])
                        sprite = Sprite([0, 0, 16, 16])
                        tiles.append(Tile(rect, sprite, "Exit"))
                else:
                    rect = pygame.Rect([r * TILE_SIZE, c * TILE_SIZE, 0, 0])
                    sprite = Sprite([0, 0, 16, 16])
                    tiles.append(Tile(rect, sprite, "None"))

        return tiles

    def draw(self, screen, off_x = 0, off_y = 0, edit = False):
        tiles = self.get_tiles()
        for tile in tiles:
            screen.blit(self.spritesheet, (tile.rect[0] + off_x, tile.rect[1] + off_y), tile.sprite.rect())
            if edit:
                if tile.type == "Exit":
                    pygame.draw.rect(screen, (255, 0, 0), (tile.rect[0] + off_x, tile.rect[1] + off_y, TILE_SIZE, TILE_SIZE))
                elif tile.type == "Enter":
                    pygame.draw.rect(screen, (0, 255, 0), (tile.rect[0] + off_x, tile.rect[1] + off_y, TILE_SIZE, TILE_SIZE))

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
                "tiles": self.tile_data
            }, f, indent=4) 
        print('saved to '+path)

def _get_path(filename):
    dir_path = Path('assets/rooms')
    dir_path.mkdir(parents=True, exist_ok=True)

    return f'assets/rooms/{filename}.json'