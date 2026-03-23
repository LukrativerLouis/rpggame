import pygame
from character_window import *

class Shop_Window():
    def __init__(self, character):
        self.character = character
        self.character_blueprint = Character_Blueprint(self.character)

    def draw(self, canvas, mouse_pos):
        spacer_padding = 5
        text_padding = 30

        self.character_blueprint.draw(canvas, mouse_pos)

        item_holder_size = self.character_blueprint.item_holder_size

        start_for_shop_x = self.character_blueprint.character_window_x + self.character_blueprint.character_window_width + item_holder_size + spacer_padding
        start_for_shop_y = self.character_blueprint.character_window_y + self.character_blueprint.character_window_height

        create_rectangle(canvas, start_for_shop_x, start_for_shop_y, item_holder_size, item_holder_size, 2, "blue")

        create_rectangle(canvas, start_for_shop_x + item_holder_size + spacer_padding, start_for_shop_y, item_holder_size, item_holder_size, 2, "blue")

        create_rectangle(canvas, start_for_shop_x + (item_holder_size + spacer_padding) * 2, start_for_shop_y, item_holder_size, item_holder_size, 2, "blue")

        create_rectangle(canvas, start_for_shop_x, start_for_shop_y + item_holder_size + spacer_padding, item_holder_size, item_holder_size, 2, "blue")

        create_rectangle(canvas, start_for_shop_x + item_holder_size + spacer_padding, start_for_shop_y + item_holder_size + spacer_padding, item_holder_size, item_holder_size, 2, "blue")

        create_rectangle(canvas, start_for_shop_x + (item_holder_size + spacer_padding) * 2, start_for_shop_y + item_holder_size + spacer_padding, item_holder_size, item_holder_size, 2, "blue")

    def handle_events(self, event, mouse_pos):
        self.character_blueprint.handle_events(event, mouse_pos)
