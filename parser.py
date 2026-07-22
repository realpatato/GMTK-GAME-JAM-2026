class Sprite():
    def __init__(self, x, y, w, h):
        self.rects = [(x, y, w, h)]

    def rect(self):
        return self.rects[0]

class Animation():
    def __init__(self, frames, frame_time):
        self.frames = frames
        self.ct = 0
        self.frame_time = frame_time
        self.current_frame_index = 0

    def advance(self):
        self.ct += 1
        if self.ct == self.frame_time:
            self.current_frame_index += 1
            self.ct = 0

    def rect(self):
        return self.frames[self.current_frame_index % len(self.frames)]

class AnimatedSprite(Sprite):
    def __init__(self, x, y, w, h, ct, anims = {}, state = "None"):
        super().__init__(x, y, w, h)
        for i in range(1, ct):
            self.rects.append((x + w * i, y, w, h))
        self.state = state
        self.anims = anims
        if len(self.anims.items()) == 0:
            self.anims["None"] = Animation(self.rects, 10)
        else:
            for key in anims:
                frames = []
                for i in self.anims[key][0]:
                    frames.append(self.rects[i])
                self.anims[key] = Animation(frames, self.anims[key][1])
                print(self.anims)

    def advance(self):
        self.anims[self.state].advance()

    def rect(self):
        return self.anims[self.state].rect()