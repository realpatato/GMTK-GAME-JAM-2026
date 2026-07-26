import math
import sys
from pygame.locals import *

IS_DESKTOP = sys.platform != "emscripten"

TILE_SIZE = 16 #pixels

TILE_TYPES = ["Ground", "Enter", "Exit", "Torch", "Faucet"]

SCALE_FACTOR = 3
WINDOW_SIZE = (1280,720)

NATIVE_RESOLUTION = [math.ceil(x / SCALE_FACTOR) for x in WINDOW_SIZE]

BACKGROUND_COLOR = (40, 19, 23)