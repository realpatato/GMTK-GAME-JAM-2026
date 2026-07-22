import pygame
import json
from constants import *
from pathlib import Path


class Level():
    def __init__(self, tiles = {}):
        #give levels names. make button and inputbox so that we can set the name, lvl w/h, and click open file button
        self.tiles = tiles
        self.w = 20
        self.h = 12
        self.name = 'untitled'


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

    def save(self, filename):
        dir_path = Path('assets/rooms')
        dir_path.mkdir(parents=True, exist_ok=True)

        path = f'assets/rooms/{filename}.json'

        with open(path, 'w') as f:
            json.dump({
                "name": filename,
                "size": { "width": self.w, "height": self.h },
                "tiles": self.tiles
            }, f, indent=4) 
        print('saved to '+path)