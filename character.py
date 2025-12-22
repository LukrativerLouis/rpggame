

class Character:
    def __init__(self):
        self.gold = 0
        self.experience = 0
        self.level = 1
        self.damage = 1
        self.health = 10

    def adjust_gold_and_exp(self, new_gold = 0, new_exp = 0):
        self.gold += new_gold
        self.experience += new_exp