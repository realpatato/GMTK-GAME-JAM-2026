import level
import random
from pathlib import Path

class Floor:
    def __init__(self, room_count):
        self.rooms = []
        
        #    level.Level.load("assets/rooms/test.json"),
        #    level.Level.load("assets/rooms/big drop.json")
        #self.rooms[1].shift(20, -1)


        dir_path = Path('assets/rooms')
        dir_path.mkdir(parents=True, exist_ok=True)

        files = [entry for entry in dir_path.iterdir() if entry.is_file()]
        for i in range(room_count):
            random_room_file = random.choice(files)

            unpositioned_room = level.Level.load(random_room_file)

            total_x_off = 0
            total_y_off = 0

            # offset for each previous room that exists
            for i in range(len(self.rooms)-1):
                l_room = self.rooms[i]
                r_room = self.rooms[i+1]

                exit_pos = next((k for k, v in l_room.tile_data.items() if v == "Exit"), None)
                enter_pos = next((k for k, v in r_room.tile_data.items() if v == "Enter"), None)

                enter_x, enter_y = [int(x) for x in enter_pos.split(",")]
                exit_x, exit_y = [int(x) for x in exit_pos.split(",")]

                total_x_off += (exit_x + 1) - enter_x
                total_y_off += (exit_y) - enter_y

                print(f'{enter_x}]{enter_y}')
                print(f'{exit_x}]{exit_y}')

            unpositioned_room.shift(total_x_off, total_y_off)
            self.rooms.append(unpositioned_room)

            print(random_room_file)  # Prints the full path to the file
        

    def draw(self, screen, off_x = 0, off_y = 0):
        for room in self.rooms:
            room.draw(screen, off_x, off_y)

    def get_torches(self):
        torches = []
        for room in self.rooms:
            for torch in room.torches:
                torches.append(torch)
        return torches