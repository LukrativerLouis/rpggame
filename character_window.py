from settings import *
from utils import *
from character import *
from item import *

class Character_Window:
    def __init__(self, character: Character, main_item_list, active_item):
        self.character = character
        self.character_blueprint = Character_Blueprint(character)
        self.main_item_list = main_item_list
        self.active_item = active_item

    @property
    def item_holder_list(self):
        return self.character_blueprint.item_holder_list

    def draw(self, canvas, mouse_pos):
        self.character_blueprint.draw(canvas, mouse_pos)

    def handle_events(self, event, mouse_pos):
        self.character_blueprint.handle_events(event, mouse_pos)

class Character_Blueprint:
    def __init__(self, character: Character):
        self.character = character        
        self.exp_bar_length = 370
        self.item_holder_list = []
        self.character_exp_bar_ratio = self.character.required_experience / self.exp_bar_length
        self.show_exp_bar_tooltips = False
        self.character_window_x = 0
        self.character_window_y = 0
        self.character_window_width = 815
        self.character_window_height = 815 - ITEM_HOLDER_SIZE
        self.setup_slots()

    def setup_slots(self):
        base_x = 20
        main_side_padding = 20
        spacer_padding = 5

        # adjust for item_holder class

        self.helmet_slot = Item_Holder(MAIN_START + main_side_padding, base_x, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", HELMET)
        self.plate_slot = Item_Holder(MAIN_START + main_side_padding, base_x + ITEM_HOLDER_SIZE + spacer_padding, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", CHEST_PLATE)
        self.legs_slot = Item_Holder(MAIN_START + main_side_padding, base_x + ((ITEM_HOLDER_SIZE + spacer_padding) * 2), ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", LEGGINGS)
        self.shoes_slot = Item_Holder(MAIN_START + main_side_padding, base_x + ((ITEM_HOLDER_SIZE + spacer_padding) * 3), ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", SHOES)
        self.weapon_slot = Item_Holder(MAIN_START + main_side_padding + ITEM_HOLDER_SIZE + spacer_padding, base_x + (ITEM_HOLDER_SIZE + spacer_padding) * 2, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", WEAPON)
        self.acc_rect_slot = Item_Holder(MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 2, base_x + (ITEM_HOLDER_SIZE + spacer_padding) * 2, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE,"red",  ACCESSORIES)
        self.amulet_slot = Item_Holder(MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 3, base_x, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", AMULET)
        self.ring_slot = Item_Holder(MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 3, base_x + ITEM_HOLDER_SIZE + spacer_padding, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", RING)
        self.extra3_slot = Item_Holder(MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 3, base_x + ((ITEM_HOLDER_SIZE + spacer_padding) * 2), ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", EXTRA3)
        self.extra4_slot = Item_Holder(MAIN_START + main_side_padding + (ITEM_HOLDER_SIZE + spacer_padding) * 3, base_x + ((ITEM_HOLDER_SIZE + spacer_padding) * 3), ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", EXTRA4)
        self.inv_1_slot = Item_Holder(self.amulet_slot.x + ITEM_HOLDER_SIZE + ITEM_HOLDER_SIZE + spacer_padding, self.amulet_slot.y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", INVENTORY)
        self.inv_2_slot = Item_Holder(self.amulet_slot.x + ITEM_HOLDER_SIZE + (ITEM_HOLDER_SIZE + spacer_padding) * 2, self.amulet_slot.y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", INVENTORY)
        self.inv_3_slot = Item_Holder(self.amulet_slot.x + ITEM_HOLDER_SIZE + (ITEM_HOLDER_SIZE + spacer_padding) * 3, self.amulet_slot.y, ITEM_HOLDER_SIZE, ITEM_HOLDER_SIZE, "red", INVENTORY)

        self.character_window_x = self.helmet_slot.x
        self.character_window_y = self.helmet_slot.y

        self.item_holder_list = [self.helmet_slot, self.plate_slot, self.legs_slot, self.shoes_slot, self.weapon_slot, self.acc_rect_slot, self.amulet_slot, self.ring_slot, self.extra3_slot, self.extra4_slot, self.inv_1_slot, self.inv_2_slot, self.inv_3_slot]

    def draw(self, canvas, mouse_pos):
        main_side_padding = 20
        spacer_padding = 5
        text_padding = 30
        base_x = 20
        
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

        # stats

        for holder in self.item_holder_list:
            holder.draw(canvas, mouse_pos)

        stat_rectangle = create_rectangle(canvas, MAIN_START + main_side_padding + ITEM_HOLDER_SIZE + spacer_padding, base_x + (ITEM_HOLDER_SIZE + spacer_padding) * 3 , ITEM_HOLDER_SIZE * 2 + spacer_padding, ITEM_HOLDER_SIZE, 2, "red")

        # health
        show_text(canvas, f"Health: {self.character.max_health}", stat_rectangle.x + text_padding, stat_rectangle.y + text_padding)

        # damage
        show_text(canvas, f"Damage: {self.character.damage}", stat_rectangle.x + text_padding, stat_rectangle.y + text_padding + 25)

        # tooltip

        if self.show_exp_bar_tooltips:
            create_tooltip(canvas, exp_bar.x + exp_bar.width / 2 - 30, exp_bar.y + exp_bar.height + spacer_padding, 100, 30, f"{self.character.experience}/{self.character.required_experience}", "white", "gray")

    def handle_events(self, event, mouse_pos):
        pass