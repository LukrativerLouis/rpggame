from item import *
from settings import *

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
        self.dungeon_completed = {
            DUNGEON_1: 1,
            DUNGEON_2: 1,
            DUNGEON_3: 1
        }
        self.inventory: list[Item] = []
        self.equipment: list[Item] = []
        self.shop_items: list[Item] = []
        self.item_stats_calculated_list: list[Item] = []
        self.quest_list: list[Quest] = []

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
        data["quest_list"] = [q.to_dict() for q in self.quest_list]
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        inventory_data = data.pop("inventory", [])
        equipment_data = data.pop("equipment", [])
        shop_data = data.pop("shop_items", [])
        quest_data = data.pop("quest_list", [])

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
        char.quest_list = [Quest.from_dict(q) for q in quest_data]

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

    def to_dict(self):
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data):
        enemy = cls(
            class_type=data["class_type"],
            level=data["level"],
            strength=data["strength"],
            dexterity=data["dexterity"],
            endurance=data["endurance"],
            precision=data["precision"],
            armor=data["armor"],
            max_health=data["max_health"]
        )
        enemy.current_health = data["current_health"]
        enemy.attack_score = data["attack_score"]
        enemy.damage = data["damage"]
        return enemy

class Quest():
    def __init__(self, gold, experience, item, duration, stamina_cost):
        self.title, self.description = getQuestDetails()
        self.gold = gold
        self.experience = experience
        self.item = item
        self.duration = duration # duration in seconds
        self.stamina_cost = stamina_cost
        self.enemy = Enemy(class_type= random.choice(CLASS_TYPE_LIST))

    def to_dict(self):
        data = self.__dict__.copy()
        data["enemy"] = self.enemy.to_dict() if self.enemy else None
        return data
    
    @classmethod
    def from_dict(cls, data):
        enemy_data = data.pop("enemy", None)
        
        quest = cls(
            gold=data["gold"],
            experience=data["experience"],
            item=data["item"],
            duration=data["duration"],
            stamina_cost=data["stamina_cost"]
        )
        
        quest.title = data["title"]
        quest.description = data["description"]
        
        if enemy_data:
            quest.enemy = Enemy.from_dict(enemy_data)
            
        return quest  

quests_list = {
    "quests": [
        {"title": "Lehrlingsprüfung", "description": "Bestehe die Prüfung, um ein Magier zu werden."},
        {"title": "lorem ipsum", "description": "SISPSISPSISPS."},
        {"title": "ipsum loren", "description": "neee neneee jaaj jajajaj."},
        {"title": "Monsterjagd", "description": "Besiege 10 Wölfe, um Erfahrung zu sammeln."},
        {"title": "Schatzsuche", "description": "Finde die versteckte Truhe im Wald."},
        {"title": "Botengang", "description": "Liefer eine Nachricht und erhalte eine Belohnung."},
        {"title": "Das verlorene Schwert", "description": "Finde das legendäre Schwert und bringe es zurück."},
        {"title": "Kräutersammler", "description": "Sammle 5 Heilkräuter für den Alchemisten."},
        {"title": "Drachenbezwinger", "description": "Besiege den Drachen, der das Dorf bedroht."},
        {"title": "Gefährliche Tiefen", "description": "Erkunde die verfluchte Höhle und kehre lebend zurück."}
    ]
}

def get_quest(character_level):
    base_xp = 15
    base_gold = 5
    variation = random.uniform(0.8, 1.2)

    quest_exp = round(base_xp * (character_level ** 1.2) * variation)
    quest_gold = round((base_gold + (character_level * 3)) * variation)
    quest_item = None
    quest_duration = random.randint(5, 30)
    quest_stamina_cost = random.randint(1, 10)

    return Quest(quest_gold, quest_exp, quest_item, quest_duration, quest_stamina_cost)

def getQuestDetails():
    random_quest = random.choice(quests_list["quests"])
    return random_quest["title"], random_quest["description"]