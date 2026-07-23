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

        total_x_off = 0
        total_y_off = 0
        for i in range(room_count):
            random_room_file = random.choice(files)

            room = level.Level.load(random_room_file)

            #subtract our position
            exit_pos = [
                int(x) for x in
                next((k for k, v in room.tile_data.items() if v == "Exit"), None)
                .split(",")
            ]
            enter_pos = [
                int(x) for x in
                next((k for k, v in room.tile_data.items() if v == "Enter"), None)
                .split(",")
            ]

            room.shift(total_x_off, total_y_off)
            total_x_off += exit_pos[0] + 1
            if (i > 0 and self.rooms[i-1]):
                old_room = self.rooms[i-1]
                old_exit_pos = [
                    int(x) for x in
                    next((k for k, v in old_room.tile_data.items() if v == "Exit"), None)
                    .split(",")
                ]
                old_enter_pos = [
                    int(x) for x in
                    next((k for k, v in old_room.tile_data.items() if v == "Enter"), None)
                    .split(",")
                ]
                total_y_off += enter_pos[1] - old_exit_pos[1]

            #add our positions

            self.rooms.append(room)

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