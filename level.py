import pygame
import json
from constants import *
from pathlib import Path


class Level():
    def __init__(self, w = 20, h = 12, tiles = {}, name = 'untitled'):
        #give levels names. make button and inputbox so that we can set the name, lvl w/h, and click open file button
        self.tiles = tiles
        self.w = w
        self.h = h
        self.name = name


    def draw(self, screen, off_x = 0, off_y = 0):
        for pos, tiletype in self.tiles.items():
            x, y = [int(x) for x in pos.split(",")]

            #debug
            if tiletype == "Ground":
                pygame.draw.rect(
                    screen, 
                    (0,0,255), 
                    (
                        x * TILE_SIZE + int(off_x), 
                        y * TILE_SIZE + int(off_y), 
                        TILE_SIZE, 
                        TILE_SIZE
                    )
                )
            #screen.blit

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