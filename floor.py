import level
import random
from pathlib import Path

class Floor:
    def __init__(self, room_count):
        self.rooms = []

        dir_path = Path('assets/rooms')
        dir_path.mkdir(parents=True, exist_ok=True)

        files = [entry for entry in dir_path.iterdir() if entry.is_file()]

        for i in range(room_count):
            random_room_file = random.choice(files)
            room = level.Level.load(random_room_file)

            if i > 0:
                old_room = self.rooms[-1]

                x_off = old_room.tile_offset[0] + old_room.exit_pos[0] + 1 - room.enter_pos[0]
                y_off = old_room.tile_offset[1] + old_room.exit_pos[1] - room.enter_pos[1]

                room.shift(x_off, y_off)

            room.torches = room.get_torches()
            self.rooms.append(room)
        

    def draw(self, screen, off_x = 0, off_y = 0):
        for room in self.rooms:
            room.draw(screen, off_x, off_y)

    def get_torches(self):
        torches = []
        for room in self.rooms:
            for torch in room.torches:
                torches.append(torch)
        return torches