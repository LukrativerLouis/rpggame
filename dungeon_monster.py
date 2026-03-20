import random
import pygame
from character import *

class Dungeon_Monster():
    def __init__(self):
        self.name = ""
        self.description = ""
        self.gold = 0
        self.experience = 0
        self.item = None
        self.enemy = Enemy()


dungeon_monster_list = {
    "Dungeon 1": [
        {"name": "Monster 1", "description": "Not that scary only number 1", "gold": 5, "experience": 100, "item": "randomItemID1", "level": 10,"damage": 10, "max_health": 100},
        {"name": "Monster 2", "description": "Not that scary only number 2", "gold": 10, "experience": 1000, "item": "randomItemID2", "level": 12,"damage": 30, "max_health": 1000},
        {"name": "Monster 3", "description": "Not that scary only number 3", "gold": 20, "experience": 2000, "item": "randomItemID3", "level": 15,"damage": 50, "max_health": 3000},
        {"name": "Monster 4", "description": "Not that scary only number 4", "gold": 30, "experience": 3000, "item": "randomItemID4", "level": 20,"damage": 50, "max_health": 4000},
        {"name": "Monster 5", "description": "Not that scary only number 5", "gold": 500, "experience": 5000, "item": "randomItemID5", "level": 25,"damage": 100, "max_health": 5000},
    ], 
    "Dungeon 2": [

    ], 
    "Dungeon 3": [

    ]
}