from settings import *
from character import *
from fight_window import *
from quest import *
from utils import *

class Quest_Window:
    def __init__(self, character: Character, level):
        self.show_dialog_window = False
        self.quest_list = [Quest(EXPERIENCE_QUEST_TYPE), Quest(GOLD_QUEST_TYPE), Quest(DANGEROUS_QUEST_TYPE)]
        self.selected_quest: Quest = None
        self.selected_quest_index = -1
        self.quest_button_list = self.__create_quest_window_buttons()
        self.dialog_button_list = self.__create_dialog_window_buttons()
        self.traveling_screen_button_list = self.__create_traveling_screen_buttons()
        self.countdown_bar_length = 1525
        self.countdown_bar_length_current = self.countdown_bar_length
        self.countdown_bar_progress = 50
        self.countdown_bar_total_time = 0
        self.countdown_bar_remaining_time = 0
        self.countdown_bar_start_time = pygame.time.get_ticks()
        self.quest_started = False
        self.fight_started = False
        self.character = character
        self.fight_window = None
        self.level = level

    def __toggle_dialog_window(self, show_quest_index = -1):
        current_selected_quest = self.quest_list[show_quest_index]

        if self.selected_quest != current_selected_quest:
            self.show_dialog_window = True
            self.selected_quest = current_selected_quest
            self.selected_quest_index = show_quest_index
        else:
            self.show_dialog_window = False
            self.selected_quest = None
            self.selected_quest_index = -1
    
    def __close_dialog_window(self, simple_close = True):
        self.show_dialog_window = False
        if not simple_close:
            self.selected_quest = None
            self.selected_quest_index = -1

    def __create_quest_window_buttons(self):
        button_quest_first = Button(position = (400, 150), size = (150, 50), text = "Quest 1", change_color = [150, 150, 150], func = lambda: self.__toggle_dialog_window(0))
        button_quest_second = Button(position=(700, 150), size=(150, 50), text="Quest 2", color=[100, 50, 50], change_color=[150, 50, 50], func= lambda: self.__toggle_dialog_window(1))
        button_quest_third = Button(position=(550, 250), size=(150, 50), text="Quest 3", color=[100, 50, 50], change_color=[150, 50, 50], func= lambda: self.__toggle_dialog_window(2))

        return [button_quest_first, button_quest_second, button_quest_third]

    def __create_dialog_window_buttons(self):
        button_close = Button(position = (1870, 50), size = (50, 50), text = "x", color = [255, 0, 0],change_color = [255, 50, 50], func = lambda: self.__close_dialog_window(False))
        button_start_quest = Button(position = (1400, INITIAL_SCREEN_HEIGHT - 100), size = (150, 50), text = "Start Quest", color = [0, 255, 0],change_color = [50, 255, 50], func = lambda: self.__start_quest())

        return [button_close, button_start_quest]
    
    def __create_traveling_screen_buttons(self):
        button_cancel_quest = Button(position = (975, 1025), size = (150, 50), text = "cancel quest", color = [255, 0, 0], change_color = [255, 50, 50])
        button_skip_quest = Button(position = (1150, 1025), size = (150, 50), text = "skip quest", color = [255, 0, 0], change_color = [255, 50, 50])

        return [button_cancel_quest, button_skip_quest]
    
    def __start_quest(self):

        self.quest_started = True
        self.countdown_bar_total_time = self.selected_quest.duration
        self.countdown_bar_start_time = pygame.time.get_ticks()
        self.__close_dialog_window(True)

    def __quest_completed(self):
        self.character.adjust_gold_and_exp(self.selected_quest.gold, self.selected_quest.experience)

        if self.selected_quest_index == 0:
            self.quest_list[0] = Quest(EXPERIENCE_QUEST_TYPE)
        elif self.selected_quest_index == 1:
            self.quest_list[1] = Quest(GOLD_QUEST_TYPE)
        elif self.selected_quest_index == 2:
            self.quest_list[2] = Quest(DANGEROUS_QUEST_TYPE)

        self.show_dialog_window = False
        self.quest_started = False
        self.level.main_window_state = DEFAULT_MAIN_WINDOW_STATE
        self.selected_quest = None
        self.fight_started = False
        self.fight_window = None

    def __start_fight(self):

        self.fight_started = True
        if self.fight_window is None:
            self.character.current_health = self.character.max_health
            self.character.attack_score = 0
            self.fight_window = Fight_Window(self, self.character, lambda: self.__quest_completed(), False)

    def __draw_quest_window(self, canvas):
        # window
        create_rectangle(canvas, 900, 0, INITIAL_SCREEN_WIDTH - 900, INITIAL_SCREEN_HEIGHT, 5, "purple")
        create_rectangle(canvas, 905, 5, INITIAL_SCREEN_WIDTH - 910, INITIAL_SCREEN_HEIGHT - 10, 0, "azure4")

        # text
        show_text(canvas, self.selected_quest.title, 1000, 100, "darkgoldenrod1")
        show_text(canvas, self.selected_quest.description, 1000, 200, "darkgoldenrod1")
        show_text(canvas, f"Experience: {self.selected_quest.experience}", 1000, 400, "green")
        show_text(canvas, f"Gold: {self.selected_quest.gold}", 1000, 450, "yellow")

    def __draw_quest_traveling_screen(self, canvas):
        countdown_bar_x = 300
        countdown_bar_y = 930
        countdown_bar_height = 50
        countdown_bar_border = 2

        self.__animate_countdown_bar()

        # quest background
        create_rectangle(canvas, 200, 5, 1715, 1070, 0, "brown")

        # quest_title

        show_text(canvas, f"{self.selected_quest.title}", 200 + 1715 / 2, 35, "darkgoldenrod", True)

        # loading bar border

        create_rectangle(canvas, countdown_bar_x, countdown_bar_y, self.countdown_bar_length, countdown_bar_height, countdown_bar_border, "black")

        # loading bar progress

        create_rectangle(canvas, countdown_bar_x + countdown_bar_border, countdown_bar_y + countdown_bar_border, self.countdown_bar_length_current - countdown_bar_border * 2, self.countdown_bar_progress - countdown_bar_border * 2, 0, "cyan4")

        show_text(canvas, f"{self.countdown_bar_remaining_time:.1f}s", countdown_bar_x + self.countdown_bar_length / 2, countdown_bar_y + countdown_bar_height / 2, "darkgoldenrod", True)

    def __animate_countdown_bar(self):

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.countdown_bar_start_time) / 1000

        # time as text
        self.countdown_bar_remaining_time = max(self.countdown_bar_total_time - elapsed_time, 0)

        # time as progress bar
        self.countdown_bar_length_current = (self.countdown_bar_remaining_time / self.countdown_bar_total_time) * self.countdown_bar_length

        if elapsed_time >= self.selected_quest.duration:
            self.__start_fight()

    def draw(self, canvas, mouse_pos):
        # temp quest board
        create_rectangle(canvas, 300, 100, 500, 400, 0, "gray")

        for button in self.quest_button_list:
            button.draw(canvas, mouse_pos)

        if self.show_dialog_window and self.selected_quest is not None:
            self.__draw_quest_window(canvas)

            for button in self.dialog_button_list:
                button.draw(canvas, mouse_pos)

        if self.quest_started:
            self.__draw_quest_traveling_screen(canvas)

            for button in self.traveling_screen_button_list:
                button.draw(canvas, mouse_pos)
            
            if self.fight_started:
                self.fight_window.draw(canvas, mouse_pos)
    
    def handle_events(self, event,  mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.quest_button_list:
                    button.click(mouse_pos)
                if self.show_dialog_window and self.selected_quest is not None:
                    for button in self.dialog_button_list:
                        button.click(mouse_pos)
                if self.quest_started:
                    for button in self.traveling_screen_button_list:
                        button.click(mouse_pos)

        if self.fight_started and self.quest_started:
            self.fight_window.handle_events(event, mouse_pos)

