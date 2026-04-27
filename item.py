from utils import *
from settings import *
import random

class Item():
    def __init__(self, id, x, y, width, height, name, strength, dexterity, endurance, precision, armor, weapon_p, weapon_s, gold_value, type, sub_type, visible):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height)).convert_alpha()
        self.rect = self.surf.get_rect(center= (x, y))
        #self.image = image
        #self.rect = image.get_rect(topleft = (x, y))
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.endurance = endurance
        self.precision = precision
        self.armor = armor
        self.weapon_p = weapon_p
        self.weapon_s = weapon_s
        self.gold_value = gold_value
        self.sell_value = self.get_sell_value()
        self.type = type
        self.sub_type = sub_type
        self.visible = visible
        color_list = ["lightblue", "cornflowerblue", "magenta", "orange", "darkseagreen", "deeppink", "darkorange4"]
        self.color = random.choice(color_list)
    
    def get_sell_value(self):
        # TODO: make sell value dynamic
        return self.gold_value * SELL_FACTOR

    def draw(self, canvas, mouse_pos):
        self.surf.fill(self.color)
        canvas.blit(self.surf, self.rect)
        show_text(canvas, self.id, self.rect.centerx, self.rect.centery, "black", True)

    def handle_events(self, event, mouse_pos):
        #TODO: Hover for TOOLTIPS
        pass

    # dictionary stuff

    def to_dict(self):
        return {
            "id": self.id,
            "width": self.width,
            "height": self.height,
            "name": self.name,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "endurance": self.endurance,
            "precision": self.precision,
            "armor": self.armor,
            "weapon_p": self.weapon_p,
            "weapon_s": self.weapon_s,
            "gold_value": self.gold_value,
            "type": self.type,
            "sub_type": self.sub_type,
            "visible": False,
            "x": self.x,
            "y": self.y
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class Item_Holder():
    def __init__(self, x, y, width, height, color, type, highlight_color = "indigo"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height)).convert_alpha()
        self.rect = self.surf.get_rect(topleft = (x, y))
        self.color = color
        self.highlight_color = highlight_color
        self.current_color = self.color
        self.type = type
        self.highlight = False

    def draw(self, canvas, mouse_pos):
        if self.highlight:
            self.current_color = self.highlight_color
        else:
            self.current_color = self.color

        self.surf.fill((0, 0, 0, 0)) 
        
        pygame.draw.rect(self.surf, self.current_color, (0, 0, self.width, self.height), 2)
        
        canvas.blit(self.surf, self.rect)

# item types

WEAPON = "weapon"
SWORD = "sword"
BOW = "bow"
STAFF = "staff"
HELMET = "Helmet"
CHEST_PLATE = "chest_plate"
LEGGINGS = "leggings"
SHOES = "shoes"
ACCESSORIES = "accessories"
AMULET = "amulet"
RING = "ring"
EXTRA3 = "extra3"
EXTRA4 = "extra4"

LIST_OF_EQUIPMENT_TYPES = [
    WEAPON, HELMET, CHEST_PLATE, LEGGINGS, SHOES, ACCESSORIES, AMULET, RING, EXTRA3, EXTRA4
]

# item_holder types
# all types not used for items

SHOP = "shop"
INVENTORY = "inventory"

item_list = [
    {"name": "Wooden Sword", "strength": 1, "dexterity": 0, "endurance": 1, "precision": 0, "armor": 0, "weapon_p": 5, "weapon_s": 0.5,"type": WEAPON, "sub_type": SWORD},
    {"name": "Cracked Wooden Sword", "strength": 0.5, "dexterity": 0, "endurance": 0.5, "precision": 0, "armor": 0, "weapon_p": 3, "weapon_s": 0.3, "type": WEAPON, "sub_type": SWORD}
]

def getItemDetailsRandom():
    random_item = random.choice(item_list)
    return random.randint(0, 10000), random_item["name"], random_item["strength"], random_item["dexterity"], random_item["endurance"], random_item["precision"], random_item["armor"], random_item["weapon_p"], random_item["weapon_s"], random_item["type"], random_item["sub_type"]