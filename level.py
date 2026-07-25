import pygame
import json
from constants import *
from pathlib import Path
from parser import Sprite
from tile import *

class Level():
    def __init__(self, w = 20, h = 12, tiles = {}, name = 'untitled', tile_offset = [0,0]):
        #give levels names. make button and inputbox so that we can set the name, lvl w/h, and click open file button
        self.tile_data = tiles
        self.w = w
        self.h = h
        self.name = name
        self.spritesheet = pygame.image.load("assets/Spritesheet.png").convert_alpha()
        self.tile_offset = tile_offset
        self.tiles = self.create_tile_objs()
        self.spawners = self.get_spawners()

        #to make things easy store start and exit when level is created
        self.enter_pos = None
        self.exit_pos = None
        self.update_enter_exit_pos()

        #store a rect that contains the bounds of the room to see what room player is in
        self.update_bounds()

    def update_bounds(self):
        self.bounds = pygame.Rect(
            self.tile_offset[0] * TILE_SIZE,
            self.tile_offset[1] * TILE_SIZE,
            self.w * TILE_SIZE,
            self.h * TILE_SIZE
        )

    def update_enter_exit_pos(self):
        for key, value in self.tile_data.items():
            x, y = map(int, key.split(","))

            if value == "Enter":
                self.enter_pos = (x, y)
            elif value == "Exit":
                self.exit_pos = (x, y)


    def create_tile_objs(self):
        tiles = []
        for r in range(self.w):
            for c in range(self.h):
                key = str(r) + "," + str(c)
                y = r + self.tile_offset[0]
                x = c + self.tile_offset[1]
                if key in self.tile_data.keys():
                    if self.tile_data[key] == "Ground":
                        rect = pygame.Rect([y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE])
                        sprite = Sprite([32, 0, 16, 16])
                        tiles.append(Tile(rect, sprite, "Ground"))
                    if self.tile_data[key] == "Enter":
                        rect = pygame.Rect([y * TILE_SIZE, x * TILE_SIZE, 0, 0])
                        sprite = Sprite([0, 0, 16, 16])
                        tiles.append(Tile(rect, sprite, "Enter"))
                    if self.tile_data[key] == "Exit":
                        rect = pygame.Rect([y * TILE_SIZE, x * TILE_SIZE, 0, 0])
                        sprite = Sprite([0, 0, 16, 16])
                        tiles.append(Tile(rect, sprite, "Exit"))
                    if self.tile_data[key] == "Torch":
                        rect = pygame.Rect([y * TILE_SIZE, x * TILE_SIZE, 0, 0])
                        sprite = Sprite([16, 0, 16, 16])
                        tiles.append(Tile(rect, Sprite([0, 0, 16, 16]), "None"))
                        tiles.append(Torch(rect, sprite, "Torch"))        
                    if self.tile_data[key] == "Faucet":
                        rect = pygame.Rect([y * TILE_SIZE, x * TILE_SIZE, 0, 0])
                        sprite = Sprite([48, 0, 16, 16])
                        tiles.append(Tile(rect, Sprite([0, 0, 16, 16]), "None"))
                        tiles.append(Faucet(rect, sprite, "Faucet"))     
                else:
                    rect = pygame.Rect([y * TILE_SIZE, x * TILE_SIZE, 0, 0])
                    sprite = Sprite([0, 0, 16, 16])
                    tiles.append(Tile(rect, sprite, "None"))

        return tiles

    def get_spawners(self):
        return [s for s in self.tiles if isinstance(s, Spawner)]

    def draw(self, screen, off_x = 0, off_y = 0, edit = False):
        tiles = self.tiles
        for tile in tiles:
            screen.blit(self.spritesheet, (tile.rect[0] + off_x, tile.rect[1] + off_y), tile.sprite.rect())
            if edit:
                if tile.type == "Exit":
                    pygame.draw.rect(screen, (255, 0, 0), (tile.rect[0] + off_x, tile.rect[1] + off_y, TILE_SIZE, TILE_SIZE))
                elif tile.type == "Enter":
                    pygame.draw.rect(screen, (0, 255, 0), (tile.rect[0] + off_x, tile.rect[1] + off_y, TILE_SIZE, TILE_SIZE))

    def shift(self, x,y):
        self.tile_offset =[x,y]
        self.update_bounds()
        self.tiles = self.create_tile_objs()

    @classmethod
    def load(cls, path, offset=[0,0]):
        level_data = None
        with open(path, 'r') as f:
            level_data = json.load(f)
        if level_data:
            return cls(
                w= level_data["size"]["width"], 
                h= level_data["size"]["height"], 
                tiles= level_data["tiles"], 
                name= level_data["name"],
                tile_offset= offset
            )
        else:
            print('could not load file')

    def save(self):
        self.update_enter_exit_pos()
        if "end-" in self.name:
            if self.enter_pos is None:
                print("Could not save-- set ENTER pos!!")
                return
        else:
            if self.exit_pos is None or self.enter_pos is None:
                print("Could not save-- set enter and exit positions!!")
                return
        
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