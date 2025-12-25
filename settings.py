
INITIAL_SCREEN_WIDTH = 1920
INITIAL_SCREEN_HEIGHT = 1080
FPS = 60
MAIN_START = 195
MAIN_END = 1725
DEFAULT_MAIN_WINDOW_STATE = "Default_Main_Window_State"
QUEST_MAIN_WINDOW_STATE = "Quest_Main_Window_State"
DUNGEON_MAIN_WINDOW_STATE = "Dungeon_Main_Window_State"

EXPERIENCE_QUEST_TYPE = "experience_quest_type"
GOLD_QUEST_TYPE = "gold_quest_type"
ITEM_QUEST_TYPE = "item_quest_type"
DANGEROUS_QUEST_TYPE = "dangerous_quest_type"

# Const for Language selector
ENGLISH = "english"
GERMAN = "german"
LANGUAGE = ENGLISH

translations = {
    ENGLISH: {
    },
    GERMAN: {
    }
}

def translate(key):
    return translations.get(LANGUAGE, {}).get(key, f"[{key}]")

class Settings:
    def __init__(self):
        self.base_width = INITIAL_SCREEN_WIDTH
        self.base_height = INITIAL_SCREEN_HEIGHT
        self.fps = FPS
        self.title = "RPG Adventure"