from settings import *
from utils import *
from character import *
from item import *

class Character_Window:
    def __init__(self, character: Character, main_item_list, settings):
        self.character = character
        self.main_item_list = main_item_list
        self.settings = settings
        self.character_blueprint = Character_Blueprint(character, settings)

    @property
    def item_holder_list(self):
        return self.character_blueprint.item_holder_list

    def draw(self, canvas, mouse_pos, active_item):
        self.character_blueprint.draw(canvas, mouse_pos, active_item)

    def handle_events(self, event, mouse_pos):
        self.character_blueprint.handle_events(event, mouse_pos)

class Character_Blueprint:
    def __init__(self, character: Character, settings):
        self.character = character
        self.settings = settings
        self.exp_bar_width = 395
        self.item_holder_list = []
        self.show_exp_bar_tooltips = False
        self.character_window_x = 0
        self.character_window_y = 0
        self.character_window_width = 815
        self.character_window_height = 815 - ITEM_HOLDER_SIZE
        self.exp_bar = None
        self.exp_bar_tooltip = Tooltip(0, 0, 100, 30, f"{self.character.experience}/{self.character.required_experience}", "white", "gray")
        self.stats_to_display = ["strength", "dexterity", "endurance", "precision"]
        self.stat_button_list = []
        self.stat_tooltips = []
        self.setup_slots()
        self.create_stat_buttons()

    def create_stat_buttons(self):
        self.stat_button_list = []
        self.stat_tooltips = []
        for stat_name in self.stats_to_display:
            btn = Button(
                position=(0, 0), 
                size=(30, 30), 
                text="+", 
                color=[255, 0, 0],
                func=lambda s=stat_name: self.character.increase_base_stat(s)
            )
            btn.stat_name = stat_name 
            self.stat_button_list.append(btn)

            cost = self.character.get_stat_price(stat_name)
            tooltip = Tooltip(
                x=0, 
                y=0, 
                width=120, 
                height=40, 
                text=f"Cost: {cost}g", 
                text_color="white", 
                bg_color="gray"
            )
            self.stat_tooltips.append(tooltip)

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

    def draw(self, canvas, mouse_pos, active_item):
        main_side_padding = 20
        spacer_padding = 5
        text_padding = 30
        base_x = 20
        
        # character

        character_rectangle = create_rectangle(canvas, MAIN_START + main_side_padding + ITEM_HOLDER_SIZE + spacer_padding, base_x, ITEM_HOLDER_SIZE * 2 + spacer_padding, ITEM_HOLDER_SIZE * 2 + spacer_padding, 2, "red")

        character_rect_y = character_rectangle.y + character_rectangle.height - 50
        character_rect_x = character_rectangle.x + spacer_padding
        character_exp_bar_height = 30

        character_exp_bar_ratio  = self.character.required_experience / self.exp_bar_width
        dynamic_width = max(0, self.character.experience / character_exp_bar_ratio - 2)

        create_rectangle(canvas, character_rect_x, character_rect_y, dynamic_width, character_exp_bar_height, 0, "lightgreen")
        self.exp_bar = create_rectangle(canvas, character_rect_x, character_rect_y, self.exp_bar_width, character_exp_bar_height, 2, "cyan")
        show_text(canvas, f"Level: {self.character.level}", self.exp_bar.x + self.exp_bar.width / 2, self.exp_bar.y + self.exp_bar.height / 2, "white", True)

        stat_rectangle = create_rectangle(canvas, MAIN_START + main_side_padding + ITEM_HOLDER_SIZE + spacer_padding, base_x + (ITEM_HOLDER_SIZE + spacer_padding) * 3 , ITEM_HOLDER_SIZE * 2 + spacer_padding, ITEM_HOLDER_SIZE, 2, "red")

        # health
        show_text(canvas, f"{self.settings.translate("stat_health")}: {self.character.max_health}", stat_rectangle.x + text_padding + 200, stat_rectangle.y + text_padding - 20)

        # damage
        show_text(canvas, f"{self.settings.translate("stat_damage")}: {self.character.damage}", stat_rectangle.x + text_padding + 200, stat_rectangle.y + text_padding + 5)

        start_y = stat_rectangle.y + text_padding + 25
        line_height = 35

        for i, stat_name in enumerate(self.stats_to_display):
            current_y = start_y + (i * line_height)
            stat_value = getattr(self.character, stat_name)
            show_text(canvas, f"{self.settings.translate(f"stat_{stat_name}")}: {stat_value}", stat_rectangle.x + text_padding, current_y)
            
            button = self.stat_button_list[i]
            button_x = stat_rectangle.x + text_padding + 150
            button_y = current_y + 10
            button.set_pos((button_x, button_y))
            button.draw(canvas, mouse_pos)

            tooltip = self.stat_tooltips[i]
            tooltip.x = button_x
            tooltip.y = button_y - 50
            tooltip.text = f"Cost: {self.character.get_stat_price(stat_name)}g"

        for i, button in enumerate(self.stat_button_list):
            self.stat_tooltips[i].draw(canvas, mouse_pos, button.rect)

        # exp tooltip
        if active_item == None:
            self.exp_bar_tooltip.text = f"{self.character.experience}/{self.character.required_experience}"

    def handle_events(self, event, mouse_pos):
        for i, button in enumerate(self.stat_button_list):
            button.handle_event(event, mouse_pos)