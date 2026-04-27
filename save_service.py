import json
import base64
from settings import *
from character import *

class Save_Service:
    def __init__(self, system, settings):
        self.system = system
        self.settings = settings

        self.character_list = [None, None, None]
        self.shop_list = []
        self.quest_list = [[], [], []]
        self.dungeon_completed = []
        # options
        self.music_on = None
        self.sounds_on = None
        self.sound_volume = None
        self.music_volume = None
        self.forced_width = None
        self.forced_height = None
        self.toggle_fullscreen = None
        self.language = None

    def save_options(self, settings):
        if self.system.is_web:
            return

        raw_data = {
            "music": settings.music_on,
            "sound": settings.sounds_on,
            "sound_volume": settings.sound_volume,
            "music_volume": settings.music_volume,
            "forced_width": settings.forced_width,
            "forced_height": settings.forced_height,
            "toggle_fullscreen": settings.is_fullscreen,
            "language": settings.language,
        }
        
        data_string = json.dumps(raw_data, indent=4)
        encoded = base64.b64encode(data_string.encode()).decode()
        
        with open(SAVE_FILE_PATH_OPTIONS, "w") as f:
            f.write(encoded)

    def load_options(self):
        try:
            with open(SAVE_FILE_PATH_OPTIONS, "r") as f:
                encoded = f.read()
                decoded_data = base64.b64decode(encoded).decode()
                data = json.loads(decoded_data)

                self.settings.music_on = data.get("music")
                self.settings.sounds_on = data.get("sound")
                self.settings.sound_volume = data.get("sound_volume")
                self.settings.music_volume = data.get("music_volume")
                self.settings.forced_width = data.get("forced_width")
                self.settings.forced_height = data.get("forced_height")
                self.settings.is_fullscreen = data.get("toggle_fullscreen")
                self.settings.language = data.get("language")

        except FileNotFoundError:
            print("File not found")

        except Exception as e:
            print(f"Error while loading the save file: {e}")

    def save_data(self, all_shops_data, character_list, dungeon_completed, quest_list = None,):
        if self.system.is_web:
            return
        
        shop_data_to_save = []
        for slot_shop in all_shops_data:
            shop_data_to_save.append([self.save_to_dict(item) for item in slot_shop])

        active_slot = self.system.menu.character_slot
        if character_list[active_slot] and quest_list:
            character_list[active_slot].quest_list = quest_list
            self.quest_list[active_slot] = quest_list

        raw_data = {
            "character_list": [ self.save_to_dict(char) for char in (character_list or [])],
            "shop_list": shop_data_to_save,
            "dungeon_completed": dungeon_completed,
        }
        
        data_string = json.dumps(raw_data, indent=4)
        encoded = base64.b64encode(data_string.encode()).decode()
        
        with open(SAVE_FILE_PATH_DATA, "w") as f:
            f.write(encoded)

    def load_data(self):
        try:
            with open(SAVE_FILE_PATH_DATA, "r") as f:
                encoded = f.read()
                decoded_data = base64.b64decode(encoded).decode()
                data = json.loads(decoded_data)

                char_dicts = data.get("character_list", [None for _ in range(3)])
                self.character_list = []
                for d in char_dicts:
                    if d is not None:
                        self.character_list.append(Character.from_dict(d))
                    else:
                        self.character_list.append(None)

                item_slots = data.get("shop_list", [[] for _ in range(3)])
                self.shop_list = [[] for _ in range(3)]
                
                for i in range(len(item_slots)):
                    for item_dict in item_slots[i]:
                        if item_dict:
                            self.shop_list[i].append(Item.from_dict(item_dict))

                self.dungeon_completed = data.get("dungeon_completed")

                while len(self.character_list) < 3:
                    self.character_list.append(None)
                while len(self.shop_list) < 3:
                    self.shop_list.append([])

        except FileNotFoundError:
            print("File not found")
            self.shop_list = [[] for _ in range(3)]

        except Exception as e:
            print(f"Error while loading the save file: {e}")
            self.shop_list = [[] for _ in range(3)]

    def save_to_dict(self, obj):
        try:
            return obj.to_dict()
        except AttributeError:
            return None # Oder ein Default-Dict
