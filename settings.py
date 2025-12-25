
INITIAL_SCREEN_WIDTH = 1920
INITIAL_SCREEN_HEIGHT = 1080
FPS = 60
MAIN_START = 195
MAIN_END = 1725
DEFAULT_QUEST_STATE = "Default_Quest_State"
SHOW_QUEST_STATE = "Show_Quest_State"

class Settings:
    def __init__(self):
        self.base_width = INITIAL_SCREEN_WIDTH
        self.base_height = INITIAL_SCREEN_HEIGHT
        self.fps = FPS
        self.title = "RPG Adventure"