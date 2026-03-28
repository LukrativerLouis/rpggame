from item import *

class Character:
    def __init__(self):
        self.gold = 100
        self.experience = 0
        self.required_experience = 100
        self.level = 1
        self.damage = 0
        self.physical_damage = 0
        self.magic_damage = 0
        self.armor = 0
        self.magic_resist = 0
        self.class_type = WARRIOR
        self.max_health = 20
        self.current_health = self.max_health
        self.attack_score = 0
        self.base_character_value_list = {
            "physical_damage": 0,
            "magic_damage": 0,
            "armor": 0,
            "magic_resist": 0
        }
        self.inventory: list[Item] = []
        self.equipment: list[Item] = []
        self.item_stats_calculated_list: list[Item] = []

    def adjust_gold_and_exp(self, new_gold = 0, new_exp = 0):
        self.gold += new_gold
        self.experience += new_exp

    def check_level_up(self):
        if self.experience >= self.required_experience:
            self.level += 1
            self.experience -= self.required_experience
            self.required_experience = round(self.required_experience * 1.1)

    def get_item_gold_value(self):
        # maybe give type (legendary or common or uncommon or something)
        return self.level
    
    def calculate_player_stats(self):
        if self.equipment:
            for item in self.equipment:
                if item not in self.item_stats_calculated_list:
                    self.physical_damage += item.physical_damage
                    self.magic_damage += item.magic_damage
                    self.armor += item.armor
                    self.magic_resist += item.magic_resist
                    self.item_stats_calculated_list.append(item)
            if self.equipment != self.item_stats_calculated_list:
                self.clear_character_stats()
        elif self.item_stats_calculated_list:
            self.clear_character_stats()
        
        self.calculate_damage()
        
    def clear_character_stats(self):
        self.physical_damage, self.magic_damage, self.armor, self.magic_resist = self.get_base_character_values()
        self.item_stats_calculated_list.clear()
        self.calculate_player_stats()

    def get_base_character_values(self):
        return self.base_character_value_list["physical_damage"], self.base_character_value_list["magic_damage"], self.base_character_value_list["armor"], self.base_character_value_list["magic_resist"]
    
    def calculate_damage(self):
        if self.class_type:
            if self.class_type == WARRIOR or self.class_type == ARCHER:
                self.damage = self.physical_damage
            elif self.class_type == MAGE:
                self.damage = self.magic_damage

class Enemy:
    def __init__(self, level = 1, damage = 1, max_health = 10):
        self.level = level
        self.damage = damage
        self.max_health = max_health
        self.current_health = max_health
        self.attack_score = 0

# class types

WARRIOR = "warrior"
MAGE = "mage"
ARCHER = "archer"