import pygame
from random import shuffle
from utils import *
from character import *
from quest import *

class Fight_Window:
    def __init__(self, quest_window, character: Character, completed_function):
        # init stuff
        self.start_fight = False
        self.quest_window = quest_window
        self.quest = self.quest_window.selected_quest
        self.fight_window_button_list = self.__create_fight_window_button()
        self.character = character
        self.enemy: Enemy = self.quest.enemy

        # ui
        self.health_bar_length = 370
        self.character_health_bar_ratio = self.character.max_health / self.health_bar_length
        self.enemy_health_bar_ratio = self.enemy.max_health / self.health_bar_length

        # time stuff
        self.initial_cooldown = 0.5
        self.attack_cooldown = 1
        self.start_time = pygame.time.get_ticks()

        # fight states
        self.fight_won = False
        self.fight_done = False
        self.completed_function = completed_function

        self.battle_log = []
        self.current_log_index = 0

        self.__simulate_fight()

    def __create_fight_window_button(self):
        button_skip = Button(position = (900, 1025), size = (150, 50), text = "skip fight", color = [255, 0, 0], change_color = [255, 50, 50], func = lambda: self.__finish_instantly() )
        button_faster = Button(position = (1250, 1025), size = (150, 50), text = "faster", color = [255, 0, 0], change_color = [255, 50, 50], func = lambda: self.__adjust_attack_cooldown())
        
        return [button_skip, button_faster]
    
    def __finish_instantly(self):
        while self.current_log_index < len(self.battle_log):
            attacker_type, damage = self.battle_log[self.current_log_index]

            if attacker_type == CHARACTER:
                self.enemy.current_health -= damage
            else:
                self.character.current_health -= damage
            self.current_log_index += 1

        self.fight_done = True
    
    def __adjust_attack_cooldown(self):
        self.attack_cooldown *= 0.5

    def __simulate_fight(self):
        temp_character_health = self.character.current_health
        temp_enemy_health = self.enemy.current_health

        players = [CHARACTER, ENEMY]
        shuffle(players)
        starter = players[0]

        simulate_character_score = 0
        simulate_enemy_score = 0

        while temp_character_health > 0 and temp_enemy_health > 0:
            if simulate_character_score < simulate_enemy_score:
                attacker = CHARACTER
            elif simulate_enemy_score < simulate_character_score:
                attacker = ENEMY
            else:
                attacker = starter

            if attacker == CHARACTER:
                temp_enemy_health -= self.character.damage
                simulate_character_score += 1
                self.battle_log.append((CHARACTER, self.character.damage))
            else:
                temp_character_health -= self.enemy.damage
                simulate_enemy_score += 1
                self.battle_log.append((ENEMY, self.enemy.damage))
        
        self.fight_won = temp_enemy_health <= 0

    def __play_next_animation_step(self):
        if self.current_log_index < len(self.battle_log):
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000

            if elapsed_time >= self.attack_cooldown:
                attacker_type, damage = self.battle_log[self.current_log_index]

                if attacker_type == CHARACTER:
                    self.enemy.current_health -= damage
                else:
                    self.character.current_health -= damage

                self.current_log_index += 1
                self.start_time = pygame.time.get_ticks()
        else:
            self.fight_done = True
    
    def draw(self, canvas, mouse_pos):
        # quest background
        create_rectangle(canvas, 200, 5, 1715, 1070, 0, "cadetblue")

        for button in self.fight_window_button_list:
            button.draw(canvas, mouse_pos)

        # character rect
        create_rectangle(canvas, 300, 250, 370, 400, 5, "blue3")
        create_rectangle(canvas, 305, 255, 360, 390, 0, "black")

        # character health bar
        character_health_width = max(0, self.character.current_health / self.character_health_bar_ratio - 4)
        create_rectangle(canvas, 300, 660, self.health_bar_length, 30, 2, "black")
        create_rectangle(canvas, 302, 662, character_health_width, 26, 0, "red")

        show_text(canvas, f"{self.character.current_health}/{self.character.max_health}", 300 + self.health_bar_length / 2, 660 + 30 / 2, "white", True)

        # character stats
        create_rectangle(canvas, 300, 700, 370, 300, 0, "azure3")
        show_text(canvas, f"Damage: {self.character.damage}", 300 + self.health_bar_length / 2, 720, "azure4", True)

        # Enemy rect
        create_rectangle(canvas, 1445, 250, 370, 400, 5, "blue3")
        create_rectangle(canvas, 1450, 255, 360, 390, 0, "black")

        # enemy health bar
        enemy_health_width = max(0, self.enemy.current_health / self.enemy_health_bar_ratio - 4)
        create_rectangle(canvas, 1445, 660, self.health_bar_length, 30, 2, "black")
        create_rectangle(canvas, 1447, 662, enemy_health_width, 26, 0, "red")

        show_text(canvas, f"{self.enemy.current_health}/{self.enemy.max_health}", 1445 + self.health_bar_length / 2, 660 + 30 / 2, "white", True)

        # enemy stats
        create_rectangle(canvas, 1445, 700, 370, 300, 0, "azure3")
        show_text(canvas, f"Damage: {self.enemy.damage}", 1445 + self.health_bar_length / 2, 720, "azure4", True)

        if not self.start_fight:
            # cooldown before fight 
            self.__inital_start_cooldown()
        else:
            # fight is in progress
            self.__play_next_animation_step()

        if self.fight_done:
            if self.fight_won:
                #self.completed_function()
                print("winner")
            else:
                print("loser")

    def __inital_start_cooldown(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        if elapsed_time >= self.initial_cooldown:
            self.start_fight = True
            self.start_time = pygame.time.get_ticks()

    def handle_events(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.fight_window_button_list:
                    button.click(mouse_pos)
