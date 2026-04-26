from item import *

class Character:
    def __init__(self, name, image, gold, level):
        self.name = name
        self.image = image
        self.current_stamina = 50
        self.max_stamina = 100
        self.gold = gold
        self.experience = 0
        self.required_experience = CHARACTER_BASE_XP
        self.level = level
        self.damage = 10
        self.strength = 0
        self.dexterity = 0
        self.endurance = 0
        self.precision = 0
        self.armor = 0
        self.class_type = WARRIOR
        self.max_health = 10
        self.current_health = self.max_health
        self.attack_score = 0
        self.base_character_value_list = {
            "strength": 0,
            "dexterity": 0,
            "endurance": 0,
            "precision": 0
        }
        self.dungeon_completed = [1, 1, 1]
        self.inventory: list[Item] = []
        self.equipment: list[Item] = []
        self.shop_items: list[Item] = []
        self.item_stats_calculated_list: list[Item] = []

    def adjust_gold_and_exp(self, new_gold = 0, new_exp = 0):
        self.gold += new_gold
        self.experience += new_exp

    def check_level_up(self):
        if self.required_experience != self.calculate_required_exp():
            self.required_experience = self.calculate_required_exp()

        if self.experience >= self.required_experience:
            self.level += 1
            self.experience -= self.required_experience
            self.required_experience = self.calculate_required_exp()

    def calculate_required_exp(self):
        return round(CHARACTER_BASE_XP * (pow(XP_MULTIPLIER, self.level - 1)))

    def get_item_gold_value(self):
        # maybe give type (legendary or common or uncommon or something)
        return self.level
    
    def calculate_player_stats(self):
        if not self.item_stats_calculated_list:
            self.item_stats_calculated_list = []

        if self.equipment:
            for item in self.equipment:
                if item not in self.item_stats_calculated_list:
                    self.strength += item.strength
                    self.dexterity += item.dexterity
                    self.endurance += item.endurance
                    self.precision += item.precision
                    self.armor += item.armor
                    self.item_stats_calculated_list.append(item)
            if self.equipment != self.item_stats_calculated_list:
                self.clear_character_stats()
        elif self.item_stats_calculated_list:
            self.clear_character_stats()
        
        self.calculate_damage()
        
    def clear_character_stats(self):
        self.strength, self.dexterity, self.endurance, self.precision = self.get_base_character_values()
        self.item_stats_calculated_list.clear()
        self.calculate_player_stats()

    def get_base_character_values(self):
        return self.base_character_value_list["strength"], self.base_character_value_list["dexterity"], self.base_character_value_list["endurance"], self.base_character_value_list["precision"]
    
    def calculate_damage(self):
        if self.class_type:
            if self.class_type == WARRIOR or self.class_type == ARCHER:
                self.damage = 1
            elif self.class_type == MAGE:
                self.damage = 1

    # dictionary stuff

    def to_dict(self):
        data = self.__dict__.copy()

        data["inventory"] = [item.to_dict() for item in self.inventory]
        data["equipment"] = [item.to_dict() for item in self.equipment]
        data["shop_items"] = [item.to_dict() for item in self.shop_items]
        data["item_stats_calculated_list"] = None
        
        return data
    
    @classmethod

    def from_dict(cls, data):
        inventory_data = data.pop("inventory", [])
        equipment_data = data.pop("equipment", [])
        shop_data = data.pop("shop_items", [])

        char = cls(
            name = data["name"],
            image = data["image"],
            gold = data["gold"],
            level = data["level"]
        )

        for key, value in data.items():
            setattr(char, key, value)

        char.inventory = [Item.from_dict(i) for i in inventory_data]
        char.equipment = [Item.from_dict(i) for i in equipment_data]
        char.shop_items = [Item.from_dict(i) for i in shop_data]

        return char

class Enemy:
    def __init__(self, class_type, level = 1, strength = 0, dexterity = 0, endurance = 0, precision = 0, armor = 0, max_health = 10):
        self.class_type = class_type
        self.level = level
        self.damage = 0
        self.strength = strength
        self.dexterity = dexterity
        self.endurance = endurance
        self.precision = precision
        self.armor = armor
        self.max_health = max_health
        self.current_health = max_health
        self.attack_score = 0

        self.calculate_damage()

    def calculate_damage(self):
        if self.class_type:
            if self.class_type == WARRIOR or self.class_type == ARCHER:
                self.damage = 1
            elif self.class_type == MAGE:
                self.damage = 1