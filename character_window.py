from settings import *
from utils import *
from character import *

class Character_Window:
    def __init__(self, character: Character, main_item_list):
        self.character_blueprint = Character_Blueprint(character)
        self.main_item_list = main_item_list

    def draw(self, canvas, mouse_pos):
        self.character_blueprint.draw(canvas, mouse_pos)

    def handle_events(self, event, mouse_pos):
        self.character_blueprint.handle_events(event, mouse_pos)

class Character_Blueprint:
    def __init__(self, character: Character):
        self.character = character        
        self.exp_bar_length = 370
        self.character_exp_bar_ratio = self.character.required_experience / self.exp_bar_length
        self.show_exp_bar_tooltips = False
        self.character_window_x = 0
        self.character_window_y = 0
        self.character_window_width = 0
        self.character_window_height = 0

    def draw(self, canvas, mouse_pos):
        main_side_padding = 20
        spacer_padding = 5
        text_padding = 30
        base_x = 20

        # helmet

        helmet_rect = create_rectangle(canvas, MAIN_START + main_side_padding, base_x, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        self.character_window_x = helmet_rect.x
        self.character_window_y = helmet_rect.y
        self.character_window_width = 815
        self.character_window_height = 815 - ITEM_HOLDER_SIZE

        # plate

        create_rectangle(canvas, MAIN_START + main_side_padding, base_x + ITEM_HOLDER_SIZE + spacer_padding, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        # legs

        create_rectangle(canvas, MAIN_START + main_side_padding, base_x + ((ITEM_HOLDER_SIZE + spacer_padding) * 2), ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        # shoes

        create_rectangle(canvas, MAIN_START + main_side_padding, base_x + ((ITEM_HOLDER_SIZE + spacer_padding) * 3), ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        # character

        character_rectangle = create_rectangle(canvas, MAIN_START + main_side_padding + ITEM_HOLDER_SIZE + spacer_padding, base_x, ITEM_HOLDER_SIZE * 2 + spacer_padding, ITEM_HOLDER_SIZE * 2 + spacer_padding, 2, "red")

        character_rect_y = character_rectangle.y + character_rectangle.height - 50
        character_rect_x = character_rectangle.x + spacer_padding
        character_exp_bar_width = 395
        character_exp_bar_height = 30

        dynamic_width = max(0, self.character.experience / self.character_exp_bar_ratio)

        create_rectangle(canvas, character_rect_x, character_rect_y, dynamic_width, character_exp_bar_height, 0, "lightgreen")
        exp_bar = create_rectangle(canvas, character_rect_x, character_rect_y, character_exp_bar_width, character_exp_bar_height, 2, "cyan")
        show_text(canvas, f"Level: {self.character.level}", exp_bar.x + exp_bar.width / 2, exp_bar.y + exp_bar.height / 2, "white", True)

        if exp_bar.collidepoint(mouse_pos):
            self.show_exp_bar_tooltips = True
        else:
            self.show_exp_bar_tooltips = False

        # weapon and accessorie

        create_rectangle(canvas, MAIN_START + main_side_padding + ITEM_HOLDER_SIZE + spacer_padding, base_x + (ITEM_HOLDER_SIZE + spacer_padding) * 2 , ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        create_rectangle(canvas, MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 2, base_x + (ITEM_HOLDER_SIZE + spacer_padding) * 2 , ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        # stats

        stat_rectangle = create_rectangle(canvas, MAIN_START + main_side_padding + ITEM_HOLDER_SIZE + spacer_padding, base_x + (ITEM_HOLDER_SIZE + spacer_padding) * 3 , ITEM_HOLDER_SIZE * 2 + spacer_padding, ITEM_HOLDER_SIZE, 2, "red")

        # health
        show_text(canvas, f"Health: {self.character.max_health}", stat_rectangle.x + text_padding, stat_rectangle.y + text_padding)

        # damage
        show_text(canvas, f"Damage: {self.character.damage}", stat_rectangle.x + text_padding, stat_rectangle.y + text_padding + 25)

        # amulet

        amulet_rect = create_rectangle(canvas, MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 3, base_x, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        # ring 

        create_rectangle(canvas, MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 3, base_x + ITEM_HOLDER_SIZE + spacer_padding, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        # extra 3

        create_rectangle(canvas, MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 3, base_x + ((ITEM_HOLDER_SIZE + spacer_padding) * 2), ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")

        # extra 4

        create_rectangle(canvas, MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 3, base_x + ((ITEM_HOLDER_SIZE + spacer_padding) * 3), ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "red")


        # inventory 

        create_rectangle(canvas, amulet_rect.x + ITEM_HOLDER_SIZE + ITEM_HOLDER_SIZE + spacer_padding, amulet_rect.y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "green")
        create_rectangle(canvas, amulet_rect.x + ITEM_HOLDER_SIZE + (ITEM_HOLDER_SIZE + spacer_padding) * 2, amulet_rect.y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "green")
        create_rectangle(canvas, amulet_rect.x + ITEM_HOLDER_SIZE + (ITEM_HOLDER_SIZE + spacer_padding) * 3, amulet_rect.y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "green")

        # tooltip

        if self.show_exp_bar_tooltips:
            create_tooltip(canvas, exp_bar.x + exp_bar.width / 2 - 30, exp_bar.y + exp_bar.height + spacer_padding, 100, 30, f"{self.character.experience}/{self.character.required_experience}", "white", "gray")

    def handle_events(self, event, mouse_pos):
        pass