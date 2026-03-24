from utils import *
from settings import *

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