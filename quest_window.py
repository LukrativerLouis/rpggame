from settings import *
from character import *
from quest import *
from utils import *

class Quest_Window:
    def __init__(self, character: Character):
        self.show_dialog_window = False
        self.quest_list = [Quest(EXPERIENCE_QUEST_TYPE), Quest(GOLD_QUEST_TYPE), Quest(DANGEROUS_QUEST_TYPE)]
        self.current_quest_shown: Quest = None
        self.quest_button_list = self.create_quest_window_buttons()
        self.dialog_button_list = self.create_dialog_window_buttons()
        self.character = character

    def toggle_dialog_window(self, show_quest = None):
        if self.current_quest_shown != show_quest:
            self.show_dialog_window = True
            self.current_quest_shown = show_quest
        else:
            self.show_dialog_window = False
            self.current_quest_shown = None

    def create_quest_window_buttons(self):
        button_quest_first = Button(position = (400, 150), size = (150, 50), text = "Quest 1", change_color = [150, 150, 150], func = lambda: self.toggle_dialog_window(self.quest_list[0]))
        button_quest_second = Button(position=(700, 150), size=(150, 50), text="Quest 2", color=[100, 50, 50], change_color=[150, 50, 50], func= lambda: self.toggle_dialog_window(self.quest_list[1]))
        button_quest_third = Button(position=(550, 250), size=(150, 50), text="Quest 3", color=[100, 50, 50], change_color=[150, 50, 50], func= lambda: self.toggle_dialog_window(self.quest_list[2]))

        return [button_quest_first, button_quest_second, button_quest_third]

    def create_dialog_window_buttons(self):
        button_close = Button(position = (INITIAL_SCREEN_WIDTH - 200, 50), size = (50, 50), text = "x", color = [255, 0, 0],change_color = [255, 50, 50], func = lambda: self.toggle_dialog_window())
        button_start_quest = Button(position = (1400, INITIAL_SCREEN_HEIGHT - 100), size = (150, 50), text = "Start Quest", color = [0, 255, 0],change_color = [50, 255, 50], func = lambda: self.start_quest())

        return [button_close, button_start_quest]
    
    def start_quest(self):
        print(f"current Quest: {self.current_quest_shown.title}")
        self.character.adjust_gold_and_exp(self.current_quest_shown.gold, self.current_quest_shown.experience)

    def draw_quest_window(self, canvas):
        # window
        create_rectangle(canvas, 900, 0, INITIAL_SCREEN_WIDTH - 900, INITIAL_SCREEN_HEIGHT, 5, "purple")
        create_rectangle(canvas, 905, 5, INITIAL_SCREEN_WIDTH - 910, INITIAL_SCREEN_HEIGHT - 10, 0, "gray")

    def draw_quest_info(self, canvas):
        show_text(canvas, self.current_quest_shown.title, 100, 1000, "gold")
        show_text(canvas, self.current_quest_shown.description, 200, 1000, "gold")
        show_text(canvas, f"Experience: {self.current_quest_shown.experience}", 400, 1000, "green")
        show_text(canvas, f"Gold: {self.current_quest_shown.gold}", 450, 1000, "yellow")

    def draw(self, canvas, mouse_pos):
        # temp quest board
        create_rectangle(canvas, 300, 100, 500, 400, 0, "gray")

        for button in self.quest_button_list:
            button.draw(canvas, mouse_pos)

        if self.show_dialog_window and self.current_quest_shown != None:
            self.draw_quest_window(canvas)
            self.draw_quest_info(canvas)

            for button in self.dialog_button_list:
                button.draw(canvas, mouse_pos)
    
    def handle_events(self, event,  mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.quest_button_list:
                    button.click(mouse_pos)
                if self.show_dialog_window and self.current_quest_shown != None:
                    for button in self.dialog_button_list:
                        button.click(mouse_pos)
