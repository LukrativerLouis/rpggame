import pygame
from character_window import *
from item import *

class Shop_Window():
    def __init__(self, character, main_item_list):
        self.character = character
        self.main_item_list = main_item_list
        self.character_blueprint = Character_Blueprint(self.character)
        self.__get_new_item()

    def __get_new_item(self):
        # TODO: create one item for a slot
        test_item = Item(600, 600, ITEM_SIZE, ITEM_SIZE, "TEST", 0, 0, 0, 0, "TEST", False)
        self.main_item_list.append(test_item)

    def __create_item_list(self):
        # TODO:

        item_list = []

        return item_list

    def draw(self, canvas, mouse_pos):
        spacer_padding = 5
        text_padding = 30

        self.character_blueprint.draw(canvas, mouse_pos)

        start_for_shop_x = self.character_blueprint.character_window_x + self.character_blueprint.character_window_width + ITEM_HOLDER_SIZE + spacer_padding
        start_for_shop_y = self.character_blueprint.character_window_y + self.character_blueprint.character_window_height

        create_rectangle(canvas, start_for_shop_x, start_for_shop_y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "blue")

        create_rectangle(canvas, start_for_shop_x + ITEM_HOLDER_SIZE + spacer_padding, start_for_shop_y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "blue")

        create_rectangle(canvas, start_for_shop_x + (ITEM_HOLDER_SIZE + spacer_padding) * 2, start_for_shop_y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "blue")

        create_rectangle(canvas, start_for_shop_x, start_for_shop_y + ITEM_HOLDER_SIZE + spacer_padding, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "blue")

        create_rectangle(canvas, start_for_shop_x + ITEM_HOLDER_SIZE + spacer_padding, start_for_shop_y + ITEM_HOLDER_SIZE + spacer_padding, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "blue")

        create_rectangle(canvas, start_for_shop_x + (ITEM_HOLDER_SIZE + spacer_padding) * 2, start_for_shop_y + ITEM_HOLDER_SIZE + spacer_padding, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, 2, "blue")

    def handle_events(self, event, mouse_pos):
        self.character_blueprint.handle_events(event, mouse_pos)

