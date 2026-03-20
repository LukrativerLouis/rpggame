from settings import *
from utils import *
from character import *

class Dungeon_Window:
    def __init__(self, character: Character):
        self.character = character
        
    def draw(self, canvas, mouse_pos):

        spacer_padding = 5
        main_side_padding = 20
        base_dungeon_window_size = 400

        # first dungeon window

        first_dungeon_window = create_rectangle(canvas, MAIN_START + main_side_padding, main_side_padding, base_dungeon_window_size, 800, 4, "green")

        show_text(canvas, "Dungeon 1", first_dungeon_window.x + first_dungeon_window.width / 2, first_dungeon_window.y + main_side_padding, "white", True)

        # second dungeon window 

        second_dungeon_window = create_rectangle(canvas, MAIN_START + main_side_padding + base_dungeon_window_size + spacer_padding, main_side_padding, base_dungeon_window_size, 800, 4, "blue")

        show_text(canvas, "Dungeon 2", second_dungeon_window.x + second_dungeon_window.width / 2, second_dungeon_window.y + main_side_padding, "white", True)

        # third dungeon window

        third_dungeon_window = create_rectangle(canvas, MAIN_START + main_side_padding + (base_dungeon_window_size + spacer_padding) * 2, main_side_padding, base_dungeon_window_size, 800, 4, "red")

        show_text(canvas, "Dungeon 3", third_dungeon_window.x + third_dungeon_window.width / 2, third_dungeon_window.y + main_side_padding, "white", True)


    def handle_events(self, canvas, mouse_pos):
        pass