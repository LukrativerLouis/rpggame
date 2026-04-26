import random
from settings import *
from character import *

class Quest():
    def __init__(self, gold, experience, item, duration, stamina_cost):
        self.title, self.description = getQuestDetails()
        self.quest_type = None
        self.gold = gold
        self.experience = experience
        self.item = item
        self.duration = duration # duration in seconds
        self.stamina_cost = stamina_cost
        self.enemy = Enemy(class_type= random.choice(CLASS_TYPE_LIST))

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