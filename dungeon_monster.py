import random
import pygame
from character import *

class Dungeon_Monster():
    def __init__(self, name, description, gold, experience, level, damage, max_health, item = None):
        self.name = name
        self.description = description
        self.gold = gold
        self.experience = experience
        self.item = item
        self.enemy_level = level
        self.enemy_damage = damage
        self.enemy_max_health = max_health
        self.enemy = Enemy(level = level, damage = damage, max_health = max_health)

    def reset_enemy(self):
        self.enemy = Enemy(level = self.enemy_level, damage = self.enemy_damage, max_health = self.enemy_max_health)

DUNGEON_1 = "Dungeon 1"
DUNGEON_2 = "Dungeon 2"
DUNGEON_3 = "Dungeon 3"

dungeon_monster_list = {
    DUNGEON_1: [
        Dungeon_Monster(name="Monster 1", description="Not that scary only number 1", gold=5, experience=100, item="randomItemID1", level=10, damage=1, max_health=5),
        Dungeon_Monster(name="Monster 2", description="Not that scary only number 2", gold=10, experience=1000, item="randomItemID2", level=12, damage=30, max_health=1000),
        Dungeon_Monster(name="Monster 3", description="Not that scary only number 3", gold=20, experience=2000, item="randomItemID3", level=15, damage=50, max_health=3000),
        Dungeon_Monster(name="Monster 4", description="Not that scary only number 4", gold=30, experience=3000, item="randomItemID4", level=20, damage=50, max_health=4000),
        Dungeon_Monster(name="Monster 5", description="Not that scary only number 5", gold=500, experience=5000, item="randomItemID5", level=25, damage=100, max_health=5000),
    ], 

    DUNGEON_2: [
        Dungeon_Monster(name="Enemy 1", description="Not that scary only number 1", gold=5, experience=100, item="randomItemID1", level=10, damage=10, max_health=10000),
        Dungeon_Monster(name="Enemy 2", description="Not that scary only number 2", gold=10, experience=1000, item="randomItemID2", level=12, damage=30, max_health=1000),
        Dungeon_Monster(name="Enemy 3", description="Not that scary only number 3", gold=20, experience=2000, item="randomItemID3", level=15, damage=50, max_health=3000),
        Dungeon_Monster(name="Enemy 4", description="Not that scary only number 4", gold=30, experience=3000, item="randomItemID4", level=20, damage=50, max_health=4000),
        Dungeon_Monster(name="Enemy 5", description="Not that scary only number 5", gold=500, experience=5000, item="randomItemID5", level=25, damage=100, max_health=5000),
    ], 

    DUNGEON_3: [
        Dungeon_Monster(name="Boss 1", description="Not that scary only number 1", gold=5, experience=100, item="randomItemID1", level=10, damage=10, max_health=100),
        Dungeon_Monster(name="Boss 2", description="Not that scary only number 2", gold=10, experience=1000, item="randomItemID2", level=12, damage=30, max_health=1000),
        Dungeon_Monster(name="Boss 3", description="Not that scary only number 3", gold=20, experience=2000, item="randomItemID3", level=15, damage=50, max_health=3000),
        Dungeon_Monster(name="Boss 4", description="Not that scary only number 4", gold=30, experience=3000, item="randomItemID4", level=20, damage=50, max_health=4000),
        Dungeon_Monster(name="Boss 5", description="Not that scary only number 5", gold=500, experience=5000, item="randomItemID5", level=25, damage=100, max_health=5000),
    ]
}