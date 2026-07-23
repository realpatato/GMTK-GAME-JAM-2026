from pygame import font

class Timer:
    def __init__(self):
        self.time = 30.00
        self.font = font.Font("assets/Bomby.ttf", 48)

    def get_display(self):
        return self.font.render(f"{self.time:.2f}", True, (255, 255, 255))

    def decrease(self, dec):
        self.time -= dec
        if self.time <= 0:
            self.lose()

    def lose(self):
        print("lose")