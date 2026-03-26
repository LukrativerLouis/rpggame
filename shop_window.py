import pygame
from character_window import *
from item import *

class Shop_Window():
    def __init__(self, character, main_item_list, active_item):
        self.character = character
        self.main_item_list = main_item_list
        self.active_item = active_item
        self.item_holder_list = []
        self.character_blueprint = Character_Blueprint(self.character)
        self.__get_new_item()
        self.setup_shop_slots()

    def setup_shop_slots(self):
        spacer_padding = 5
        start_for_shop_x = self.character_blueprint.character_window_x + self.character_blueprint.character_window_width + ITEM_HOLDER_SIZE + spacer_padding
        start_for_shop_y = self.character_blueprint.character_window_y + self.character_blueprint.character_window_height

        for row in range(2):
            for col in range(3):
                x = start_for_shop_x + (ITEM_HOLDER_SIZE + spacer_padding) * col
                y = start_for_shop_y + (ITEM_HOLDER_SIZE + spacer_padding) * row
                self.item_holder_list.append(Item_Holder(x, y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, SHOP))

    def __get_new_item(self):
        test_item = Item(600, 600, ITEM_SIZE, ITEM_SIZE, "TEST", 0, 0, 0, 0, "TEST", False)
        self.main_item_list.append(test_item)

    def __create_item_list(self):
        # TODO:

        item_list = []

        return item_list

    def draw(self, canvas, mouse_pos):
        self.character_blueprint.draw(canvas, mouse_pos)

        for rect in self.item_holder_list:
            pygame.draw.rect(canvas, "blue", rect, 2)

    def handle_events(self, event, mouse_pos):
        self.character_blueprint.handle_events(event, mouse_pos)

