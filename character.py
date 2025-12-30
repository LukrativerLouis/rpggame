

class Character:
    def __init__(self):
        self.gold = 0
        self.experience = 0
        self.required_experience = 0
        self.level = 1
        self.damage = 1
        self.max_health = 20
        self.current_health = self.max_health
        self.attack_score = 0

    def adjust_gold_and_exp(self, new_gold = 0, new_exp = 0):
        self.gold += new_gold
        self.experience += new_exp

class Enemy:
    def __init__(self):
        self.level = 1
        self.damage = 1
        self.max_health = 10
        self.current_health = self.max_health
        self.attack_score = 0