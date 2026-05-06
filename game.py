import pygame
from character import *
from save_service import *
from menu import *
from character_window import *
from shop_window import *
from dungeon_window import *
from quest_window import *
from settings import *
from utils import *
from intro import *

class Game():
    def __init__(self, system, character_list, active_character, current_shop_data, all_shops_data):
        self.system = system
        self.character_list = character_list
        self.all_shops_data = all_shops_data
        self.character: Character = active_character
        self.character.shop_items = current_shop_data

        self.main_item_list: list[Item] = []
        self.active_item = None
        self.main_button_list = []

        self.main_window_state = DEFAULT_MAIN_WINDOW_STATE
        self.quest_window = Quest_Window(self.character, self, self.system.settings)
        self.shop_window = Shop_Window(self.character, self.main_item_list, self.system.settings)
        self.character_window = Character_Window(self.character, self.main_item_list, self.system.settings)
        self.dungeon_window = Dungeon_Window(self.character, self.system.settings)

        self.item_holder_list: list[Item_Holder] = self.shop_window.item_holder_list + self.character_window.item_holder_list

        # IF CURSOR STUFF PLEASE YOU NEED TO REMOVE
        if pygame.mouse.get_cursor() != pygame.Cursor(pygame.SYSTEM_CURSOR_ARROW):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.create_buttons()

    def create_buttons(self):
        btn_quest = Button(position = (100, 100), size = (150, 50), text = self.system.settings.translate("button_questboard"), change_color = [150, 150, 150], func = lambda: self.toggle_main_state(QUEST_MAIN_WINDOW_STATE))
        btn_character = Button(position = (100, 170), size = (150, 50), text = self.system.settings.translate("button_character"), change_color = [150, 150, 150], func = lambda: self.toggle_main_state(CHARACTER_MAIN_WINDOW_STATE))
        btn_shop = Button(position = (100, 240), size = (150, 50), text = self.system.settings.translate("button_shop"), change_color = [150, 150, 150], func = lambda: self.toggle_main_state(SHOP_MAIN_WINDOW_STATE))
        btn_dungeon = Button(position = (100, 310), size = (150, 50), text = self.system.settings.translate("button_dungeon"), change_color = [150, 150, 150], func = lambda: self.toggle_main_state(DUNGEON_MAIN_WINDOW_STATE))
        btn_back = Button(position=(100, 925), size=(100, 50), text= self.system.settings.translate("button_back"), color=[150, 50, 50], change_color=[200, 50, 50], func= lambda: self.back_button())
        btn_quit = Button(position=(100, 995), size=(100, 50), text= self.system.settings.translate("button_quit"), color=[150, 50, 50], change_color=[200, 50, 50], func= lambda: self.quit_game())
        #btn_test = Button(position=(100, 1050), size=(100, 40), text="Test", color=[200, 50, 50], func= lambda: self.set_specific_window_size(1280, 720))

        self.main_button_list = [btn_quest, btn_character, btn_shop, btn_dungeon, btn_back, btn_quit]

    def back_button(self):
        self.system.save_service.save_data(self.all_shops_data, self.character_list, self.character.dungeon_completed, self.quest_window.quest_list)
        self.system.switch_menu_state(CHARACTER_SLOTS_STATE)

    def quit_game(self):
        if self.system.is_web:
            return
        self.system.save_service.save_data(self.all_shops_data, self.character_list, self.character.dungeon_completed, self.quest_window.quest_list)
        self.system.save_service.save_options(self.system.settings)
        self.system.quit_game(already_saved = True)

    def set_items_to_visible(self, item_list):
        for item in item_list:
            item.visible = True

    def set_items_to_invisible(self, item_list):
        for item in item_list:
            item.visible = False

    def remove_item_from_holder(self, item, holder):
        if holder.type == SHOP and item in self.character.shop_items:
            self.character.shop_items.remove(item)
        elif holder.type == INVENTORY and item in self.character.inventory:
            self.character.inventory.remove(item)
        elif holder.type in LIST_OF_EQUIPMENT_TYPES and item in self.character.equipment:
            self.character.equipment.remove(item)

    def add_item_to_holder(self, item, holder):
        if holder.type == INVENTORY and item not in self.character.inventory:
            self.character.inventory.append(item)
        elif holder.type in LIST_OF_EQUIPMENT_TYPES and item not in self.character.equipment:
            self.character.equipment.append(item)

    def get_free_inventory_slot(self):
        for holder in self.item_holder_list:
            if holder.type == INVENTORY:
                is_occupied = any(item.rect.colliderect(holder.rect) for item in self.main_item_list)

                if not is_occupied:
                    return holder
        return None

    def toggle_main_state(self, new_window_state):
        #  actually game state
        if self.main_window_state == new_window_state:
            self.main_window_state = DEFAULT_MAIN_WINDOW_STATE
        else:
            self.main_window_state = new_window_state

    def on_item_hover(self, new_item):
        equipped_item = self.get_equipped_item_of_type(new_item.type)
        
        if equipped_item:
            new_item.compare_with_equipped(equipped_item)
            equipped_item.tooltip.is_hovered = new_item.tooltip.is_hovered
        else:
            new_item.create_tooltip()

    def get_equipped_item_of_type(self, item_type):
        for item in self.character.equipment:
            if item.type == item_type:
                return item
        return None

    def handle_events(self, event, mouse_pos):
        # event handling

        for button in self.main_button_list:
            button.handle_event(event, mouse_pos)

        # event handling window states

        if self.main_window_state == DEFAULT_MAIN_WINDOW_STATE:
            pass
        elif self.main_window_state == QUEST_MAIN_WINDOW_STATE:
            self.quest_window.handle_events(event, mouse_pos)
        elif self.main_window_state == SHOP_MAIN_WINDOW_STATE:
            self.shop_window.handle_events(event, mouse_pos)
        elif self.main_window_state == CHARACTER_MAIN_WINDOW_STATE:
            self.character_window.handle_events(event, mouse_pos)
        elif self.main_window_state == DUNGEON_MAIN_WINDOW_STATE:
            self.dungeon_window.handle_events(event, mouse_pos)

        # character events

        self.character.check_level_up()

        # start item events

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.main_item_list != None:
            for num, item in enumerate(self.main_item_list):
                if item.rect.collidepoint(mouse_pos) and item.visible:
                    self.active_item = num
                    self.original_holder = None

                    for h in self.item_holder_list:
                        if h.type == self.main_item_list[self.active_item].type or h.type == INVENTORY:
                            h.highlight = True 
                        
                        if h.rect.colliderect(item.rect):
                            self.original_holder = h
                    break

        # item release events

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.active_item is not None:
                current_item = self.main_item_list[self.active_item]

                max_snap_distance = 100
                closest_holder = None
                min_dist = float("inf")

                # adjust for item_holder

                for holder in self.item_holder_list:
                    item_center = pygame.Vector2(current_item.rect.center)
                    holder_center = pygame.Vector2(holder.rect.center)
                    dist = item_center.distance_to(holder_center)

                    if dist < min_dist:
                        min_dist = dist
                        closest_holder = holder

                snap_condition = True

                # check if really halfway in shop to sell
                if closest_holder:
                    if closest_holder.type == SHOP:
                        if not closest_holder.rect.collidepoint(current_item.rect.center):
                            snap_condition = False
                    else:
                        if min_dist >= max_snap_distance:
                            snap_condition = False
                else:
                    snap_condition = False

                occupying_item = None
                move_item_to_inventory = False

                # check if new slot is full
                if snap_condition:
                    for item in self.main_item_list:
                        if item.rect.colliderect(closest_holder.rect) and item != current_item:
                            occupying_item = item
                            break

                # delete item when over shop
                if snap_condition and closest_holder.type == SHOP and self.original_holder.type != SHOP and self.main_window_state == SHOP_MAIN_WINDOW_STATE:
                    self.remove_item_from_holder(current_item, self.original_holder)
                    self.character.clear_character_stats()
                    self.main_item_list.remove(current_item)
                    for h in self.item_holder_list:
                        h.highlight = False
                    self.character.gold += current_item.sell_value
                    self.active_item = None
                    return
                
                # item doesnt match type not snap
                if snap_condition and closest_holder.type != current_item.type and closest_holder.type != INVENTORY:
                    snap_condition = False

                # character not enough money TODO: Implement Info for player
                if snap_condition and self.original_holder.type == SHOP and (self.character.gold - current_item.gold_value) < 0:
                    snap_condition = False

                if occupying_item:
                    # shop item has no slot because slot is occupied
                    if self.original_holder.type == SHOP:
                        if self.get_free_inventory_slot() is not None:
                            move_item_to_inventory = True
                        else:
                            snap_condition = False
                    # cant swap items if no type match
                    elif occupying_item.type != self.original_holder.type and self.original_holder.type != INVENTORY:
                        snap_condition = False

                # snap item to holder
                if snap_condition:

                    # add new item where bought item was
                    if self.original_holder.type == SHOP:
                        self.shop_window.create_new_item(self.original_holder)
                        self.character.gold += -current_item.gold_value

                    if occupying_item:
                        new_holder = None

                        if move_item_to_inventory:
                            new_holder = self.get_free_inventory_slot()
                        else:
                            new_holder = self.original_holder

                        # check condition to remove and add for old item
                        self.remove_item_from_holder(occupying_item, closest_holder)
                        self.add_item_to_holder(occupying_item, new_holder)
                        # set old item to old item slot
                        occupying_item.rect.center = new_holder.rect.center
                        occupying_item.x, occupying_item.y = occupying_item.rect.center

                    # check condition to remove and add for current item
                    self.remove_item_from_holder(current_item, self.original_holder)
                    self.add_item_to_holder(current_item, closest_holder)

                    # set new item to new item slot
                    current_item.rect.center = closest_holder.rect.center
                    current_item.x, current_item.y = current_item.rect.center

                    self.character.clear_character_stats()

                else:
                    # return to origin
                    current_item.rect.center = (current_item.x, current_item.y)
                
                for h in self.item_holder_list:
                    h.highlight = False
                    self.active_item = None

        if event.type == pygame.MOUSEMOTION:
            if self.active_item != None:
                rel_x = event.rel[0] / self.system.scale_factor
                rel_y = event.rel[1] / self.system.scale_factor
                self.main_item_list[self.active_item].rect.move_ip(rel_x, rel_y)

    def draw(self, canvas, mouse_pos):

        for button in self.main_button_list:
            button.draw(canvas, mouse_pos)

        show_text(canvas, f"Gold: {round(self.character.gold, 2)}", x = 25, y = 15, color = "yellow")

        show_text(canvas, f"Mouse: {mouse_pos}", x = 10, y = 850, color = "white")

        # left menu rect
        create_rectangle(canvas, 0, 0, 200, 1080, 5, "blue")

        # right main rect
        create_rectangle(canvas, 195, 0, 1725, 1080, 5, "blue")

        # window states

        for item in self.character.inventory:
            if item not in self.main_item_list:
                self.main_item_list.append(item)

        for item in self.character.equipment:
            if item not in self.main_item_list:
                self.main_item_list.append(item)

        if self.main_window_state == DEFAULT_MAIN_WINDOW_STATE:
            pass
        elif self.main_window_state == QUEST_MAIN_WINDOW_STATE:
            self.quest_window.draw(canvas, mouse_pos)
        elif self.main_window_state == SHOP_MAIN_WINDOW_STATE:
            for holder in self.item_holder_list:
                holder.draw(canvas, mouse_pos)
            self.shop_window.draw(canvas, mouse_pos, self.active_item)
        elif self.main_window_state == CHARACTER_MAIN_WINDOW_STATE:
            for holder in self.item_holder_list:
                if holder.type != SHOP:
                    holder.draw(canvas, mouse_pos)
            self.character_window.draw(canvas, mouse_pos, self.active_item)
        elif self.main_window_state == DUNGEON_MAIN_WINDOW_STATE:
            self.dungeon_window.draw(canvas, mouse_pos)

        if self.main_window_state == CHARACTER_MAIN_WINDOW_STATE:
            self.set_items_to_visible(self.character_window.main_item_list)
            self.set_items_to_invisible(self.character.shop_items)
        elif self.main_window_state == SHOP_MAIN_WINDOW_STATE:
            self.set_items_to_visible(self.main_item_list)
        else:
            self.set_items_to_invisible(self.main_item_list)

        for item in self.main_item_list:
            if item.visible:
                item.draw(canvas, mouse_pos)

        # draw tooltips

        if self.active_item is None:
            for num, item in enumerate(self.main_item_list):
                if item.visible and num != self.active_item:
                    if item not in self.character.equipment:
                        if item.rect.collidepoint(mouse_pos):
                            self.on_item_hover(item)

                    item.tooltip.draw(canvas, mouse_pos, item.rect, self.system.screen.height)

        if self.main_window_state == CHARACTER_MAIN_WINDOW_STATE:
            self.character_window.character_blueprint.exp_bar_tooltip.draw(canvas, mouse_pos, self.character_window.character_blueprint.exp_bar)
        elif self.main_window_state == SHOP_MAIN_WINDOW_STATE:
            self.shop_window.character_blueprint.exp_bar_tooltip.draw(canvas, mouse_pos, self.shop_window.character_blueprint.exp_bar)

        if self.active_item is not None:
            if self.main_item_list[self.active_item].is_compare_tooltip:
                self.main_item_list[self.active_item].create_tooltip()
            self.main_item_list[self.active_item].draw(canvas, mouse_pos)
