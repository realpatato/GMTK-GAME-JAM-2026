class Sprite():
    def __init__(self, x, y, w, h, sf):
        self.rects = [(x * sf, y * sf, w * sf, h * sf)]

    def rect(self):
        return self.rects[0]

class AnimatedSprite(Sprite):
    def __init__(self, x, y, w, h, sf, ct):
        super().__init__(x, y, w, h)
        for i in range(ct - 1):
            self.rects.append((x + w * sf * i, y + h * sf * i, w * sf, h *sf))