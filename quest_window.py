from settings import *
from utils import *

class Quest_Window:
    def __init__(self, character):
        self.show_quest_window = False
        self.quest_button_list = self.create_buttons()
        self.character = character

    def toggle_quest_window(self):
        self.show_quest_window = not self.show_quest_window

    def draw(self, canvas, mouse_pos):
        # temp quest board
        create_rectangle(canvas, 300, 100, 500, 400, 0, "gray")

        for button in self.quest_button_list:
            button.draw(canvas, mouse_pos)
    
    def create_buttons(self):
        button_quest_exp = Button(position = (400, 150), size = (150, 50), text = "More Exp (Quest 1)", change_color = [150, 150, 150], func = lambda: self.character.adjust_gold_and_exp(1, 5))
        button_quest_gold = Button(position=(700, 150), size=(150, 50), text="More Gold (Quest 2)", color=[100, 50, 50], change_color=[150, 50, 50], func= lambda: self.character.adjust_gold_and_exp(5, 1))

        return [button_quest_exp, button_quest_gold]
    
    def handle_events(self, event,  mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.quest_button_list:
                    button.click(mouse_pos)
