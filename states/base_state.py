class BaseState:
    def __init__(self):
        self.next_state = None
        self.done = False
        self.persist = {}

    def enter(self, persistent_data): 
        self.persist = persistent_data

    def leave(self):
        self.done = False
        return self.persist

    def handle_event(self, event): 
        pass

    def update(self, dt): 
        pass

    def draw(self, screen): 
        pass