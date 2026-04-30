import pygame
import asyncio
import sys
from game import *
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

class System():
    def __init__(self):
        pygame.init()
        self.is_web = sys.platform == WEB_PLATFORM
        self.settings = Settings()

        if self.is_web:
            self.screen = pygame.display.set_mode((self.settings.base_width, self.settings.base_height))
        else: 
            self.screen = pygame.display.set_mode((self.settings.base_width, self.settings.base_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        
        if self.settings.forced_width and self.settings.forced_height:
            self.screen = pygame.display.set_mode((self.settings.forced_width, self.settings.forced_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        
        self.intro = Intro()

        self.start_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()

        # auto save
        self.last_auto_save_time = 0
        self.auto_save_interval = 1 * 60 * 1000

        self.save_service = Save_Service(self, self.settings)
        self.save_service.load_options()

        self.menu = Menu(self, self.settings)
        self.game: Game = None

        if self.settings.is_fullscreen:
            self.toggle_fullscreen(no_toggle = True)
        
        pygame.display.set_caption(self.settings.title)

        self.last_window_size = (self.settings.base_width, self.settings.base_height)

        self.canvas = pygame.Surface((self.settings.base_width, self.settings.base_height))

        self.running = True

        # this is to ensure what main menu is shown: Intro, Menu, Options, Game, Character_Slots, Character Add Screen
        self.menu_state = INTRO_STATE

        # dynamic display

        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0

        if not self.is_web:
            self.calc_scale(self.settings.forced_width, self.settings.forced_height)

    def get_virtual_mouse_pos(self):

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
    
    def quit_game(self, already_saved = False):
        if self.is_web:
            return
                
        if not already_saved:
            if self.game:
                self.save_service.save_data(self.game.all_shops_data, self.game.character_list, self.game.character.dungeon_completed, self.game.quest_window.quest_list)
            self.save_service.game_time = self.total_time_ms
            self.save_service.save_options(self.settings)
        self.running = False

    def start_total_game_time(self):
        self.session_time_ms = pygame.time.get_ticks() - self.start_time
        
        self.total_time_ms = self.save_service.game_time + self.session_time_ms

    def perform_auto_saving(self):
        if self.settings.auto_save and self.session_time_ms - self.last_auto_save_time >= self.auto_save_interval:
            if self.game:
                self.save_service.save_data(self.game.all_shops_data, self.game.character_list, self.game.character.dungeon_completed, self.game.quest_window.quest_list)
            self.save_service.save_options(self.settings)
            self.last_auto_save_time = self.session_time_ms
            # TODO: SHOW THE USER ITS AUTOSAVING

    def toggle_fullscreen(self, is_fullscreen = None, no_toggle = False):
        if self.is_web:
           return 

        if not no_toggle:
            self.settings.is_fullscreen = not self.settings.is_fullscreen

        if self.settings.is_fullscreen:
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

    def set_specific_window_size(self, width, height):
        self.settings.forced_width = width
        self.settings.forced_height = height
        self.calc_scale(width, height)
        self.screen = pygame.display.set_mode((self.settings.forced_width, self.settings.forced_height), pygame.RESIZABLE | pygame.DOUBLEBUF)

    def switch_menu_state(self, new_state):
        self.menu.show_add_text_editor = False

        if new_state == CHARACTER_SLOTS_STATE or new_state == GAME_STATE:

            previous_character_list = (
                self.menu.character_list[:] if self.menu.character_list else None
            )

            self.save_service.load_data()
            self.menu.character_list = self.save_service.character_list

            if previous_character_list: 
                for i, char in enumerate(previous_character_list):
                    if char is not None and self.menu.character_list[i] is None:
                        self.menu.character_list[i] = char
                        self.save_service.character_list[i] = char
                        self.save_service.character_list[i].shop_items = self.save_service.shop_list[i]

            if new_state == GAME_STATE:
                self.game = Game(self, self.save_service.character_list, self.save_service.character_list[self.menu.character_slot], self.save_service.shop_list[self.menu.character_slot], self.save_service.shop_list)
                self.game.character = self.save_service.character_list[self.menu.character_slot]
                self.game.character.clear_character_stats()

        self.menu_state = new_state

    def draw(self, mouse_pos):
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

        elif self.menu_state == OPTIONS_STATE:
            self.menu.draw_options(self.canvas, mouse_pos)

        elif self.menu_state == GAME_STATE:
            self.game.draw(self.canvas, mouse_pos)

    async def run(self):
        
        while self.running:

            mouse_pos = self.get_virtual_mouse_pos()

            # total game time

            self.start_total_game_time()

            # auto saving

            self.perform_auto_saving()

            # event handling

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.VIDEORESIZE:
                    if not self.settings.is_fullscreen:
                        self.calc_scale()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()

                if self.menu_state == MENU_STATE:
                    self.menu.handle_events(event, mouse_pos)

                elif self.menu_state == OPTIONS_STATE:
                    self.menu.handle_options_events(event, mouse_pos)

                elif self.menu_state == CHARACTER_SLOTS_STATE:
                    self.menu.handle_character_slot_events(event, mouse_pos)
                
                elif self.menu_state == GAME_STATE:
                    self.game.handle_events(event, mouse_pos)


            self.draw(mouse_pos)

            self.screen.fill((20, 20, 20))

            scaled_surf = pygame.transform.smoothscale(self.canvas, (int(self.settings.base_width * self.scale_factor), int(self.settings.base_height * self.scale_factor)))

            self.screen.blit(scaled_surf, (self.offset_x, self.offset_y))
            
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

            await asyncio.sleep(0)

async def main():
    system = System()
    await system.run()

if __name__ == "__main__":
    asyncio.run(main())