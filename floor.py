import level
import random
from pathlib import Path

class Floor:
    def __init__(self, spritesheet, room_count):
        self.spritesheet = spritesheet
        self.generate_rooms(room_count)

    def generate_rooms(self, room_count):
        self.rooms = []

        dir_path = Path('assets/rooms')
        dir_path.mkdir(parents=True, exist_ok=True)

        start_files = [
            f for f in dir_path.iterdir()
            if f.is_file() and "start-" in f.name.lower()
        ]
        end_files = [
            f for f in dir_path.iterdir()
            if f.is_file() and "end-" in f.name.lower()
        ]
        middle_files = [
            f for f in dir_path.iterdir() 
            if f.is_file() 
            and not "start-" in f.name.lower() 
            and not "end-" in f.name.lower()
        ]


        if start_files:
            random_start_file = random.choice(start_files)
            room = level.Level.load(random_start_file, spritesheet=self.spritesheet)
            room.spawners = room.get_spawners()
            self.rooms.append(room)
        else:
            print("no start files!!")
            

        if not end_files:
            print("no end files..")

        i = 0
        while i < room_count + 1:
            files = end_files if i == room_count and end_files else middle_files
            random_room_file = random.choice(files)
            room = level.Level.load(random_room_file, spritesheet=self.spritesheet)

            old_room = self.rooms[-1]

            room.shift(
                old_room.tile_offset[0] + old_room.exit_pos[0] + 1 - room.enter_pos[0],
                old_room.tile_offset[1] + old_room.exit_pos[1] - room.enter_pos[1]
            )

            room.spawners = room.get_spawners()
            self.rooms.append(room)
            i+=1

    def find_room(self, player):
        for room in self.rooms:
            if room.bounds.collidepoint(player.collision_hitbox.center):
                return room

    def draw(self, screen, off_x = 0, off_y = 0):
        for room in self.rooms:
            room.draw(screen, off_x, off_y)

    def get_spawners(self):
        spawners = []
        for room in self.rooms:
            for spawner in room.spawners:
                spawners.append(spawner)
        return spawners

    def get_tiles(self):
        tiles = []
        for room in self.rooms:
            for tile in room.tiles:
                tiles.append(tile)
        return tiles