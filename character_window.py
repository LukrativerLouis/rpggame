from settings import *
from utils import *
from character import *

class Character_Window:
    def __init__(self, character: Character):
        self.character = character        
        self.exp_bar_length = 370
        self.character_exp_bar_ratio = self.character.required_experience / self.exp_bar_length

    def draw(self, canvas, mouse_pos):

        main_side_padding = 20
        spacer_padding = 5
        text_padding = 30
        base_x = 20
        item_holder_size = 200

        # helmet

        create_rectangle(canvas, MAIN_START + main_side_padding, base_x, item_holder_size, item_holder_size, 2, "red")

        # plate

        create_rectangle(canvas, MAIN_START + main_side_padding, base_x + item_holder_size + spacer_padding, item_holder_size, item_holder_size, 2, "red")

        # legs

        create_rectangle(canvas, MAIN_START + main_side_padding, base_x + ((item_holder_size + spacer_padding) * 2), item_holder_size, item_holder_size, 2, "red")

        # shoes

        create_rectangle(canvas, MAIN_START + main_side_padding, base_x + ((item_holder_size + spacer_padding) * 3), item_holder_size, item_holder_size, 2, "red")

        # character

        character_rectangle = create_rectangle(canvas, MAIN_START + main_side_padding + item_holder_size + spacer_padding, base_x, item_holder_size * 2 + spacer_padding, item_holder_size * 2 + spacer_padding, 2, "red")

        character_rect_y = character_rectangle.y + character_rectangle.height - 50
        character_rect_x = character_rectangle.x + spacer_padding
        character_exp_bar_width = 395
        character_exp_bar_height = 30

        dynamic_width = max(0, self.character.experience / self.character_exp_bar_ratio)

        create_rectangle(canvas, character_rect_x, character_rect_y, dynamic_width, character_exp_bar_height, 0, "lightgreen")
        exp_bar = create_rectangle(canvas, character_rect_x, character_rect_y, character_exp_bar_width, character_exp_bar_height, 2, "cyan")
        show_text(canvas, f"Level: {self.character.level}", exp_bar.x + exp_bar.width / 2, exp_bar.y + exp_bar.height / 2, "white", True)

        # weapon and accessorie

        create_rectangle(canvas, MAIN_START + main_side_padding + item_holder_size + spacer_padding, base_x + (item_holder_size + spacer_padding) * 2 , item_holder_size, item_holder_size, 2, "red")

        create_rectangle(canvas, MAIN_START + main_side_padding + (item_holder_size + spacer_padding) * 2, base_x + (item_holder_size + spacer_padding) * 2 , item_holder_size, item_holder_size, 2, "red")

        # stats

        stat_rectangle = create_rectangle(canvas, MAIN_START + main_side_padding + item_holder_size + spacer_padding, base_x + (item_holder_size + spacer_padding) * 3 , item_holder_size * 2 + spacer_padding, item_holder_size, 2, "red")

        # health
        show_text(canvas, f"Health: {self.character.max_health}", stat_rectangle.x + text_padding, stat_rectangle.y + text_padding)

        # damage
        show_text(canvas, f"Damage: {self.character.damage}", stat_rectangle.x + text_padding, stat_rectangle.y + text_padding + 25)

        # amulet

        create_rectangle(canvas, MAIN_START + main_side_padding + (item_holder_size + spacer_padding) * 3, base_x, item_holder_size, item_holder_size, 2, "red")

        # ring 

        create_rectangle(canvas, MAIN_START + main_side_padding + (item_holder_size + spacer_padding) * 3, base_x + item_holder_size + spacer_padding, item_holder_size, item_holder_size, 2, "red")

        # extra 3

        create_rectangle(canvas, MAIN_START + main_side_padding + (item_holder_size + spacer_padding) * 3, base_x + ((item_holder_size + spacer_padding) * 2), item_holder_size, item_holder_size, 2, "red")

        # extra 4

        create_rectangle(canvas, MAIN_START + main_side_padding + (item_holder_size + spacer_padding) * 3, base_x + ((item_holder_size + spacer_padding) * 3), item_holder_size, item_holder_size, 2, "red")
        

    def handle_events(self, canvas, mouse_pos):
        pass