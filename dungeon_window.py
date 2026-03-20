from settings import *
from utils import *
from character import *

class Dungeon_Window:
    def __init__(self, character: Character):
        self.character = character
        
    def draw(self, canvas, mouse_pos):
        create_rectangle(canvas, MAIN_START + 100, 200, 100, 100, 2, "green")
        pass

    def handle_events(self, canvas, mouse_pos):
        pass