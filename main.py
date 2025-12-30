import pygame
from character import *
from quest_window import *
from settings import *
from utils import *

class Game():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.character = Character()

        self.screen = pygame.display.set_mode((self.settings.base_width, self.settings.base_height), pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.settings.title)

        self.is_fullscreen = False
        self.last_window_size = (self.settings.base_width, self.settings.base_height)

        self.canvas = pygame.Surface((self.settings.base_width, self.settings.base_height))

        self.main_button_list = []

        self.clock = pygame.time.Clock()
        self.running = True

        self.main_window_state = DEFAULT_MAIN_WINDOW_STATE
        self.quest_window = Quest_Window(self.character, self)

        # dynamic display

        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0

        self.calc_scale()
        self.create_objects()

    def create_objects(self):

        btn_quest = Button(position = (100, 100), size = (150, 50), text = "Questboard", change_color = [150, 150, 150], func = lambda: self.toggle_main_state(QUEST_MAIN_WINDOW_STATE))
        btn_character = Button(position = (100, 170), size = (150, 50), text = "Character", change_color = [150, 150, 150], func = lambda: self.toggle_main_state(CHARACTER_MAIN_WINDOW_STATE))
        btn_dungeon = Button(position = (100, 240), size = (150, 50), text = "Dungeon", change_color = [150, 150, 150], func = lambda: self.toggle_main_state(DUNGEON_MAIN_WINDOW_STATE))
        btn_quit = Button(position=(100, 1000), size=(100, 50), text="Quit", color=[150, 50, 50], change_color=[200, 50, 50], func= lambda: self.quit_game())

        self.main_button_list = [btn_quest, btn_character, btn_dungeon, btn_quit]

    def quit_game(self):
        self.running = False

    def calc_scale(self):
        """
        Calculates how much to scale the game to fit the window
        while maintaining aspect ratio.
        """
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
    
    def toggle_fullscreen(self):

        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.last_window_size = self.screen.get_size()

            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)

        else:
            self.screen = pygame.display.set_mode(self.last_window_size, pygame.RESIZABLE | pygame.DOUBLEBUF)

        self.calc_scale()

    def toggle_main_state(self, new_window_state):
        if self.main_window_state == new_window_state:
            self.main_window_state = DEFAULT_MAIN_WINDOW_STATE
        else:
            self.main_window_state = new_window_state

    def start(self):

        while self.running:

            mouse_pos = self.get_virtual_mouse_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.main_button_list:
                            button.click(mouse_pos)

                    # event handling window states
                    if self.main_window_state == DEFAULT_MAIN_WINDOW_STATE:
                        pass
                    elif self.main_window_state == QUEST_MAIN_WINDOW_STATE:
                        self.quest_window.handle_events(event, mouse_pos)
                    elif self.main_window_state == CHARACTER_MAIN_WINDOW_STATE:
                        pass
                    elif self.main_window_state == DUNGEON_MAIN_WINDOW_STATE:
                        pass

                if event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.calc_scale()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    if event.key == pygame.K_ESCAPE:
                        self.quit_game()

            self.canvas.fill("black")

            for button in self.main_button_list:
                button.draw(self.canvas, mouse_pos)

            show_text(self.canvas, f"Gold: {self.character.gold}", x = 25, y = 15, color = "yellow")
            show_text(self.canvas, f"EXP: {self.character.experience}", x = 25, y = 35, color = "green")

            show_text(self.canvas, f"Mouse: {mouse_pos}", x = 10, y = 850, color = "white")

            # left menu rect
            create_rectangle(self.canvas, 0, 0, 200, 1080, 5, "blue")

            # right main rect
            create_rectangle(self.canvas, 195, 0, 1725, 1080, 5, "blue")

            # window states
            if self.main_window_state == QUEST_MAIN_WINDOW_STATE:
                self.quest_window.draw(self.canvas, mouse_pos)

            self.screen.fill((20, 20, 20))

            scaled_surf = pygame.transform.smoothscale(self.canvas, (int(self.settings.base_width * self.scale_factor), int(self.settings.base_height * self.scale_factor)))

            self.screen.blit(scaled_surf, (self.offset_x, self.offset_y))
            
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

if __name__ == "__main__":
    Game().start()