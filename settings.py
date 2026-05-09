import pygame

INITIAL_SCREEN_WIDTH = 1920
INITIAL_SCREEN_HEIGHT = 1080
FPS = 144
MAIN_START = 195
MAIN_END = 1725
ITEM_SIZE = 180
ITEM_HOLDER_SIZE = 200
GAME_VERSION = "0.1.0.dev"
WEB_PLATFORM = "emscripten"

MENU_STATE = "menu_state"
OPTIONS_STATE = "options_state"
CHARACTER_SLOTS_STATE = "character_slots_state"
GAME_STATE = "game_state"
INTRO_STATE = "intro_state"

DEFAULT_MAIN_WINDOW_STATE = "Default_Main_Window_State"
QUEST_MAIN_WINDOW_STATE = "Quest_Main_Window_State"
DUNGEON_MAIN_WINDOW_STATE = "Dungeon_Main_Window_State"
CHARACTER_MAIN_WINDOW_STATE = "Character_Main_Window_State"
SHOP_MAIN_WINDOW_STATE = "Shop_Main_Window_State"

# Events

LEVEL_UP_EVENT = "level_up_event"

AUTO_SAVE_TIME = 5
SELL_FACTOR = 0.3
CHARACTER_BASE_XP = 100
XP_MULTIPLIER = 1.5
CHARACTER_STAT_BASE_PRICE = 1
BASE_HP = 100
HEALTH_SCALING_WARRIOR = 15
HEALTH_SCALING_ARCHER = 12
HEALTH_SCALING_MAGE = 10
CRIT_CHANCE_SCALING = 0.5
CRIT_MULITPLIER_BASE = 1.5
CRIT_MULITPLIER_SCALING = 0.005

STAMINA_COST = 25

ARMOR_K_BASE = 100
ARMOR_LEVEL_SCALING = 10

CHARACTER = "character"
ENEMY = "enemy"

EXPERIENCE_QUEST_TYPE = "experience_quest_type"
GOLD_QUEST_TYPE = "gold_quest_type"
ITEM_QUEST_TYPE = "item_quest_type"
DANGEROUS_QUEST_TYPE = "dangerous_quest_type"

# file paths

SAVE_FILE_PATH_OPTIONS = "data/options.json"
SAVE_FILE_PATH_DATA = "data/data.json"
PIXELIFY_FONT_PATH = "font/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf"

# keys

TITLE_KEY = "title_key"
DESCRIPTION_KEY = "description_key"

# dungeons

DUNGEON_1 = "Dungeon 1"
DUNGEON_2 = "Dungeon 2"
DUNGEON_3 = "Dungeon 3"

# class types

WARRIOR = "Warrior"
MAGE = "Mage"
ARCHER = "Archer"

CLASS_TYPE_LIST = [WARRIOR, ARCHER, MAGE]
DISPLAY_RESOLUTION_LIST = ["2560x1440", "1920x1080", "1280x720"]

# Const for Language selector
ENGLISH = "English"
GERMAN = "German"

LANGUAGE_LIST  = [ENGLISH, GERMAN]

translations = {
    ENGLISH: {
        "title_start": "Start game",
        "title_options": "Options",
        "title_quit": "Quit",
        "settings_toggle_fullscreen": "Toggle Fullscreen",
        "settings_music_on": "Music",
        "settings_sounds_on": "Sounds",
        "music_volume": "Music volume",
        "sound_volume": "Sound volume",
        "button_back": "Back",
        "button_save_and_close": "Save and close",
        "character_name": "Enter character name",
        "press_enter": "Press enter to continue",
        "Warrior": "Warrior",
        "Mage": "Mage",
        "Archer": "Archer",
        "button_questboard": "Questboard",
        "button_character": "Character",
        "button_shop": "Shop",
        "button_dungeon": "Dungeon",
        "button_quit": "Quit",
        "stat_health": "Health",
        "stat_damage": "Damage",
        "stat_strength": "Strength",
        "stat_dexterity": "Dexterity",
        "stat_endurance": "Endurance",
        "stat_precision": "Precision",
        "button_reroll_items": "Reroll items",
        "slot": "Slot",
        "button_cancel_quest": "Cancel quest",
        "button_skip_quest_time": "Skip quest time",
        "button_start_quest": "Start quest",
        "stamina_bar": "Stamina",
        "experience": "Experience",
        "gold": "Gold",
        "stamina_cost": "Stamina-Cost",
        "button_start_fight": "Start fight",
        "button_close": "Close",
        "button_skip_fight": "Skip fight",
        "button_faster": "Faster",
        "button_continue": "Continue",
        "message_won": "You won!",
        "message_lost": "You lost!",
        "playtime_total": "Total playtime",
        "playtime_current": "Current session",
        "button_stats": "Statistics",
        "settings_auto_save": "Auto save (5m)",

        # Quest
        "quest_exam_title": "Apprenticeship Exam",
        "quest_exam_description": "Pass the exam to become a mage.",
        "quest_lorem_ipsum_title": "lorem ipsum",
        "quest_lorem_ipsum_description": "SISPSISPSISPS",
        "quest_test_title": "Test",
        "quest_test_description": "test",
        "quest_monsterhunt_title": "Monster Hunt",
        "quest_monsterhunt_description": "Defeat 10 wolves to gain experience.",
        "quest_treasurehunt_title": "Treasure Hunt",
        "quest_treasurehunt_description": "Find the hidden chest in the forest.",
        "quest_errands_title": "Run Errands",
        "quest_errands_description": "Deliver a message and get a reward.",
        "quest_sword_title": "The Lost Sword",
        "quest_sword_description": "Find the legendary sword and bring it back.",
        "quest_herb_title": "Herb collector",
        "quest_herb_description": "Collect 5 medicinal herbs for the alchemist.",
        "quest_dragon_title": "Dragon Slayer",
        "quest_dragon_description": "Defeat the dragon that is threatening the village.",
        "quest_depths_title": "Dangerous Depths",
        "quest_depths_description": "Explore the cursed cave and make it back alive.",
        "quest_ipsum_lorem_title": "ipsum lorem",
        "quest_ipsum_lorem_description": "GRRR Grrrr",

        # Dungeon
        "dungeon_monster_1_title": "Monster 1",
        "dungeon_monster_1_description": "Not that scary only number 1",
        "dungeon_monster_2_title": "Monster 2",
        "dungeon_monster_2_description": "Not that scary only number 2",
        "dungeon_monster_3_title": "Monster 3",
        "dungeon_monster_3_description": "Not that scary only number 3",
        "dungeon_monster_4_title": "Monster 4",
        "dungeon_monster_4_description": "Not that scary only number 4",
        "dungeon_monster_5_title": "Monster 5",
        "dungeon_monster_5_description": "Not that scary only number 5",
        "dungeon_enemy_1_title": "Enemy 1",
        "dungeon_enemy_1_description": "Not that scary only number 1",
        "dungeon_enemy_2_title": "Enemy 2",
        "dungeon_enemy_2_description": "Not that scary only number 2",
        "dungeon_enemy_3_title": "Enemy 3",
        "dungeon_enemy_3_description": "Not that scary only number 3",
        "dungeon_enemy_4_title": "Enemy 4",
        "dungeon_enemy_4_description": "Not that scary only number 4",
        "dungeon_enemy_5_title": "Enemy 5",
        "dungeon_enemy_5_description": "Not that scary only number 5",
        "dungeon_boss_1_title": "Boss 1",
        "dungeon_boss_1_description": "Not that scary only number 1",
        "dungeon_boss_2_title": "Boss 2",
        "dungeon_boss_2_description": "Not that scary only number 1",
        "dungeon_boss_3_title": "Boss 3",
        "dungeon_boss_3_description": "Not that scary only number 1",
        "dungeon_boss_4_title": "Boss 4",
        "dungeon_boss_4_description": "Not that scary only number 1",
        "dungeon_boss_5_title": "Boss 5",
        "dungeon_boss_5_description": "Not that scary only number 1"
    },
    GERMAN: {
        "title_start": "Spiel starten",
        "title_options": "Optionen",
        "title_quit": "Verlassen",
        "settings_toggle_fullscreen": "Vollbild an/aus",
        "settings_music_on": "Musik",
        "settings_sounds_on": "Geräusche",
        "music_volume": "Musik Lautstärke",
        "sound_volume": "Geräusche Lautstärke",
        "button_back": "Zurück",
        "button_save_and_close": "Speichern und schließen",
        "character_name": "Charakternamen eingeben",
        "press_enter": "Drück Eingabe um fortzufahren",
        "Warrior": "Krieger",
        "Mage": "Magier",
        "Archer": "Bogenschütze",
        "button_questboard": "Questbrett",
        "button_character": "Charakter",
        "button_shop": "Laden",
        "button_dungeon": "Dungeon",
        "button_quit": "Verlassen",
        "stat_health": "Leben",
        "stat_damage": "Schaden",
        "stat_strength": "Stärke",
        "stat_dexterity": "Geschick",
        "stat_endurance": "Ausdauer",
        "stat_precision": "Präzision",
        "button_reroll_items": "Laden erneuern",
        "slot": "Speicherplatz",
        "button_cancel_quest": "Quest abbrechen",
        "button_skip_quest_time": "Zeit überspringen",
        "button_start_quest": "Quest starten",
        "stamina_bar": "Kondition",
        "experience": "Erfahrung",
        "gold": "Gold",
        "stamina_cost": "Kondition Kosten",
        "button_start_fight": "Kampf starten",
        "button_close": "Schließen",
        "button_skip_fight": "Kampf überspringen",
        "button_faster": "Schneller",
        "button_continue": "Weiter",
        "message_won": "Du hast Gewonnen!",
        "message_lost": "Du hast Verloren!",
        "playtime_total": "Gesamte Spielzeit",
        "playtime_current": "Aktuelle Sitzung",
        "button_stats": "Statistiken",
        "settings_auto_save": "Automatisch speichern (5m)",

        # Quest
        "quest_exam_title": "Lehrlingsprüfung",
        "quest_exam_description": "Bestehe die Prüfung, um Magier zu werden.",
        "quest_lorem_ipsum_title": "lorem ipsum",
        "quest_lorem_ipsum_description": "SISPSISPSISPS",
        "quest_test_title": "Test",
        "quest_test_description": "test",
        "quest_monsterhunt_title": "Monsterjagd",
        "quest_monsterhunt_description": "Besiege 10 Wölfe, um Erfahrungspunkte zu sammeln.",
        "quest_treasurehunt_title": "Schatzsuche",
        "quest_treasurehunt_description": "Finde die versteckte Truhe im Wald.",
        "quest_errands_title": "Botengang",
        "quest_errands_description": "Überbringe eine Nachricht und erhalte eine Belohnung.",
        "quest_sword_title": "Das verlorene Schwert",
        "quest_sword_description": "Finde das legendäre Schwert und bring es zurück.",
        "quest_herb_title": "Kräutersammler",
        "quest_herb_description": "Sammle 5 Heilkräuter für den Alchemisten.",
        "quest_dragon_title": "Drachentöter",
        "quest_dragon_description": "Besiege den Drachen, der das Dorf bedroht.",
        "quest_depths_title": "Gefährliche Tiefen",
        "quest_depths_description": "Erkunde die verfluchte Höhle und schaffe es, lebend zurückzukommen.",
        "quest_ipsum_lorem_title": "ipsum lorem",
        "quest_ipsum_lorem_description": "GRRR Grrrr",

        # Dungeon
        "dungeon_monster_1_title": "Monster 1",
        "dungeon_monster_1_description": "Nicht so furchterregend, nur Monster Nummer 1",
        "dungeon_monster_2_title": "Monster 2",
        "dungeon_monster_2_description": "Nicht so furchterregend, nur Monster Nummer 2",
        "dungeon_monster_3_title": "Monster 3",
        "dungeon_monster_3_description": "Nicht so furchterregend, nur Monster Nummer 3",
        "dungeon_monster_4_title": "Monster 4",
        "dungeon_monster_4_description": "Nicht so furchterregend, nur Monster Nummer 4",
        "dungeon_monster_5_title": "Monster 5",
        "dungeon_monster_5_description": "Nicht so furchterregend, nur Monster Nummer 5",
        "dungeon_enemy_1_title": "Gegner 1",
        "dungeon_enemy_1_description": "Nicht so furchterregend, nur Gegner Nummer 1",
        "dungeon_enemy_2_title": "Gegner 2",
        "dungeon_enemy_2_description": "Nicht so furchterregend, nur Gegner Nummer 2",
        "dungeon_enemy_3_title": "Gegner 3",
        "dungeon_enemy_3_description": "Nicht so furchterregend, nur Gegner Nummer 3",
        "dungeon_enemy_4_title": "Gegner 4",
        "dungeon_enemy_4_description": "Nicht so furchterregend, nur Gegner Nummer 4",
        "dungeon_enemy_5_title": "Gegner 5",
        "dungeon_enemy_5_description": "Nicht so furchterregend, nur Gegner Nummer 5",
        "dungeon_boss_1_title": "Boss 1",
        "dungeon_boss_1_description": "Nicht so furchterregend, nur Boss Nummer 1",
        "dungeon_boss_2_title": "Boss 2",
        "dungeon_boss_2_description": "Nicht so furchterregend, nur Boss Nummer 2",
        "dungeon_boss_3_title": "Boss 3",
        "dungeon_boss_3_description": "Nicht so furchterregend, nur Boss Nummer 3",
        "dungeon_boss_4_title": "Boss 4",
        "dungeon_boss_4_description": "Nicht so furchterregend, nur Boss Nummer 4",
        "dungeon_boss_5_title": "Boss 5",
        "dungeon_boss_5_description": "Nicht so furchterregend, nur Boss Nummer 5"
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
        self.is_fullscreen = False
        self.language = ENGLISH
        self.fps = FPS
        self.title = "RPG Adventure"

        self.sounds = {
            #"Test": pygame.mixer.Sound("TestPath")
        }
        self.current_music_path = None
        self.music_volume = 0.05
        self.sound_volume = 0.1
        self.auto_save = True
        self.music_on = True
        self.sounds_on = False
        self.debug = False

    def translate(self, key):
        return translations.get(self.language, {}).get(key, f"[{key}]")
    
    def on_toggle_auto_save(self, state):
        self.auto_save = state

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