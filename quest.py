import random
from settings import *

class Quest():
    def __init__(self, quest_type):
        self.title, self.description = getQuestDetails(quest_type)
        self.quest_type = quest_type
        self.gold = 0
        self.experience = 0
        self.item = 0
        self.duration = 0 # duration in seconds

        if self.quest_type == EXPERIENCE_QUEST_TYPE:
            self.experience = 10
            self.gold = 1
            self.item = 0
            self.duration = 2 # only for test TODO 
        elif self.quest_type == GOLD_QUEST_TYPE:
            self.experience = 1
            self.gold = 10
            self.item = 0
            self.duration = 10
        elif self.quest_type == ITEM_QUEST_TYPE:
            self.experience = 1
            self.gold = 1
            self.item = 0
            self.duration = 10
        elif self.quest_type == DANGEROUS_QUEST_TYPE:
            self.experience = 20
            self.gold = 20
            self.item = 0
            self.duration = 20

quests_list = {
    EXPERIENCE_QUEST_TYPE: [
        {"title": "Lehrlingsprüfung", "description": "Bestehe die Prüfung, um ein Magier zu werden."},
        {"title": "lorem ipsum", "description": "SISPSISPSISPS."},
        {"title": "ipsum loren", "description": "neee neneee jaaj jajajaj."},
        {"title": "Monsterjagd", "description": "Besiege 10 Wölfe, um Erfahrung zu sammeln."},
    ],
    GOLD_QUEST_TYPE: [
        {"title": "Schatzsuche", "description": "Finde die versteckte Truhe im Wald."},
        {"title": "Botengang", "description": "Liefer eine Nachricht und erhalte eine Belohnung."}
    ],
    ITEM_QUEST_TYPE: [
        {"title": "Das verlorene Schwert", "description": "Finde das legendäre Schwert und bringe es zurück."},
        {"title": "Kräutersammler", "description": "Sammle 5 Heilkräuter für den Alchemisten."}
    ],
    DANGEROUS_QUEST_TYPE: [
        {"title": "Drachenbezwinger", "description": "Besiege den Drachen, der das Dorf bedroht."},
        {"title": "Gefährliche Tiefen", "description": "Erkunde die verfluchte Höhle und kehre lebend zurück."}
    ]
}

def getQuestDetails(quest_type):
    random_quest = random.choice(quests_list[quest_type])
    return random_quest["title"], random_quest["description"]