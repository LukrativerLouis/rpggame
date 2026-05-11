from character_window import *
from item import *

class Shop_Window():
    def __init__(self, character: Character, main_item_list, settings):
        self.character = character
        self.main_item_list: list[Item] = main_item_list
        self.settings = settings
        self.item_holder_list = []
        self.character_blueprint = Character_Blueprint(self.character, self.settings)
        self.setup_shop_slots()
        self.refresh_buttom = Button(position = (self.start_for_shop_x + ITEM_HOLDER_SIZE + 5 + ITEM_HOLDER_SIZE / 2, self.start_for_shop_y - 50), size = (150, 50), color = (0, 0, 255), text = self.settings.translate("button_reroll_items"), func = lambda: self.reroll_shop())
        if self.character.shop_items:
            self.load_shop_items(self.character.shop_items)
        else:
            self.reroll_shop()

    def setup_shop_slots(self):
        spacer_padding = 5
        self.start_for_shop_x = self.character_blueprint.character_window_x + self.character_blueprint.character_window_width + ITEM_HOLDER_SIZE + spacer_padding
        self.start_for_shop_y = self.character_blueprint.character_window_y + self.character_blueprint.character_window_height

        for row in range(2):
            for col in range(3):
                x = self.start_for_shop_x + (ITEM_HOLDER_SIZE + spacer_padding) * col
                y = self.start_for_shop_y + (ITEM_HOLDER_SIZE + spacer_padding) * row
                self.item_holder_list.append(Item_Holder(x, y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "blue", SHOP))

    def create_new_item(self, item_holder):
        item = create_random_item(self.character.level, self.character.class_type, item_holder.rect.center[0], item_holder.rect.center[1])

        self.character.shop_items.append(item)

        if item not in self.main_item_list:
            self.main_item_list.append(item)

    def load_shop_items(self, items):
        self.character.shop_items = items

        for item in self.character.shop_items:
            if item not in self.main_item_list:
                self.main_item_list.append(item)

        for i, item in enumerate(self.character.shop_items):
            if i < len(self.item_holder_list):
                item.rect.center = self.item_holder_list[i].rect.center
                item.x, item.y = item.rect.center

    def reroll_shop(self):
        if not self.character: return

        if self.character.shop_items:
            for item in self.character.shop_items:
                if item in self.main_item_list:
                    self.main_item_list.remove(item)
        self.character.shop_items.clear()
        for holder in self.item_holder_list:
            self.create_new_item(holder)

    def draw(self, canvas, mouse_pos, active_item):
        self.character_blueprint.draw(canvas, mouse_pos, active_item)

        self.refresh_buttom.draw(canvas, mouse_pos)

        for holder in self.item_holder_list:
            holder.draw(canvas, mouse_pos)

    def handle_events(self, event, mouse_pos):
        self.character_blueprint.handle_events(event, mouse_pos)
        self.refresh_buttom.handle_event(event, mouse_pos)

