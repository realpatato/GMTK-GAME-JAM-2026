import game
import pygame

pygame.init()

from states.play_state import PlayState
from states.level_editor_state import LevelEditorState
from states.mainmenu_state import MainMenuState

g = game.Game()

states = {
    'play_state': PlayState(),
    'level_editor_state': LevelEditorState(),
    'mainmenu_state': MainMenuState(),
}

g.begin(states, "mainmenu_state")
g.loop()