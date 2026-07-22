import pygame

class Game:
    def __init__(self, states):
        self.screen = pygame.display.set_mode((1000, 600))
        self.keep_playing = True
        self.clock = pygame.time.Clock()

        #state that we start with
        self.state_name = "play_state"
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
        self.state.draw(self.screen)
        pygame.display.update()
        