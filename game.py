import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        self.keep_playing = True
        self.clock = pygame.time.Clock()
    def loop(self):
        dt = 0

        while self.keep_playing:
            
            self.handle_events()
            self.update(dt)
            self.draw()

            dt = self.clock.tick(60) / 1000

        pygame.quit()
        quit()
            

    def handle_events(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                self.keep_playing = False

    def update(self, dt):
        print(dt)

    def draw(self):
        # draw things here

        pygame.display.update()
        