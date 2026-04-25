import pygame
import asyncio
import sys
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
    def __init__(self):
        pygame.init()
        self.is_web = sys.platform == "emscripten"
        self.settings = Settings()
        self.is_fullscreen = False

        if self.is_web:
            self.screen = pygame.display.set_mode((self.settings.base_width, self.settings.base_height))
        else: 
            self.screen = pygame.display.set_mode((self.settings.base_width, self.settings.base_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        self.save_service = Save_Service(self)
        self.save_service.load_progress()

        if self.settings.forced_width and self.settings.forced_height:
            self.screen = pygame.display.set_mode((self.settings.forced_width, self.settings.forced_height), pygame.RESIZABLE | pygame.DOUBLEBUF)

        self.intro = Intro()

        self.all_shops_data = self.save_service.shop_list

        self.character_list: list[Character] = self.save_service.character_list
        self.menu = Menu(self.settings, self)
        self.character: Character = None

        if self.is_fullscreen:
            self.toggle_fullscreen(no_toggle = True)
        
        pygame.display.set_caption(self.settings.title)

        self.last_window_size = (self.settings.base_width, self.settings.base_height)

        self.canvas = pygame.Surface((self.settings.base_width, self.settings.base_height))

        self.clock = pygame.time.Clock()
        self.running = True

        self.main_item_list: list[Item] = []
        self.active_item = None
        self.main_button_list = []

        # this is to ensure what main menu is shown: Intro, Menu, Options, Game, Character_Slots, Character Add Screen
        self.menu_state = INTRO_STATE

        self.main_window_state = DEFAULT_MAIN_WINDOW_STATE
        self.quest_window = Quest_Window(self.character, self)
        self.shop_window = Shop_Window(self.character, self.main_item_list)
        self.character_window = Character_Window(self.character, self.main_item_list)
        self.dungeon_window = Dungeon_Window(self.character)

        self.item_holder_list: list[Item_Holder] = self.shop_window.item_holder_list + self.character_window.item_holder_list

        # dynamic display

        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0

        if not self.is_web:
            self.calc_scale(self.settings.forced_width, self.settings.forced_height)
        self.create_buttons()

    def create_buttons(self):
        btn_quest = Button(position = (100, 100), size = (150, 50), text = "Questboard", change_color = [150, 150, 150], func = lambda: self.toggle_main_state(QUEST_MAIN_WINDOW_STATE))
        btn_character = Button(position = (100, 170), size = (150, 50), text = "Character", change_color = [150, 150, 150], func = lambda: self.toggle_main_state(CHARACTER_MAIN_WINDOW_STATE))
        btn_shop = Button(position = (100, 240), size = (150, 50), text = "Shop", change_color = [150, 150, 150], func = lambda: self.toggle_main_state(SHOP_MAIN_WINDOW_STATE))
        btn_dungeon = Button(position = (100, 310), size = (150, 50), text = "Dungeon", change_color = [150, 150, 150], func = lambda: self.toggle_main_state(DUNGEON_MAIN_WINDOW_STATE))
        btn_back = Button(position=(100, 925), size=(100, 50), text="Back", color=[150, 50, 50], change_color=[200, 50, 50], func= lambda: self.menu.change_menu_state(CHARACTER_SLOTS_STATE))
        btn_quit = Button(position=(100, 995), size=(100, 50), text="Quit", color=[150, 50, 50], change_color=[200, 50, 50], func= lambda: self.quit_game())
        #btn_test = Button(position=(100, 1050), size=(100, 40), text="Test", color=[200, 50, 50], func= lambda: self.set_specific_window_size(1280, 720))

        self.main_button_list = [btn_quest, btn_character, btn_shop, btn_dungeon, btn_back, btn_quit]

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

    def quit_game(self):
        if self.is_web:
            return
        self.save_service.save_progress(self)
        self.running = False

    def calc_scale(self, new_screen_w = None, new_screen_h = None):
        """
        Calculates how much to scale the game to fit the window
        while maintaining aspect ratio.
        """
        
        if new_screen_w and new_screen_h:
            screen_w, screen_h = new_screen_w, new_screen_h
        else:
            screen_w, screen_h = self.screen.get_size()

        base_w, base_h = self.settings.base_width, self.settings.base_height

        self.scale_factor = min(screen_w / base_w, screen_h / base_h)

        new_w = int(base_w * self.scale_factor)
        new_h = int(base_h * self.scale_factor)

        self.offset_x = (screen_w - new_w) // 2
        self.offset_y = (screen_h - new_h) // 2

    def get_virtual_mouse_pos(self):
        """
        Translates the real mouse position on the monitor 
        to the coordinate system of the 1280x720 canvas.
        """

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Remove the offset (black bars)
        x_on_scaled_surface = mouse_x - self.offset_x
        y_on_scaled_surface = mouse_y - self.offset_y

        # Scale back down
        virtual_x = int(x_on_scaled_surface / self.scale_factor)
        virtual_y = int(y_on_scaled_surface / self.scale_factor)

        # Clamp ensures we don't get coordinates outside the game area
        virtual_x = max(0, min(virtual_x, self.settings.base_width))
        virtual_y = max(0, min(virtual_y, self.settings.base_height))

        return (virtual_x, virtual_y)
    
    def toggle_fullscreen(self, is_fullscreen = None, no_toggle = False):
        if self.is_web:
           return 

        if not no_toggle:
            self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.last_window_size = self.screen.get_size()

            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)

            self.menu.resolution_drop_down.locked = True
            if self.menu.resolution_drop_down.display_item:
                self.menu.resolution_drop_down.selected_item = self.menu.resolution_drop_down.display_item
            else:
                self.menu.resolution_drop_down.selected_item = "-"
            
            self.settings.forced_width = None
            self.settings.forced_height = None

        else:
            self.screen = pygame.display.set_mode(self.last_window_size, pygame.RESIZABLE | pygame.DOUBLEBUF)
            self.menu.resolution_drop_down.locked = False

        self.calc_scale()

    def toggle_main_state(self, new_window_state):
        if self.main_window_state == new_window_state:
            self.main_window_state = DEFAULT_MAIN_WINDOW_STATE
        else:
            self.main_window_state = new_window_state

    def sync_character_to_ui(self):
        if not self.character:
            return

        self.main_item_list.clear()
        
        self.main_item_list.extend(self.character.inventory)
        self.main_item_list.extend(self.character.equipment)
        
        if not hasattr(self.character, 'shop_items') or self.character.shop_items is None:
            self.character.shop_items = []

        if not self.character.shop_items:
            self.shop_window.character = self.character
            self.shop_window.reroll_shop()
        else:
            self.main_item_list.extend(self.character.shop_items)

        self.shop_window.character = self.character
        self.character_window.character = self.character
        
        for i, item in enumerate(self.character.shop_items):
            if i < len(self.shop_window.item_holder_list):
                item.rect.center = self.shop_window.item_holder_list[i].rect.center
                item.x, item.y = item.rect.center

    def set_specific_window_size(self, width, height):
        self.settings.forced_width = width
        self.settings.forced_height = height
        self.calc_scale(width, height)
        self.screen = pygame.display.set_mode((self.settings.forced_width, self.settings.forced_height), pygame.RESIZABLE | pygame.DOUBLEBUF)

    async def start(self):

        while self.running:

            mouse_pos = self.get_virtual_mouse_pos()

            # event handling

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                for button in self.main_button_list:
                    button.handle_event(event, mouse_pos)

                # event handling window states

                if self.menu_state == MENU_STATE:
                    self.menu.handle_events(event, mouse_pos)

                elif self.menu_state == OPTIONS_STATE:
                    self.menu.handle_options_events(event, mouse_pos)

                elif self.menu_state == CHARACTER_SLOTS_STATE:
                    self.menu.handle_character_slot_events(event, mouse_pos)

                elif self.menu_state == CHARACTER_ADD_STATE:
                    pass
                    #self.menu.handle_character_add_events(event, mouse_pos)

                elif self.menu_state == GAME_STATE:
                    if self.main_window_state == DEFAULT_MAIN_WINDOW_STATE:
                        pass
                    elif self.main_window_state == QUEST_MAIN_WINDOW_STATE:
                        self.quest_window.handle_events(event, mouse_pos, self.character)
                    elif self.main_window_state == SHOP_MAIN_WINDOW_STATE:
                        self.shop_window.handle_events(event, mouse_pos, self.character)
                    elif self.main_window_state == CHARACTER_MAIN_WINDOW_STATE:
                        self.character_window.handle_events(event, mouse_pos, self.character)
                    elif self.main_window_state == DUNGEON_MAIN_WINDOW_STATE:
                        self.dungeon_window.handle_events(event, mouse_pos, self.character)
 
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
                                self.character.calculate_player_stats()
                                self.main_item_list.remove(current_item)
                                for h in self.item_holder_list:
                                    h.highlight = False
                                self.character.gold += current_item.sell_value
                                self.active_item = None
                                continue
                            
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

                                self.character.calculate_player_stats()

                            else:
                                # return to origin
                                current_item.rect.center = (current_item.x, current_item.y)
                            
                            for h in self.item_holder_list:
                                h.highlight = False
                                self.active_item = None

                    if event.type == pygame.MOUSEMOTION:
                        if self.active_item != None:
                            rel_x = event.rel[0] / self.scale_factor
                            rel_y = event.rel[1] / self.scale_factor
                            self.main_item_list[self.active_item].rect.move_ip(rel_x, rel_y)   

                if event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.calc_scale()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()

            # drawing

            self.canvas.fill("black")

            if self.menu_state == INTRO_STATE:
                self.intro.draw(self.canvas, self.settings.base_width / 2, self.settings.base_height / 2)
                if self.intro.fade_out_complete:
                    self.menu_state = MENU_STATE
            else:
                # global except intro
                show_text(self.canvas, f"{GAME_VERSION}", x = 10, y = 1050, color= "lightblue")

            if self.menu_state == MENU_STATE:
                self.menu.draw(self.canvas, mouse_pos)

            elif self.menu_state == CHARACTER_SLOTS_STATE:
                self.menu.draw_character_slots(self.canvas, mouse_pos)

            elif self.menu_state == CHARACTER_ADD_STATE:
                pass
                #self.menu.draw_character_add_screen(self.canvas, mouse_pos)

            elif self.menu_state == OPTIONS_STATE:
                self.menu.draw_options(self.canvas, mouse_pos)

            elif self.menu_state == GAME_STATE:

                for button in self.main_button_list:
                    button.draw(self.canvas, mouse_pos)

                show_text(self.canvas, f"Gold: {round(self.character.gold, 2)}", x = 25, y = 15, color = "yellow")

                show_text(self.canvas, f"Mouse: {mouse_pos}", x = 10, y = 850, color = "white")

                # left menu rect
                create_rectangle(self.canvas, 0, 0, 200, 1080, 5, "blue")

                # right main rect
                create_rectangle(self.canvas, 195, 0, 1725, 1080, 5, "blue")

                # window states

                if self.main_window_state == DEFAULT_MAIN_WINDOW_STATE:
                    pass
                elif self.main_window_state == QUEST_MAIN_WINDOW_STATE:
                    self.quest_window.draw(self.canvas, mouse_pos)
                elif self.main_window_state == SHOP_MAIN_WINDOW_STATE:
                    for holder in self.item_holder_list:
                        holder.draw(self.canvas, mouse_pos)
                    self.shop_window.draw(self.canvas, mouse_pos, self.active_item)
                elif self.main_window_state == CHARACTER_MAIN_WINDOW_STATE:
                    for holder in self.item_holder_list:
                        if holder.type != SHOP:
                            holder.draw(self.canvas, mouse_pos)
                    self.character_window.draw(self.canvas, mouse_pos, self.active_item)
                elif self.main_window_state == DUNGEON_MAIN_WINDOW_STATE:
                    self.dungeon_window.draw(self.canvas, mouse_pos)

                if self.main_window_state == CHARACTER_MAIN_WINDOW_STATE:
                    self.set_items_to_visible(self.character_window.main_item_list)
                    self.set_items_to_invisible(self.character.shop_items)
                elif self.main_window_state == SHOP_MAIN_WINDOW_STATE:
                    self.set_items_to_visible(self.main_item_list)
                else:
                    self.set_items_to_invisible(self.main_item_list)

                for item in self.main_item_list:
                    if item.visible:
                        item.draw(self.canvas, mouse_pos)

                if self.active_item is not None:
                    self.main_item_list[self.active_item].draw(self.canvas, mouse_pos)

            self.screen.fill((20, 20, 20))

            scaled_surf = pygame.transform.smoothscale(self.canvas, (int(self.settings.base_width * self.scale_factor), int(self.settings.base_height * self.scale_factor)))

            self.screen.blit(scaled_surf, (self.offset_x, self.offset_y))
            
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

            await asyncio.sleep(0)

async def main():
    game = Game()
    await game.start()

if __name__ == "__main__":
    asyncio.run(main())