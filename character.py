

class Character:
    def __init__(self):
        self.gold = 0
        self.experience = 0
        self.required_experience = 100
        self.level = 1
        self.damage = 1
        self.max_health = 20
        self.current_health = self.max_health
        self.attack_score = 0
        self.inventory = []
        self.equipment = []

    def adjust_gold_and_exp(self, new_gold = 0, new_exp = 0):
        self.gold += new_gold
        self.experience += new_exp

    def get_item_gold_value(self):
        # maybe return type (legendary or common or uncommon or something)
        return self.level

class Enemy:
    def __init__(self, level = 1, damage = 1, max_health = 10):
        self.level = level
        self.damage = damage
        self.max_health = max_health
        self.current_health = max_health
        self.attack_score = 0