import game
import pygame
import asyncio 

pygame.init()

from states.play_state import PlayState
from states.level_editor_state import LevelEditorState
from states.mainmenu_state import MainMenuState

if __name__ == "__main__":
    g = game.Game()
    states = {
        'play_state': PlayState(),
        'level_editor_state': LevelEditorState(),
        'mainmenu_state': MainMenuState(),
    }

    g.begin(states, "mainmenu_state")
    asyncio.run(g.loop())