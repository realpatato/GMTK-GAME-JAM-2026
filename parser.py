class Sprite():
    def __init__(self, x, y, w, h):
        self.rects = [(x, y, w, h)]

class AnimatedSprite(Sprite):
    def __init__(self, x, y, w, h, ct):
        super().__init__(x, y, w, h)
        for i in range(ct - 1):
            self.rects.append((x + w * i, y + h * i, w, h))