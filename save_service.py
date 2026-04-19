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

        raw_data = {
            "character_list": [ self.save_to_dict(char) for char in (game.character_list or [])],
            "shop_list": [self.save_to_dict(item) for item in (game.shop_list or [])],
            "music": game.settings.music_on,
            "sound": game.settings.sounds_on,
            "sound_volume": game.settings.sound_volume,
            "music_volume": game.settings.music_volume,
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

                item_dicts = data.get("shop_list", [])
                self.shop_list = []
                for item in item_dicts:
                    if item is not None:
                        self.shop_list.append(Item.from_dict(item))
                    else:
                        self.shop_list.append(None)

                self.game.settings.music_on = data.get("music")
                self.game.settings.sounds_on = data.get("sound")
                self.game.settings.sound_volume = data.get("sound_volume")
                self.game.settings.music_volume = data.get("music_volume")

        except FileNotFoundError:
            print("File not found")
            #self.save_progress()
            #self.load_progress()

        except Exception as e:
            print(f"Error while loading the save file: {e}")

    def save_to_dict(self, obj):
        try:
            return obj.to_dict()
        except AttributeError:
            return None # Oder ein Default-Dict

    def refresh_data(self, game):
        self.game = game