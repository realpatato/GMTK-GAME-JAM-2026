import game
import pygame

pygame.init()

from states.play_state import PlayState
from states.level_editor_state import LevelEditorState

game.Game({
    'play_state': PlayState(),
    'level_editor_state': LevelEditorState(),
}).loop()
