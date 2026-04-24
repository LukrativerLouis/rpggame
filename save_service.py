import json
import base64
from settings import *
from character import *

class Save_Service:
    def __init__(self, game):
        self.game = game

        self.character_list = [None, None, None]
        self.shop_list = []
        self.music_on = None
        self.sounds_on = None
        self.sound_volume = None
        self.music_volume = None

    def save_progress(self, game):
        if game.is_web:
            return
        
        shop_data_to_save = []
        for slot_shop in game.all_shops_data:
            shop_data_to_save.append([self.save_to_dict(item) for item in slot_shop])

        raw_data = {
            "character_list": [ self.save_to_dict(char) for char in (game.character_list or [])],
            "shop_list": shop_data_to_save,
            "music": game.settings.music_on,
            "sound": game.settings.sounds_on,
            "sound_volume": game.settings.sound_volume,
            "music_volume": game.settings.music_volume,
            "forced_width": game.settings.forced_width,
            "forced_height": game.settings.forced_height,
            "toggle_fullscreen": game.is_fullscreen,
            "language": game.settings.language
        }
        
        data_string = json.dumps(raw_data, indent=4)
        encoded = base64.b64encode(data_string.encode()).decode()
        
        with open(SAVE_FILE_PATH, "w") as f:
            f.write(encoded)

    def load_progress(self):
        try:
            with open(SAVE_FILE_PATH, "r") as f:
                encoded = f.read()
                decoded_data = base64.b64decode(encoded).decode()
                data = json.loads(decoded_data)

                char_dicts = data.get("character_list", [None, None, None])
                self.character_list = []
                for d in char_dicts:
                    if d is not None:
                        self.character_list.append(Character.from_dict(d))
                    else:
                        self.character_list.append(None)

                    item_slots = data.get("shop_list", [[], [], []])
                    self.shop_list = [[], [], []]
                    
                    for i in range(len(item_slots)):
                        for item_dict in item_slots[i]:
                            if item_dict:
                                self.shop_list[i].append(Item.from_dict(item_dict))

                self.game.settings.music_on = data.get("music")
                self.game.settings.sounds_on = data.get("sound")
                self.game.settings.sound_volume = data.get("sound_volume")
                self.game.settings.music_volume = data.get("music_volume")
                self.game.settings.forced_width = data.get("forced_width")
                self.game.settings.forced_height = data.get("forced_height")
                self.game.is_fullscreen = data.get("toggle_fullscreen")
                self.game.settings.language = data.get("language")

        except FileNotFoundError:
            print("File not found")
            self.shop_list = [[], [], []]

        except Exception as e:
            print(f"Error while loading the save file: {e}")
            self.shop_list = [[], [], []]

    def save_to_dict(self, obj):
        try:
            return obj.to_dict()
        except AttributeError:
            return None # Oder ein Default-Dict
