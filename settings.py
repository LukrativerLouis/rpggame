import pygame

INITIAL_SCREEN_WIDTH = 1920
INITIAL_SCREEN_HEIGHT = 1080
FPS = 144
MAIN_START = 195
MAIN_END = 1725
ITEM_SIZE = 180
ITEM_HOLDER_SIZE = 200
GAME_VERSION = "0.1.0.dev"

MENU_STATE = "menu_state"
OPTIONS_STATE = "options_state"
CHARACTER_SLOTS_STATE = "character_slots_state"
CHARACTER_ADD_STATE = "character_add_state"
GAME_STATE = "game_state"

DEFAULT_MAIN_WINDOW_STATE = "Default_Main_Window_State"
QUEST_MAIN_WINDOW_STATE = "Quest_Main_Window_State"
DUNGEON_MAIN_WINDOW_STATE = "Dungeon_Main_Window_State"
CHARACTER_MAIN_WINDOW_STATE = "Character_Main_Window_State"
SHOP_MAIN_WINDOW_STATE = "Shop_Main_Window_State"

SELL_FACTOR = 0.3

CHARACTER_BASE_XP = 100
XP_MULTIPLIER = 1.5

CHARACTER = "character"
ENEMY = "enemy"

EXPERIENCE_QUEST_TYPE = "experience_quest_type"
GOLD_QUEST_TYPE = "gold_quest_type"
ITEM_QUEST_TYPE = "item_quest_type"
DANGEROUS_QUEST_TYPE = "dangerous_quest_type"

# file paths

SAVE_FILE_PATH = "data/data.json"

# class types

WARRIOR = "warrior"
MAGE = "mage"
ARCHER = "archer"

CLASS_TYPE_LIST = [WARRIOR, MAGE, ARCHER]
DISPLAY_RESOLUTION_LIST = ["2560x1440", "1920x1080", "1280x720"]

# Const for Language selector
ENGLISH = "English"
GERMAN = "German"

LANGUAGE_LIST  = [ENGLISH, GERMAN]

translations = {
    ENGLISH: {
    },
    GERMAN: {
    }
}

class Settings:
    def __init__(self):
        self.base_width = INITIAL_SCREEN_WIDTH
        self.base_height = INITIAL_SCREEN_HEIGHT
        # this is to use for specific resolution
        self.forced_width = None
        self.forced_height = None
        self.fullscreen_display_resolution = (0,0)
        self.language = ENGLISH
        self.fps = FPS
        self.title = "RPG Adventure"

        self.sounds = {
            #"Test": pygame.mixer.Sound("TestPath")
        }
        self.current_music_path = None
        self.music_volume = 0.05
        self.sound_volume = 0.1
        self.music_on = True
        self.sounds_on = False
        self.debug = False

    def translate(self, key):
        return translations.get(self.language, {}).get(key, f"[{key}]")

    def on_toggle_sound(self, state):
        self.sounds_on = state

    def on_toggle_music(self, state):
        self.music_on = state
        #if self.settings.music_on:
        #    self.settings.play_music(MENU_MUSIC_PATH)
        #else:
        #    pygame.mixer.music.stop()

    def on_music_volume_change(self, value):
        self.music_volume = value / 100
        if self.music_on:
            pygame.mixer.music.set_volume(self.music_volume)

    def on_sound_volume_change(self, value):
        self.sound_volume = value / 100
    
    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def play_sound(self, name):
        if self.sounds_on:
            sound = self.sounds.get(name)
            if sound:
                sound.set_volume(self.sound_volume)
                sound.play()

    def play_music(self, file_path):
        if self.music_on:
            if self.current_music_path != file_path or not pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1, 0.0, 5000)
                self.current_music_path = file_path
        else:
            pygame.mixer.music.stop()