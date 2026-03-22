from settings import *
from utils import *
from character import *
from dungeon_monster import *

spacer_padding = 5
main_side_padding = 20
base_dungeon_window_size = 400
specific_offset = 20

class Dungeon_Window:
    def __init__(self, character: Character):
        self.character = character

        self.dungeon_start_buttons = None
        self.specific_dungeon_buttons = None
        self.__setup_buttons()

        # 1 is first monster
        self.beaten_dungeon_monster = {
            DUNGEON_1 : 1,
            DUNGEON_2 : 1,
            DUNGEON_3 : 1
        }
        self.dungeon_monster = 0
        # specific dungeon window
        self.current_dungeon_selected = DUNGEON_1
        self.current_dungeon_focused = False
        self.current_dungeon_monster: Dungeon_Monster = dungeon_monster_list[self.current_dungeon_selected][self.beaten_dungeon_monster[self.current_dungeon_selected] - 1]

    def __setup_buttons(self):
        self.button_d1 = Button(position=(0,0), size=(50, 50), text="", color=[0, 255, 0], func=lambda: self.__toggle_dungeon_seleced(DUNGEON_1))
        self.button_d2 = Button(position=(0,0), size=(50, 50), text="", color=[0, 0, 255], func=lambda: self.__toggle_dungeon_seleced(DUNGEON_2))
        self.button_d3 = Button(position=(0,0), size=(50, 50), text="", color=[255, 0, 0], func=lambda: self.__toggle_dungeon_seleced(DUNGEON_3))
        
        self.dungeon_start_buttons = [self.button_d1, self.button_d2, self.button_d3]
        
        self.btn_start_fight = Button(position=(0,0), size=(100, 50), text="start fight")
        self.btn_close_spec = Button(position=(0,0), size=(100, 50), text="close", func=lambda: self.__toggle_dungeon_seleced(DUNGEON_1))
        self.specific_dungeon_buttons = [self.btn_start_fight, self.btn_close_spec]

    def __toggle_dungeon_seleced(self, new_selected_dungeon):
        self.current_dungeon_selected = new_selected_dungeon
        self.current_dungeon_monster: Dungeon_Monster = dungeon_monster_list[self.current_dungeon_selected][self.beaten_dungeon_monster[self.current_dungeon_selected] - 1]
        self.current_dungeon_focused = not self.current_dungeon_focused
    
    def __draw_first_dungeon_window(self, canvas, mouse_pos):

        max_dungeon_monster = 5

        # first dungeon window

        first_dungeon_window = create_rectangle(canvas, MAIN_START + main_side_padding, main_side_padding, base_dungeon_window_size, 800, 4, "green")

        show_text(canvas, DUNGEON_1, first_dungeon_window.x + first_dungeon_window.width / 2, first_dungeon_window.y + main_side_padding, "white", True)

        pos_1 = (first_dungeon_window.x + first_dungeon_window.width / 2, first_dungeon_window.y + first_dungeon_window.height - 50)
        self.button_d1.rect.center = pos_1
        self.button_d1.center_pos = pos_1
        self.button_d1.set_text(f"{self.beaten_dungeon_monster[DUNGEON_1]}/{max_dungeon_monster}")

        # second dungeon window 

        second_dungeon_window = create_rectangle(canvas, MAIN_START + main_side_padding + base_dungeon_window_size + spacer_padding, main_side_padding, base_dungeon_window_size, 800, 4, "blue")

        show_text(canvas, DUNGEON_2, second_dungeon_window.x + second_dungeon_window.width / 2, second_dungeon_window.y + main_side_padding, "white", True)

        pos_2 = (second_dungeon_window.x + second_dungeon_window.width / 2, second_dungeon_window.y + second_dungeon_window.height - 50)
        self.button_d2.rect.center = pos_2
        self.button_d2.center_pos = pos_2
        self.button_d2.set_text(f"{self.beaten_dungeon_monster[DUNGEON_2]}/{max_dungeon_monster}")

        # third dungeon window

        third_dungeon_window = create_rectangle(canvas, MAIN_START + main_side_padding + (base_dungeon_window_size + spacer_padding) * 2, main_side_padding, base_dungeon_window_size, 800, 4, "red")

        show_text(canvas, DUNGEON_3, third_dungeon_window.x + third_dungeon_window.width / 2, third_dungeon_window.y + main_side_padding, "white", True)

        pos_3 = (third_dungeon_window.x + third_dungeon_window.width / 2, third_dungeon_window.y + third_dungeon_window.height - 50)
        self.button_d3.rect.center = pos_3
        self.button_d3.center_pos = pos_3
        self.button_d3.set_text(f"{self.beaten_dungeon_monster[DUNGEON_3]}/{max_dungeon_monster}")

    def __draw_specific_dungeon_window(self, canvas, mouse_pos):
        specific_window = create_rectangle(canvas, MAIN_START + MAIN_END / 2 - 400, main_side_padding + specific_offset, 800, 800, 0, "gray")
        create_rectangle(canvas, specific_window.x, specific_window.y, specific_window.width, specific_window.height, 5, "orange")

        # display dungeon monster picture

        monster_picture = create_rectangle(canvas, specific_window.x + specific_offset, specific_window.y + specific_offset, specific_window.width / 2, specific_window.height / 2, 0, "black")

        # display title

        show_text(canvas, self.current_dungeon_monster.name, monster_picture.x + monster_picture.width + specific_offset, monster_picture.y, "gold")

        # display description

        show_text(canvas, self.current_dungeon_monster.description, monster_picture.x + monster_picture.width + specific_offset, monster_picture.y + 200, "gold")

        # display start button

        pos_1 = (specific_window.x + specific_window.width / 2 - 130, specific_window.y + specific_window.height - 50)
        self.btn_start_fight.rect.center = pos_1
        self.btn_start_fight.center_pos = pos_1

        # display exit button

        pos_2 = (specific_window.x + specific_window.width / 2, specific_window.y + specific_window.height - 50)
        self.btn_close_spec.rect.center = pos_2
        self.btn_close_spec.center_pos = pos_2

    def draw(self, canvas, mouse_pos):
        self.__draw_first_dungeon_window(canvas, mouse_pos)

        for button in self.dungeon_start_buttons:
            button.draw(canvas, mouse_pos)

        if self.current_dungeon_focused:
            self.__draw_specific_dungeon_window(canvas, mouse_pos)

            for button in self.specific_dungeon_buttons:
                button.draw(canvas, mouse_pos)


    def handle_events(self, event, mouse_pos):
        if self.dungeon_start_buttons is not None:
            if not self.current_dungeon_focused:
                for button in self.dungeon_start_buttons:
                    button.handle_event(event, mouse_pos)
            if self.current_dungeon_focused and self.specific_dungeon_buttons is not None:
                for button in self.specific_dungeon_buttons:
                    button.handle_event(event, mouse_pos)
