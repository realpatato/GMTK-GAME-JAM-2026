from pygame import font

class Timer:
    def __init__(self):
        self.time = 30.00
        self.font = font.Font("assets/Bomby.ttf", 48)

    def get_display(self):
        return self.font.render(f"{self.time:.2f}", True, self.get_color())

    def decrease(self, dec):
        self.time -= dec
        if self.time <= 0:
            self.time = 0
            self.lose()

    def get_color(self):
        if self.time < 5:
            return (255, 51 * self.time, 51 * self.time)
        else:
            return (255, 255, 255)

    def lose(self):
        print("lose")