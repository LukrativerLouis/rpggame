from utils import *
from settings import *
import random

class Item():
    def __init__(self, x, y, width, height, name, physical_damage, magic_damage, armor, magic_resist, type, visible):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height)).convert_alpha()
        self.rect = self.surf.get_rect(topleft= (x, y))
        #self.image = image
        #self.rect = image.get_rect(topleft = (x, y))
        self.name = name
        self.physical_damage = physical_damage
        self.magic_damage = magic_damage
        self.armor = armor
        self.magic_resist = magic_resist
        self.type = type
        self.visible = visible

    def draw(self, canvas, mouse_pos):
        self.surf.fill("lightblue")
        canvas.blit(self.surf, self.rect)

    def handle_events(self, event, mouse_pos):
        #TODO: Hover for TOOLTIPS
        pass

class Item_Holder():
    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.type = type

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

# item_holder types
# all types not used for items

SHOP = "shop"
INVENTORY = "inventory"


item_list = {
    "name": "Wooden Sword", "physical_damage": 1, "magic_damage": 0, "armor": 1, "magic_resist": 0, "type": WEAPON, "sub_type": SWORD
}

def getItemDetails():
    random_item = random.choice(item_list)
    return random_item["name"], random_item["physical_damage"], random_item["magic_damage"], random_item["armor"], random_item["magic_resist"]