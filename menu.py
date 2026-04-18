from utils import *
from settings import *
from character import *
import pygame

class Menu:
    def __init__(self, settings: Settings, game):
        self.settings = settings
        self.game = game
        self.character_slot = 0
        self.character_list = None
        self.cursor_focused = False
        self.menu_button_list = []
        self.character_slot_list = []
        self.character_slot_buttons = []
        self.options_button = []
        self.options_slider = []
        self.options_toggle = []

        # create ui elements
        self.create_main_menu_buttons()
        self.create_character_slot_buttons()
        self.create_options_menu_button()
        self.create_options_slider()
        self.create_options_toggle()

    def create_main_menu_buttons(self):
        width = 250
        height = 100
        spacing = 20

        center_x = INITIAL_SCREEN_WIDTH / 2
        center_y = INITIAL_SCREEN_HEIGHT / 2

        start_button = Button(position = (center_x, center_y - height - spacing), size = (width, height), text = "Start", change_color = [150, 150, 150], func= lambda: self.change_menu_state(CHARACTER_SLOTS_STATE))
        options_button = Button(position = (center_x, center_y), size = (width, height), text = "Options", change_color = [150, 150, 150], func= lambda: self.change_menu_state(OPTIONS_STATE))
        quit_buttton = Button(position = (center_x, center_y + height + spacing), size = (width, height), text = "Quit", change_color = [150, 150, 150], func= lambda: self.game.quit_game())

        self.menu_button_list = [start_button, options_button, quit_buttton]

    def create_character_slot_buttons(self):
        width = 300
        height = 600
        spacing = 20

        center_x = INITIAL_SCREEN_WIDTH / 2 - width / 2
        center_y = INITIAL_SCREEN_HEIGHT / 2 - height / 2

        back_button = Button(position = (center_x + width / 2, center_y + height + spacing * 2), size = (150, 50), text = "Back", change_color = [150, 150, 150], func= lambda: self.change_menu_state(MENU_STATE))
        self.character_slot_buttons = [back_button]

    def change_menu_state(self, new_state):
        self.game.menu_state = new_state

    def create_options_menu_button(self):
        mid_x = self.settings.base_width / 2
        mid_y = self.settings.base_height / 2

        options_back = Button(position= (mid_x, mid_y + 120),size= (150, 50), text= "Back", change_color = [150, 150, 150], func= lambda: self.change_menu_state(MENU_STATE))
        self.options_button = [options_back]

    def create_options_slider(self):
        mid_x = self.settings.base_width / 2
        mid_y = self.settings.base_height / 2

        MUSIC_SLIDER = VolumeSlider(size=(200, 20), font=get_font(25), label="music volume:",
                                initial_value=int(self.settings.music_volume * 100),
                                on_change=self.settings.on_music_volume_change, center_pos= (mid_x, mid_y), text_color= "white", slider_color= "gray", slider_picker_color= "white")
    
        SOUND_SLIDER = VolumeSlider(size=(200, 20), font=get_font(25), label="sound volume:",
                                initial_value=int(self.settings.sound_volume * 100),
                                on_change=self.settings.on_sound_volume_change, center_pos= (mid_x, mid_y + 30), text_color= "white", slider_color= "gray", slider_picker_color= "white")
        
        self.options_slider = [MUSIC_SLIDER, SOUND_SLIDER]

    def create_options_toggle(self):
        mid_x = self.settings.base_width / 2
        mid_y = self.settings.base_height / 2
        
        MUSIC_TOGGLE = SliderToggle(pos=(mid_x, mid_y - 120), size=(100, 40), font=get_font(30),
                                    label="music:", initial_state=self.settings.music_on,
                                    on_toggle=self.settings.on_toggle_music, text_color= "white")
        
        SOUND_TOGGLE = SliderToggle(pos=(mid_x, mid_y - 70), size=(100, 40), font=get_font(30),
                                    label="sound effects:", initial_state=self.settings.sounds_on,
                                    on_toggle=self.settings.on_toggle_sound, text_color= "white")

        self.options_toggle = [MUSIC_TOGGLE, SOUND_TOGGLE]

    def draw_options(self, canvas, mouse_pos):

        for toggle in self.options_toggle:
            toggle.update((toggle.center_x, toggle.center_y))
            toggle.draw(canvas)

        for button in self.options_button:
            button.draw(canvas, mouse_pos)

        for slider in self.options_slider:
            slider.draw(canvas)

    def draw_character_slots(self, canvas, mouse_pos):
        width = 300
        height = 600
        spacing = 20

        center_x = INITIAL_SCREEN_WIDTH / 2 - width / 2
        center_y = INITIAL_SCREEN_HEIGHT / 2 - height / 2

        first_character: Character = self.game.character_list[0]

        character_slot_1 = create_rectangle(canvas, center_x - width - spacing, center_y, width, height, 4, "gray")

        show_text(canvas, "Slot 1", character_slot_1.x + character_slot_1.width / 2, character_slot_1.y + 20, "white", True)
        show_text(canvas, f"{first_character.name}", character_slot_1.x + character_slot_1.width / 2, character_slot_1.y + 20 + 50, "white", True)
        show_text(canvas, f"Level: {first_character.level}", character_slot_1.x + character_slot_1.width / 2, character_slot_1.y + 20 + 100, "green", True)

        second_character: Character = self.game.character_list[1]

        character_slot_2 = create_rectangle(canvas, center_x, center_y, width, height, 4, "gray")

        show_text(canvas, "Slot 2", character_slot_2.x + character_slot_2.width / 2, character_slot_2.y + 20, "white", True)
        show_text(canvas, f"{second_character.name}", character_slot_2.x + character_slot_2.width / 2, character_slot_2.y + 20 + 50, "white", True)
        show_text(canvas, f"Level: {second_character.level}", character_slot_2.x + character_slot_2.width / 2, character_slot_2.y + 20 + 100, "green", True)

        third_character: Character = self.game.character_list[2]

        character_slot_3 = create_rectangle(canvas, center_x + width + spacing, center_y, width, height, 4, "gray")

        show_text(canvas, "Slot 3", character_slot_3.x + character_slot_3.width / 2, character_slot_3.y + 20, "white", True)
        show_text(canvas, f"{third_character.name}", character_slot_3.x + character_slot_3.width / 2, character_slot_3.y + 20 + 50, "white", True)
        show_text(canvas, f"Level: {third_character.level}", character_slot_3.x + character_slot_3.width / 2, character_slot_3.y + 20 + 100, "green", True)

        self.character_slot_list = [character_slot_1, character_slot_2, character_slot_3]

        for button in self.character_slot_buttons:
            button.draw(canvas, mouse_pos)

    def handle_character_slot_events(self, event, mouse_pos):
        self.cursor_focused = False

        for button in self.character_slot_buttons:
            button.handle_event(event, mouse_pos)

        for character_slot in self.character_slot_list:
            if character_slot.collidepoint(mouse_pos):
                self.cursor_focused = True
        
        if self.cursor_focused:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for num, character_slot in enumerate(self.character_slot_list):
                if character_slot.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.character_slot = num
                    self.game.character = self.game.character_list[self.character_slot]
                    self.game.menu_state = GAME_STATE

    def handle_options_events(self, event, mouse_pos):
        for toggle in self.options_toggle:
            toggle.handle_event(event, mouse_pos)

        for slider in self.options_slider:
            slider.handle_event(event)

        for button in self.options_button:
            button.handle_event(event, mouse_pos)

    def draw(self, canvas, mouse_pos):

        for button in self.menu_button_list:
            button.draw(canvas, mouse_pos)

    def handle_events(self, event, mouse_pos):

        for button in self.menu_button_list:
            button.handle_event(event, mouse_pos)
