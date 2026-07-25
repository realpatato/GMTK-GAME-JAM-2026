from pygame import font

class Timer:
    def __init__(self):
        self.total_time = 30.00
        self.time = self.total_time
        self.font = font.Font("assets/Bomby.ttf", 48)

        self.has_ended = False

    def get_display(self):
        return self.font.render(f"{self.time:.2f}", True, self.get_color())

    def decrease(self, dec):
        if not self.has_ended:
            self.time -= dec
            if self.time <= 0:
                self.time = 0
                self.has_ended = True

    def get_color(self):
        ratio = min(1.0, max(0.0, self.time / (self.total_time - 10)))
        return (255, 200 * ratio + 50, 200 * ratio + 50)