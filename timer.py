class Timer:
    def __init__(self):
        self.time = 30

    def decrease(self, dec):
        self.time -= dec
        if self.time <= 0:
            self.lose()

    def lose(self):
        print("lose")