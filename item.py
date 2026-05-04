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
        self.tooltip = Tooltip(self.rect.centerx, self.rect.centery, 200, 100, "", offset = 100)
        color_list = ["lightblue", "cornflowerblue", "magenta", "orange", "darkseagreen", "deeppink", "darkorange4"]
        self.color = random.choice(color_list)

        self.create_tooltip()

    def compare_with_equipped(self, equipped_item=None):
        if not equipped_item:
            return self.create_tooltip()
        
        relevant_stats = ITEM_STAT_MAPPING.get(self.type, 
            ["strength", "dexterity", "endurance", "precision", "armor"])
        
        comparison_lines = [f"--- {self.name} vs {equipped_item.name} ---"]
        
        for stat in relevant_stats:
            new_val = getattr(self, stat, 0)
            old_val = getattr(equipped_item, stat, 0)
            diff = new_val - old_val
            
            if diff > 0:
                symbol = "+"
                color = "green"
            elif diff < 0:
                symbol = "-"
                color = "red"
            else:
                symbol = ""
                color = "white"

            if old_val == 0 and new_val == 0:
                continue
            
            comparison_lines.append(f"{stat.capitalize()}: {new_val} ({symbol}{abs(diff)})")
        
        self.tooltip.text = "\n".join(comparison_lines)

    def create_tooltip(self):
        relevant_stats = ITEM_STAT_MAPPING.get(self.type, 
            ["strength", "dexterity", "endurance", "precision", "armor"])
        
        stats = [
            (f"--- {self.name} ---", True),
        ]
        
        for stat in relevant_stats:
            val = getattr(self, stat, 0)
            stats.append((f"{stat.capitalize()}: {val}", val > 0))
        
        stats.append((f"Cost: {self.gold_value}g", self.gold_value > 0))
        
        active_lines = [text for text, condition in stats if condition]
        self.tooltip.text = "\n".join(active_lines)
    
    def get_sell_value(self):
        # TODO: make sell value dynamic
        return round(self.gold_value * SELL_FACTOR)

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

ITEM_STAT_MAPPING = {
    WEAPON: ["strength", "dexterity", "precision", "endurance", "weapon_p", "weapon_s"],
    HELMET: ["armor", "strength", "dexterity", "precision", "endurance"],
    CHEST_PLATE: ["armor", "strength", "dexterity", "precision", "endurance"],
    LEGGINGS: ["armor", "strength", "dexterity", "precision", "endurance"],
    SHOES: ["armor", "strength", "dexterity", "precision", "endurance"],
    AMULET: ["strength", "dexterity", "endurance", "precision"],
    RING: ["strength", "dexterity", "endurance", "precision"],
    EXTRA3: ["strength", "dexterity", "endurance", "precision"],
    EXTRA4: ["strength", "dexterity", "endurance", "precision"],
}

item_list = [
    {"name": "Wooden Sword", "strength": 1, "dexterity": 0, "endurance": 1, "precision": 0, "armor": 0, "weapon_p": 5, "weapon_s": 0.5,"type": WEAPON, "sub_type": SWORD},
    {"name": "Cracked Wooden Sword", "strength": 0.5, "dexterity": 0, "endurance": 0.5, "precision": 0, "armor": 0, "weapon_p": 3, "weapon_s": 0.3, "type": WEAPON, "sub_type": SWORD}
]

def getItemDetailsRandom():
    random_item = random.choice(item_list)
    return random.randint(0, 10000), random_item["name"], random_item["strength"], random_item["dexterity"], random_item["endurance"], random_item["precision"], random_item["armor"], random_item["weapon_p"], random_item["weapon_s"], random_item["type"], random_item["sub_type"]