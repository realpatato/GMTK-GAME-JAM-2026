import game
import pygame

from states.play_state import PlayState
from states.level_editor_state import LevelEditorState

pygame.init()

game.Game({
    'play_state': PlayState(),
    'level_editor_state': LevelEditorState(),
}).loop()
