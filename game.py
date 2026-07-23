import pygame
from constants import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.native_screen = pygame.Surface(NATIVE_RESOLUTION)
        self.keep_playing = True
        self.clock = pygame.time.Clock()


    def begin(self, states, start_state):
        self.state_name = start_state
        self.states = states
        self.state = self.states[self.state_name]
        
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
            if event.type == pygame.QUIT:
                self.keep_playing = False

            self.state.handle_event(event)

    def update(self, dt):
        if self.state.done: 
            self.set_state()
        self.state.update(dt) 
                
    def set_state(self):        
        persistent_data = self.state.leave()
        self.state_name = self.state.next_state
        self.state = self.states[self.state_name]
        self.state.enter(persistent_data)

    def draw(self):
        # draw things here
        self.state.draw(self.native_screen)

        self.screen.blit(
            pygame.transform.scale(self.native_screen, WINDOW_SIZE), (0, 0)
        )

        pygame.display.update()
        