import game
import pygame

pygame.init()

from states.play_state import PlayState
from states.level_editor_state import LevelEditorState

g = game.Game()

states = {
    'play_state': PlayState(),
    'level_editor_state': LevelEditorState(),
}

g.begin(states, "play_state")
g.loop()