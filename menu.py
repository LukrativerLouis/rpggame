from utils import *
from settings import *
from character import *
import pygame

class Menu:
    def __init__(self, system, settings: Settings):
        self.settings = settings
        self.system = system
        self.character_slot = 0
        self.character_list = None
        self.cursor_focused = False
        self.character_add_text_box = Text_Input_Box(0, 0, 250, 50, "white", "gray", "black", f"{self.settings.translate('character_name')}:", "white")
        self.chracter_image_box = None
        self.character_class_box = Choosing_Element(0, 0, CLASS_TYPE_LIST, 100, 30, "gray", "white")
        self.resolution_drop_down = Drop_Down_Menu(self.settings.base_width / 2 - 200, self.settings.base_height / 2 + 70, DISPLAY_RESOLUTION_LIST, 200, 50, "gray", "white", 200, 50, "Display", func= lambda res_text: self.apply_resolution(res_text))
        self.language_drop_down = Drop_Down_Menu(self.settings.base_width / 2, self.settings.base_height / 2 + 70, LANGUAGE_LIST, 200, 50, "gray", "white", 200, 50, self.settings.language, func= lambda language: self.apply_language(language))
        self.show_add_text_editor = False
        self.show_character_class_box = False
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

        start_button = Button(position = (center_x, center_y - height - spacing), size = (width, height), text = self.settings.translate("title_start"), change_color = [150, 150, 150], func= lambda: self.system.switch_menu_state(CHARACTER_SLOTS_STATE))
        options_button = Button(position = (center_x, center_y), size = (width, height), text = self.settings.translate("title_options"), change_color = [150, 150, 150], func= lambda: self.system.switch_menu_state(OPTIONS_STATE))
        quit_buttton = Button(position = (center_x, center_y + height + spacing), size = (width, height), text = self.settings.translate("title_quit"), change_color = [150, 150, 150], func= lambda: self.system.quit_game())

        self.menu_button_list = [start_button, options_button, quit_buttton]

    def create_character_slot_buttons(self):
        center_x = INITIAL_SCREEN_WIDTH / 2
        back_button = Button(position=(center_x, INITIAL_SCREEN_HEIGHT - 100), size=(150, 50), text=f"{self.settings.translate("button_back")}", change_color= [150, 150, 150], func=lambda: self.system.switch_menu_state(MENU_STATE))
        self.character_slot_buttons = [back_button]

        self.delete_buttons = []
        self.add_buttons = []
        for i in range(3):
            btn = Button(position=(0, 0), size=(50, 50), text="+", change_color= [150, 150, 150], func= lambda idx = i: self.show_text_editor(btn.rect.centerx, btn.rect.centery, idx))
            delete_btn = Button(position=(0, 0), size=(25, 25), text= "x", color= [255, 0, 0], func = lambda idx = i: self.delete_character(idx))
            self.add_buttons.append(btn)
            self.delete_buttons.append(delete_btn)

    def create_options_menu_button(self):
        mid_x = self.settings.base_width / 2
        mid_y = self.settings.base_height / 2

        save_button = Button(position= (mid_x, mid_y + 230),size= (200, 50), text= f"{self.settings.translate("button_save_and_close")}", change_color = [150, 150, 150], func= lambda: self.save_and_close(MENU_STATE))
        self.options_button = [save_button]

    def create_options_slider(self):
        mid_x = self.settings.base_width / 2
        mid_y = self.settings.base_height / 2

        MUSIC_SLIDER = VolumeSlider(size=(200, 20), font=get_font(None, 25), label=f"{self.settings.translate("music_volume")}:",
                                initial_value=int(self.settings.music_volume * 100),
                                on_change=self.settings.on_music_volume_change, center_pos= (mid_x, mid_y), text_color= "white", slider_color= "gray", slider_picker_color= "white")
    
        SOUND_SLIDER = VolumeSlider(size=(200, 20), font=get_font(None, 25), label=f"{self.settings.translate("sound_volume")}:",
                                initial_value=int(self.settings.sound_volume * 100),
                                on_change=self.settings.on_sound_volume_change, center_pos= (mid_x, mid_y + 30), text_color= "white", slider_color= "gray", slider_picker_color= "white")
        
        self.options_slider = [MUSIC_SLIDER, SOUND_SLIDER]

    def create_options_toggle(self):
        mid_x = self.settings.base_width / 2
        mid_y = self.settings.base_height / 2


        fullscreen_toggle = Toggle(pos=(mid_x, mid_y - 170), size=(100, 40), font=get_font(None, 25),
                                    label=f"{self.settings.translate("settings_toggle_fullscreen")}:", getter = lambda: self.system.settings.is_fullscreen,
                                    on_toggle=self.system.toggle_fullscreen, text_color= "white")
        
        music_toggle = Toggle(pos=(mid_x, mid_y - 120), size=(100, 40), font=get_font(None, 25),
                                    label=f"{self.settings.translate("settings_music_on")}:", getter = lambda: self.settings.music_on,
                                    on_toggle=self.settings.on_toggle_music, text_color= "white")
        
        sound_toggle = Toggle(pos=(mid_x, mid_y - 70), size=(100, 40), font=get_font(None, 25),
                                    label=f"{self.settings.translate("settings_sounds_on")}:", getter = lambda: self.settings.sounds_on,
                                    on_toggle=self.settings.on_toggle_sound, text_color= "white")

        self.options_toggle = [fullscreen_toggle, music_toggle, sound_toggle]

    def show_text_editor(self, x, y, i):
        self.character_slot = i
        self.character_add_text_box.clear()
        self.character_class_box.index = 0
        self.character_class_box.set_pos(x, y + 100)
        self.character_add_text_box.set_pos(x, y)
        self.show_add_text_editor = True
        self.show_character_class_box = True

    def save_and_close(self, new_state):
        self.system.save_service.save_options(self.settings)
        self.system.switch_menu_state(new_state)

    def apply_resolution(self, res_string):
        if self.system.is_web:
            return
        try:
            width, height = map(int, res_string.split('x'))
            self.game.set_specific_window_size(width, height)
        except ValueError:
            print(f"Ungültiges Format: {res_string}")

    def apply_language(self, new_language):
        self.settings.language = new_language

        self.menu_button_list[0].set_text(self.settings.translate("title_start"))
        self.menu_button_list[1].set_text(self.settings.translate("title_options"))
        self.menu_button_list[2].set_text(self.settings.translate("title_quit"))
        
        self.options_toggle[0].set_label(f"{self.settings.translate('settings_toggle_fullscreen')}:")
        self.options_toggle[1].set_label(f"{self.settings.translate('settings_music_on')}:")
        self.options_toggle[2].set_label(f"{self.settings.translate('settings_sounds_on')}:")

        self.options_slider[0].set_label(f"{self.settings.translate("music_volume")}")
        self.options_slider[1].set_label(f"{self.settings.translate("sound_volume")}")

        self.character_slot_buttons[0].set_text(f"{self.settings.translate("button_back")}")
        self.options_button[0].set_text(f"{self.settings.translate("button_save_and_close")}")
        self.character_add_text_box.label_text = f"{self.settings.translate('character_name')}"

    def delete_character(self, i):
        self.character_list[i] = None
        self.system.save_service.shop_list[i] = []
        self.system.save_service.character_list = self.character_list.copy()
        self.system.save_service.save_data(self.system.save_service.shop_list, self.system.save_service.character_list, self.system.save_service.dungeon_completed)

    def draw_options(self, canvas, mouse_pos):

        for toggle in self.options_toggle:
            toggle.update((toggle.center_x, toggle.center_y))
            toggle.draw(canvas)

        for button in self.options_button:
            button.draw(canvas, mouse_pos)

        for slider in self.options_slider:
            slider.draw(canvas)

        current_w, current_h = self.system.screen.get_size()
        res_string = f"{current_w}x{current_h}"

        if res_string in self.resolution_drop_down.item_list:
            self.resolution_drop_down.display_item = res_string
        else:
            self.resolution_drop_down.display_item = "Display"
        self.language_drop_down.draw(canvas, mouse_pos)
        self.resolution_drop_down.draw(canvas, mouse_pos)

    def draw_character_slots(self, canvas, mouse_pos):
        width = 300
        height = 600
        spacing = 20
        
        num_chars = len(self.character_list)
        total_width = (num_chars * width) + ((num_chars - 1) * spacing)
        start_x = (INITIAL_SCREEN_WIDTH - total_width) / 2
        center_y = (INITIAL_SCREEN_HEIGHT - height) / 2

        self.character_slot_list = []

        for i, character in enumerate(self.character_list):
            current_x = start_x + i * (width + spacing)
            
            slot = create_rectangle(canvas, current_x, center_y, width, height, 4, "gray")
            self.character_slot_list.append(slot)

            slot_center_x = slot.x + slot.width / 2
            slot_center_y = slot.y + slot.height / 2

            if character:
                show_text(canvas, f"{self.settings.translate("slot")} {i + 1}", slot_center_x, slot.y + 20, "white", True)
                show_text(canvas, f"{character.name}", slot_center_x, slot.y + 70, "white", True)
                show_text(canvas, f"Level: {character.level}", slot_center_x, slot.y + 120, "green", True)
                delete_btn = self.delete_buttons[i]
                delete_btn.set_pos((slot.x + slot.width, slot.y))
                delete_btn.draw(canvas, mouse_pos)
            else:
                show_text(canvas, f"{self.settings.translate("slot")} {i + 1}", slot_center_x, slot.y + 20, "white", True)

                if self.show_add_text_editor and self.show_character_class_box and self.character_slot == i:
                    self.character_add_text_box.set_pos(slot_center_x, slot_center_y)
                    self.character_add_text_box.draw(canvas)
                    self.character_class_box.set_pos(slot_center_x, slot_center_y + 100)
                    self.character_class_box.draw(canvas, mouse_pos, self.settings)
                    if len(self.character_add_text_box.text) > 0:
                        show_text(canvas, self.settings.translate("press_enter"), self.character_add_text_box.rect.centerx, self.character_add_text_box.rect.centery + 40, "white", True)
                else:
                    add_btn = self.add_buttons[i]
                    add_btn.set_pos((slot_center_x, slot_center_y))
                    add_btn.draw(canvas, mouse_pos)

        self.character_slot_buttons[0].draw(canvas, mouse_pos)

    def create_character_and_change_state(self, character_slot=None):
        if character_slot is None:
            chosen_name = self.character_add_text_box.text
            chosen_class_type = self.character_class_box.selected_item
            if len(chosen_name) > 0:
                new_char = Character(chosen_name, None, 1, 1, chosen_class_type)
                idx = self.character_slot
                
                self.character_list[idx] = new_char
                self.system.save_service.character_list[idx] = new_char
                self.system.save_service.shop_list[idx] = [] 
        else:
            # Bestehender Charakter ausgewählt
            self.character_slot = character_slot
            
        self.system.switch_menu_state(GAME_STATE)

    def handle_character_slot_events(self, event, mouse_pos):
        if not self.character_slot_list:
            return

        self.cursor_focused = False

        self.character_slot_buttons[0].handle_event(event, mouse_pos)
            
        if self.show_add_text_editor:
            self.character_add_text_box.handle_event(event, mouse_pos)
            self.character_class_box.handle_event(event, mouse_pos)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if len(self.character_add_text_box.text) > 0:
                    self.create_character_and_change_state(None)
                    self.show_add_text_editor = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_add_text_editor = False
        
        for i, character in enumerate(self.character_list):
            if not character:
                self.add_buttons[i].handle_event(event, mouse_pos)
            else:
                self.delete_buttons[i].handle_event(event, mouse_pos)
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

        if not self.language_drop_down.focused and not self.resolution_drop_down.focused:
            for button in self.options_button:
                button.handle_event(event, mouse_pos)

        self.resolution_drop_down.handle_event(event, mouse_pos)
        self.language_drop_down.handle_event(event, mouse_pos)

    def draw(self, canvas, mouse_pos):
        for button in self.menu_button_list:
            button.draw(canvas, mouse_pos)

    def handle_events(self, event, mouse_pos):
        for button in self.menu_button_list:
            button.handle_event(event, mouse_pos)
