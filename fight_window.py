import pygame
from random import shuffle
from utils import *
from character import *
from quest import *

class Fight_Window:
    def __init__(self, gold, experience, item, enemy, character: Character, completed_function, allow_retry):
        # init stuff
        self.start_fight = False
        self.gold = gold
        self.experience = experience
        self.item = item
        self.fight_window_button_list = self.__create_fight_window_button()
        self.button_continue = None
        self.button_retry = None
        self.allow_retry = allow_retry
        self.character = character
        self.enemy: Enemy = enemy

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

        self.__create_fight_done_button()
        self.__simulate_fight()

    def __create_fight_window_button(self):
        button_skip = Button(position = (900, 1025), size = (150, 50), text = "skip fight", color = [255, 0, 0], change_color = [255, 50, 50], func = lambda: self.__finish_instantly() )
        button_faster = Button(position = (1250, 1025), size = (150, 50), text = "faster", color = [255, 0, 0], change_color = [255, 50, 50], func = lambda: self.__adjust_attack_cooldown())
        
        return [button_skip, button_faster]
    
    def __create_fight_done_button(self):
        self.button_continue = Button(position = (690 + 735 / 2, 1025), size = (150, 50), text = "continue", color = [255, 0, 0], change_color = [255, 50, 50], func = lambda: self.completed_function())
        if not self.allow_retry:
            self.button_continue.center_pos = (900, 1025)
        self.button_retry = Button(position = (1250, 1025), size = (150, 50), text = "retry", color = [255, 0, 0], change_color = [255, 50, 50])
    
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
            self.fight_won = self.character.current_health > self.enemy.current_health
    
    def draw(self, canvas, mouse_pos):

        character_rect_x = 300
        enemy_rect_x = 1445
        player_rect_width = 370

        base_y = 200
        health_bar_offset = 410
        stats_offset = 450

        player_rect_border = 5
        player_health_bar_width = 2
        player_rect_height = 400

        # quest background
        create_rectangle(canvas, 200, 5, 1715, 1070, 0, "cadetblue")

        # buttons
        if self.fight_done:
            self.button_continue.draw(canvas, mouse_pos)
            if not self.fight_won and self.allow_retry:
                self.button_retry.draw(canvas, mouse_pos)
        else:
            for button in self.fight_window_button_list:
                button.draw(canvas, mouse_pos)

        # character rect
        create_rectangle(canvas, character_rect_x, base_y, player_rect_width, player_rect_height, player_rect_border, "blue3")
        create_rectangle(canvas, character_rect_x + player_rect_border, base_y + player_rect_border, player_rect_width - player_rect_border * 2, player_rect_height - player_rect_border * 2, 0, "black")

        # character health bar
        character_health_y = base_y + health_bar_offset
        character_health_width = max(0, self.character.current_health / self.character_health_bar_ratio - player_health_bar_width * 2)
        create_rectangle(canvas, character_rect_x, character_health_y, self.health_bar_length, 30, player_health_bar_width, "black")
        create_rectangle(canvas, character_rect_x + player_health_bar_width, character_health_y + player_health_bar_width, character_health_width, 26, 0, "red")
        show_text(canvas, f"{self.character.current_health}/{self.character.max_health}", 300 + self.health_bar_length / 2, character_health_y + 30 / 2, "white", True)

        # character stats
        character_stats_y = base_y + stats_offset
        create_rectangle(canvas, character_rect_x, character_stats_y, player_rect_width, 300, 0, "azure3")
        show_text(canvas, f"Damage: {self.character.damage}", 300 + self.health_bar_length / 2, character_stats_y + 20, "azure4", True)

        # Enemy rect
        create_rectangle(canvas, enemy_rect_x, base_y, player_rect_width, player_rect_height, player_rect_border, "blue3")
        create_rectangle(canvas, enemy_rect_x + player_rect_border, base_y + player_rect_border, player_rect_width - player_rect_border * 2, player_rect_height - player_rect_border * 2, 0, "black")

        # enemy health bar
        enemy_health_y = base_y + health_bar_offset
        enemy_health_width = max(0, self.enemy.current_health / self.enemy_health_bar_ratio - player_health_bar_width * 2)
        create_rectangle(canvas, enemy_rect_x, enemy_health_y, self.health_bar_length, 30, 2, "black")
        create_rectangle(canvas, enemy_rect_x + player_health_bar_width, enemy_health_y + player_health_bar_width, enemy_health_width, 26, 0, "red")
        show_text(canvas, f"{self.enemy.current_health}/{self.enemy.max_health}", enemy_rect_x + self.health_bar_length / 2, enemy_health_y + 30 / 2, "white", True)

        # enemy stats
        enemy_stats_y = base_y + stats_offset
        create_rectangle(canvas, enemy_rect_x, enemy_stats_y, player_rect_width, 300, 0, "azure3")
        show_text(canvas, f"Damage: {self.enemy.damage}", enemy_rect_x + self.health_bar_length / 2, enemy_stats_y + 20, "azure4", True)

        if not self.start_fight:
            # cooldown before fight 
            self.__inital_start_cooldown()
        else:
            # fight is in progress
            self.__play_next_animation_step()

        if self.fight_done:
            # fight end base
            create_rectangle(canvas, character_rect_x + player_rect_width + 20, character_stats_y, 735, 300, 0, "darkgray")

            if self.fight_won:
                show_text(canvas, "You won!", character_rect_x + player_rect_width + 20 + 735 / 2, character_stats_y + 20, "darkgoldenrod1", True)
                show_text(canvas, f"Experience: {self.experience}", character_rect_x + player_rect_width + 20 + 735 / 2, character_stats_y + 40, "darkgoldenrod1", True)
                show_text(canvas, f"Gold: {self.gold}", character_rect_x + player_rect_width + 20 + 735 / 2, character_stats_y + 60, "darkgoldenrod1", True)
            else:
                show_text(canvas, "You lost!", character_rect_x + player_rect_width + 20 + 735 / 2, character_stats_y + 20, "darkgoldenrod1", True)

    def __inital_start_cooldown(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        if elapsed_time >= self.initial_cooldown:
            self.start_fight = True
            self.start_time = pygame.time.get_ticks()

    def handle_events(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.fight_done:
                    self.button_continue.click(mouse_pos)
                    if not self.fight_won and self.allow_retry:
                        self.button_retry.click(mouse_pos)
                else:
                    for button in self.fight_window_button_list:
                        button.click(mouse_pos)
                
