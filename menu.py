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
        self.character_add_text_editor = Text_Input_Box(0, 0, 250, 50, "white", "gray", "black")
        self.show_add_text_editor = False
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
        center_x = INITIAL_SCREEN_WIDTH / 2
        back_button = Button(position=(center_x, INITIAL_SCREEN_HEIGHT - 100), size=(150, 50), text="Back", change_color= [150, 150, 150], func=lambda: self.change_menu_state(MENU_STATE))
        self.character_slot_buttons = [back_button]

        self.add_buttons = []
        for i in range(3):
            btn = Button(position=(0, 0), size=(50, 50), text="+", change_color= [150, 150, 150], func= lambda idx = i: self.show_text_editor(btn.rect.centerx, btn.rect.centery, idx))
            self.add_buttons.append(btn)

    def change_menu_state(self, new_state):
        self.show_add_text_editor = False
        self.game.menu_state = new_state

    def create_options_menu_button(self):
        mid_x = self.settings.base_width / 2
        mid_y = self.settings.base_height / 2

        save_button = Button(position= (mid_x, mid_y + 120),size= (150, 50), text= "Save and close", change_color = [150, 150, 150], func= lambda: self.save_and_close(MENU_STATE))
        self.options_button = [save_button]

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

    def show_text_editor(self, x, y, i):
        self.character_slot = i
        self.character_add_text_editor.clear()
        self.character_add_text_editor.set_pos(x, y)
        self.show_add_text_editor = True

    def save_and_close(self, new_state):
        self.game.save_service.save_progress(self.game)
        self.change_menu_state(new_state)

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
        
        num_chars = len(self.game.character_list)
        total_width = (num_chars * width) + ((num_chars - 1) * spacing)
        start_x = (INITIAL_SCREEN_WIDTH - total_width) / 2
        center_y = (INITIAL_SCREEN_HEIGHT - height) / 2

        self.character_slot_list = []

        for i, character in enumerate(self.game.character_list):
            current_x = start_x + i * (width + spacing)
            
            slot = create_rectangle(canvas, current_x, center_y, width, height, 4, "gray")
            self.character_slot_list.append(slot)

            slot_center_x = slot.x + slot.width / 2
            slot_center_y = slot.y + slot.height / 2

            if character:
                show_text(canvas, f"Slot {i + 1}", slot_center_x, slot.y + 20, "white", True)
                show_text(canvas, f"{character.name}", slot_center_x, slot.y + 70, "white", True)
                show_text(canvas, f"Level: {character.level}", slot_center_x, slot.y + 120, "green", True)
            else:
                show_text(canvas, f"Slot {i + 1}", slot_center_x, slot.y + 20, "white", True)

                if self.show_add_text_editor and self.character_slot == i:
                    self.character_add_text_editor.set_pos(slot_center_x, slot_center_y)
                    self.character_add_text_editor.draw(canvas)
                else:
                    add_btn = self.add_buttons[i]
                    add_btn.set_pos((slot_center_x, slot_center_y))
                    add_btn.draw(canvas, mouse_pos)

        self.character_slot_buttons[0].draw(canvas, mouse_pos)

    def create_character_and_change_state(self, character_slot = None):
        if not character_slot:
            chosen_name = self.character_add_text_editor.text
            new_char = Character(chosen_name, None, 1, 1)
            self.game.character_list[self.character_slot] = new_char
        else:
            self.character_slot = character_slot
            self.game.character_slot = self.character_slot
            self.game.character_list[self.character_slot] = self.game.character_list[self.character_slot]

        self.game.character = self.game.character_list[self.character_slot]
        self.game.toggle_main_state(DEFAULT_MAIN_WINDOW_STATE)
        self.game.sync_character_to_ui()
        self.change_menu_state(GAME_STATE)

    def handle_character_slot_events(self, event, mouse_pos):
        if not self.character_slot_list:
            return

        self.cursor_focused = False

        self.character_slot_buttons[0].handle_event(event, mouse_pos)
            
        if self.show_add_text_editor:
            self.character_add_text_editor.handle_event(event, mouse_pos)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if len(self.character_add_text_editor.text) > 0:
                    self.create_character_and_change_state(None)
                    self.show_add_text_editor = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_add_text_editor = False
        
        for i, character in enumerate(self.game.character_list):
            if not character:
                self.add_buttons[i].handle_event(event, mouse_pos)
            else:
                if self.character_slot_list[i].collidepoint(mouse_pos):
                    self.cursor_focused = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.cursor_focused = False
                        self.create_character_and_change_state(i)
        
        if self.cursor_focused:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_options_events(self, event, mouse_pos):
        for toggle in self.options_toggle:
            toggle.handle_event(event, mouse_pos)

        for slider in self.options_slider:
            slider.handle_event(event, mouse_pos)

        for button in self.options_button:
            button.handle_event(event, mouse_pos)

    def draw(self, canvas, mouse_pos):
        for button in self.menu_button_list:
            button.draw(canvas, mouse_pos)

    def handle_events(self, event, mouse_pos):
        for button in self.menu_button_list:
            button.handle_event(event, mouse_pos)
