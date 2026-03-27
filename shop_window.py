from character_window import *
from item import *

class Shop_Window():
    def __init__(self, character: Character, main_item_list, active_item):
        self.character = character
        self.main_item_list: list[Item] = main_item_list
        self.shop_item_list = []
        self.active_item = active_item
        self.item_holder_list = []
        self.character_blueprint = Character_Blueprint(self.character)
        self.setup_shop_slots()
        self.__create_all_items()
        self.refresh_buttom = Button(position = (self.start_for_shop_x + ITEM_HOLDER_SIZE + 5 + ITEM_HOLDER_SIZE / 2, self.start_for_shop_y - 50), size = (150, 50), color = (0, 0, 255), text = "reroll items", func = lambda: self.reroll_shop())

    def setup_shop_slots(self):
        spacer_padding = 5
        self.start_for_shop_x = self.character_blueprint.character_window_x + self.character_blueprint.character_window_width + ITEM_HOLDER_SIZE + spacer_padding
        self.start_for_shop_y = self.character_blueprint.character_window_y + self.character_blueprint.character_window_height

        for row in range(2):
            for col in range(3):
                x = self.start_for_shop_x + (ITEM_HOLDER_SIZE + spacer_padding) * col
                y = self.start_for_shop_y + (ITEM_HOLDER_SIZE + spacer_padding) * row
                self.item_holder_list.append(Item_Holder(x, y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "blue", SHOP))

    def __create_all_items(self):
        for item_holder in self.item_holder_list:
            id, name, physical_damage, magic_damage, armor, magic_resist, type, sub_type = getItemDetailsRandom()
            item = Item(id, item_holder.rect.center[0], item_holder.rect.center[1], ITEM_SIZE, ITEM_SIZE, name, physical_damage, magic_damage, armor, magic_resist, self.character.get_item_gold_value() , type, sub_type, False)
            self.main_item_list.append(item)
            self.shop_item_list.append(item)

    def create_new_item(self, item_holder):
        id, name, physical_damage, magic_damage, armor, magic_resist, type, sub_type = getItemDetailsRandom()
        item = Item(id, item_holder.rect.center[0], item_holder.rect.center[1], ITEM_SIZE, ITEM_SIZE, name, physical_damage, magic_damage, armor, magic_resist,self.character.get_item_gold_value(), type, sub_type, False)
        self.main_item_list.append(item)
        self.shop_item_list.append(item)

    def reroll_shop(self):
        for item in self.shop_item_list:
            self.main_item_list.remove(item)
        self.shop_item_list.clear()
        self.__create_all_items()

    def draw(self, canvas, mouse_pos):
        self.character_blueprint.draw(canvas, mouse_pos)

        self.refresh_buttom.draw(canvas, mouse_pos)

        for holder in self.item_holder_list:
            holder.draw(canvas, mouse_pos)

    def handle_events(self, event, mouse_pos):
        self.character_blueprint.handle_events(event, mouse_pos)
        self.refresh_buttom.handle_event(event, mouse_pos)

