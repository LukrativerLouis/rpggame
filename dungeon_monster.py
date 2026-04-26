from character import *
from settings import *

class Dungeon_Monster():
    def __init__(self, name, description, class_type, gold, experience, level, strength, dexterity, endurance, precision, armor, max_health, item = None):
        self.name = name
        self.description = description
        self.gold = gold
        self.experience = experience
        self.item = item
        self.enemy_level = level
        self.enemy_strength = strength
        self.enemy_dexterity = dexterity
        self.enemy_endurance = endurance
        self.enemy_precision = precision
        self.enemy_armor = armor
        self.enemy_max_health = max_health
        self.enemy = Enemy(class_type, level, strength, dexterity, endurance, precision, armor, max_health)

    def reset_enemy(self):
        self.enemy = Enemy(self.enemy.class_type, self.gold, self.experience, self.enemy_level, self.enemy_strength, self.enemy_dexterity, self.enemy_endurance, self.enemy_precision, self.enemy_armor, self.enemy_max_health)

dungeon_monster_list = {
    DUNGEON_1: [
        Dungeon_Monster(name="Monster 1", description="Not that scary only number 1", class_type=WARRIOR, gold=5, experience=150, level=10, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=5, item="randomItemID1"),
        Dungeon_Monster(name="Monster 2", description="Not that scary only number 2", class_type=WARRIOR, gold=10, experience=1000, level=12, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=1000, item="randomItemID2"),
        Dungeon_Monster(name="Monster 3", description="Not that scary only number 3", class_type=WARRIOR, gold=20, experience=2000, level=15, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=3000, item="randomItemID3"),
        Dungeon_Monster(name="Monster 4", description="Not that scary only number 4", class_type=WARRIOR, gold=30, experience=3000, level=20, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=4000, item="randomItemID4"),
        Dungeon_Monster(name="Monster 5", description="Not that scary only number 5", class_type=WARRIOR, gold=500, experience=5000, level=25, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=5000, item="randomItemID5"),
    ], 

    DUNGEON_2: [
        Dungeon_Monster(name="Enemy 1", description="Not that scary only number 1", class_type=WARRIOR, gold=5, experience=100, level=10, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=10000, item="randomItemID1"),
        Dungeon_Monster(name="Enemy 2", description="Not that scary only number 2", class_type=WARRIOR, gold=10, experience=1000, level=12, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=1000, item="randomItemID2"),
        Dungeon_Monster(name="Enemy 3", description="Not that scary only number 3", class_type=WARRIOR, gold=20, experience=2000, level=15, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=3000, item="randomItemID3"),
        Dungeon_Monster(name="Enemy 4", description="Not that scary only number 4", class_type=WARRIOR, gold=30, experience=3000, level=20, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=4000, item="randomItemID4"),
        Dungeon_Monster(name="Enemy 5", description="Not that scary only number 5", class_type=WARRIOR, gold=500, experience=5000, level=25, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=5000, item="randomItemID5"),
    ], 

    DUNGEON_3: [
        Dungeon_Monster(name="Boss 1", description="Not that scary only number 1", class_type=WARRIOR, gold=5, experience=100, level=10, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=100, item="randomItemID1"),
        Dungeon_Monster(name="Boss 2", description="Not that scary only number 2", class_type=WARRIOR, gold=10, experience=1000, level=12, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=1000, item="randomItemID2"),
        Dungeon_Monster(name="Boss 3", description="Not that scary only number 3", class_type=WARRIOR, gold=20, experience=2000, level=15, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=3000, item="randomItemID3"),
        Dungeon_Monster(name="Boss 4", description="Not that scary only number 4", class_type=WARRIOR, gold=30, experience=3000, level=20, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=4000, item="randomItemID4"),
        Dungeon_Monster(name="Boss 5", description="Not that scary only number 5", class_type=WARRIOR, gold=500, experience=5000, level=25, strength=0, dexterity=0, endurance=0, precision=0, armor=0, max_health=5000, item="randomItemID5"),
    ]
}