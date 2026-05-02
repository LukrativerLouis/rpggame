import pygame
from random import shuffle
from utils import *
from character import *

class Fight_Window:
    def __init__(self, gold, experience, item, enemy, character: Character, settings, completed_function, completed_function_winning):
        # init stuff
        self.start_fight = False
        self.settings = settings
        self.gold = gold
        self.experience = experience
        self.item = item
        self.fight_window_button_list = self.__create_fight_window_button()
        self.button_continue = None
        self.character = character
        self.enemy: Enemy = enemy
        self.reward_rewarded = False

        # ui
        self.health_bar_length = 370
        self.character_visual_health = self.character.current_health
        self.enemy_visual_health = self.enemy.current_health
        self.character_health_bar_ratio = self.character.max_health / self.health_bar_length
        self.enemy_health_bar_ratio = self.enemy.max_health / self.health_bar_length

        # time stuff
        self.initial_cooldown = 0.5
        self.attack_cooldown = 1
        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = pygame.time.get_ticks()

        # fight states
        self.fight_won = False
        self.fight_done = False
        self.completed_function = completed_function
        self.completed_function_winning = completed_function_winning

        self.battle_log = []
        self.current_log_index = 0

        self.active_damage_numbers = []

        self.character_fight_window = None
        self.enemy_fight_window = None

        self.__create_player_windows()

        self.__create_fight_done_button()
        self.__simulate_fight()

    def __create_player_windows(self):
        start_time = pygame.time.get_ticks()
        self.character_fight_window = Player_Fight_Window(x = 300, y= 200, image= None, width= 370, height= 400, start_time= start_time, duration= 1.0, border_size= 5, color= "black", border_color= "blue3")
        self.enemy_fight_window = Player_Fight_Window(x=1445, y=200, image=None, width=370, height=400, start_time=start_time, duration=1.0, border_size=5, color="black", border_color="blue3")

    def __execute_completed_functions(self):
        if self.completed_function_winning and self.fight_won:
            self.completed_function_winning()
        self.completed_function()

    def __create_fight_window_button(self):
        button_skip = Button(position = (900, 1025), size = (150, 50), text = self.settings.translate("button_skip_fight"), color = [255, 0, 0], change_color = [255, 50, 50], func = lambda: self.__finish_instantly() )
        button_faster = Button(position = (1250, 1025), size = (150, 50), text = self.settings.translate("button_faster"), color = [255, 0, 0], change_color = [255, 50, 50], func = lambda: self.__adjust_attack_cooldown())
        
        return [button_skip, button_faster]
    
    def __create_fight_done_button(self):
        self.button_continue = Button(position = (900, 1025), size = (150, 50), text = self.settings.translate("button_continue"), color = [255, 0, 0], change_color = [255, 50, 50], func = lambda: self.__execute_completed_functions())
    
    def __finish_instantly(self):
        while self.current_log_index < len(self.battle_log):
            attacker_type, damage, is_crit = self.battle_log[self.current_log_index]

            if attacker_type == CHARACTER:
                self.enemy_visual_health = 0
                self.enemy.current_health -= damage
            else:
                self.character_visual_health = 0
                self.character.current_health -= damage
            self.current_log_index += 1

        self.fight_done = True
    
    def __adjust_attack_cooldown(self):
        self.attack_cooldown *= 0.5

    def __simulate_fight(self):
        self.character.calculate_fighting_stats()
        self.enemy.calculate_fighting_stats()

        temp_character_health = self.character.current_health
        temp_enemy_health = self.enemy.current_health

        players = [CHARACTER, ENEMY]
        starter = None
        if self.character.initiative > self.enemy.initiative:
            starter = CHARACTER
        elif self.character.initiative < self.enemy.initiative:
            starter = ENEMY
        else:
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
                damage, is_crit = calculate_player_damage(self.character, self.enemy)
                temp_enemy_health -= damage
                simulate_character_score += 1
                self.battle_log.append((CHARACTER, damage, is_crit))
            else:
                damage, is_crit = calculate_player_damage(self.enemy, self.character)
                temp_character_health -= damage
                simulate_enemy_score += 1
                self.battle_log.append((ENEMY, damage, is_crit))
        
        self.fight_won = temp_enemy_health <= 0

    def __play_next_animation_step(self):
        if self.current_log_index < len(self.battle_log):
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000

            if elapsed_time >= self.attack_cooldown:
                attacker_type, damage, is_crit = self.battle_log[self.current_log_index]
                character_rect = self.character_fight_window.get_rect()
                enemy_rect = self.enemy_fight_window.get_rect()

                if attacker_type == CHARACTER:

                    self.character_fight_window.start_hit_animation(is_attacker = True, is_character = True)
                    self.enemy_fight_window.start_hit_animation(is_attacker = False, is_character = False)
                    self.enemy.current_health -= damage

                    y_shift = random.randint(-20, 80)

                    damage_number = Damage_Number(damage, enemy_rect.centerx, enemy_rect.centery + y_shift, current_time + 200, duration = self.attack_cooldown, color = "red" if is_crit else "white")
                    self.active_damage_numbers.append(damage_number)
                else:

                    self.enemy_fight_window.start_hit_animation(is_attacker = True, is_character = False)
                    self.character_fight_window.start_hit_animation(is_attacker = False, is_character = True)
                    self.character.current_health -= damage

                    y_shift = random.randint(-20, 80)
                    damage_number = Damage_Number(damage, character_rect.centerx, character_rect.centery + y_shift, current_time + 200, duration = self.attack_cooldown, color = "red" if is_crit else "white")
                    self.active_damage_numbers.append(damage_number)

                self.current_log_index += 1
                self.start_time = pygame.time.get_ticks()
        else:
            self.fight_done = True
            self.fight_won = self.character.current_health > self.enemy.current_health

    def draw_damage_numbers(self, canvas):
        current_time = pygame.time.get_ticks()

        for damage_number in self.active_damage_numbers:
            if damage_number.is_finished(current_time):
                self.active_damage_numbers.remove(damage_number)
            else:
                damage_number.update(current_time)
                show_text(canvas, damage_number.damage, damage_number.x, damage_number.y, damage_number.color, True, 30)
    
    def draw(self, canvas, mouse_pos):
        current_time = pygame.time.get_ticks()

        self.character_fight_window.update_hit_animation(current_time)
        self.enemy_fight_window.update_hit_animation(current_time)

        character_rect_x = 300
        enemy_rect_x = 1445
        player_rect_width = 370

        base_y = 200
        health_bar_offset = 410
        stats_offset = 450

        health_bar_height = 30
        health_bar_border = 2

        # quest background
        create_rectangle(canvas, 200, 5, 1715, 1070, 0, "cadetblue")

        # buttons
        if self.fight_done:
            self.button_continue.draw(canvas, mouse_pos)
        else:
            for button in self.fight_window_button_list:
                button.draw(canvas, mouse_pos)

        # character rect
        self.character_fight_window.draw(canvas, mouse_pos)

        dt = (current_time - self.last_frame_time) / 1000.0
        self.last_frame_time = current_time

        ANIMATION_DURATION = 3

        character_constant_speed = self.character.max_health / ANIMATION_DURATION
        enemy_constant_speed = self.enemy.max_health / ANIMATION_DURATION

        # Character health Animation
        if self.character_visual_health > self.character.current_health:
            self.character_visual_health -= character_constant_speed * dt
            if self.character_visual_health < self.character.current_health:
                self.character_visual_health = self.character.current_health
        elif self.character_visual_health < self.character.current_health:
            self.character_visual_health = self.character.current_health

        # Enemy health Animation
        if self.enemy_visual_health > self.enemy.current_health:
            self.enemy_visual_health -= enemy_constant_speed * dt
            if self.enemy_visual_health < self.enemy.current_health:
                self.enemy_visual_health = self.enemy.current_health
        elif self.enemy_visual_health < self.enemy.current_health:
            self.enemy_visual_health = self.enemy.current_health

        self.character_visual_health = draw_health_bar(
            canvas,
            character_rect_x,
            base_y + health_bar_offset,
            self.character_visual_health,
            self.character.current_health,
            self.character.max_health,
            self.health_bar_length,
            health_bar_height,
            health_bar_border,
        )

        # character stats
        character_stats_y = base_y + stats_offset
        create_rectangle(canvas, character_rect_x, character_stats_y, player_rect_width, 300, 0, "azure3")
        show_text(canvas, f"{self.settings.translate("stat_strength")}: {self.character.strength}", 300 + self.health_bar_length / 2, character_stats_y + 20, "azure4", True)
        show_text(canvas, f"{self.settings.translate("stat_dexterity")}: {self.character.dexterity}", 300 + self.health_bar_length / 2, character_stats_y + 40, "azure4", True)
        show_text(canvas, f"{self.settings.translate("stat_endurance")}: {self.character.endurance}", 300 + self.health_bar_length / 2, character_stats_y + 60, "azure4", True)
        show_text(canvas, f"{self.settings.translate("stat_precision")}: {self.character.precision}", 300 + self.health_bar_length / 2, character_stats_y + 80, "azure4", True)

        # Enemy rect
        self.enemy_fight_window.draw(canvas, mouse_pos)

        self.enemy_visual_health = draw_health_bar(
            canvas,
            enemy_rect_x,
            base_y + health_bar_offset,
            self.enemy_visual_health,
            self.enemy.current_health,
            self.enemy.max_health,
            self.health_bar_length,
            health_bar_height,
            health_bar_border,
        )

        # enemy stats
        enemy_stats_y = base_y + stats_offset
        create_rectangle(canvas, enemy_rect_x, enemy_stats_y, player_rect_width, 300, 0, "azure3")
        show_text(canvas, f"{self.settings.translate("stat_strength")}: {self.enemy.strength}", enemy_rect_x + self.health_bar_length / 2, enemy_stats_y + 20, "azure4", True)
        show_text(canvas, f"{self.settings.translate("stat_dexterity")}: {self.enemy.dexterity}", enemy_rect_x + self.health_bar_length / 2, enemy_stats_y + 40, "azure4", True)
        show_text(canvas, f"{self.settings.translate("stat_endurance")}: {self.enemy.endurance}", enemy_rect_x + self.health_bar_length / 2, enemy_stats_y + 60, "azure4", True)
        show_text(canvas, f"{self.settings.translate("stat_precision")}: {self.enemy.precision}", enemy_rect_x + self.health_bar_length / 2, enemy_stats_y + 80, "azure4", True)

        if not self.start_fight:
            # cooldown before fight 
            self.__inital_start_cooldown()
        else:
            # fight is in progress
            self.__play_next_animation_step()
        
        self.draw_damage_numbers(canvas)

        if self.fight_done:
            # fight end base
            create_rectangle(canvas, character_rect_x + player_rect_width + 20, character_stats_y, 735, 300, 0, "darkgray")

            if self.fight_won:
                show_text(canvas, self.settings.translate("message_won"), character_rect_x + player_rect_width + 20 + 735 / 2, character_stats_y + 20, "darkgoldenrod1", True)
                show_text(canvas, f"{self.settings.translate("experience")}: {self.experience}", character_rect_x + player_rect_width + 20 + 735 / 2, character_stats_y + 40, "darkgoldenrod1", True)
                show_text(canvas, f"{self.settings.translate("gold")}:: {self.gold}", character_rect_x + player_rect_width + 20 + 735 / 2, character_stats_y + 60, "darkgoldenrod1", True)
                if not self.reward_rewarded:
                    self.character.adjust_gold_and_exp(self.gold, self.experience)
                    self.reward_rewarded = True
                    
            else:
                show_text(canvas, self.settings.translate("message_lost"), character_rect_x + player_rect_width + 20 + 735 / 2, character_stats_y + 20, "darkgoldenrod1", True)

    def __inital_start_cooldown(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        if elapsed_time >= self.initial_cooldown:
            self.start_fight = True
            self.start_time = pygame.time.get_ticks()

    def handle_events(self, event, mouse_pos):
        if self.fight_done:
            self.button_continue.handle_event(event, mouse_pos)
        else:
            for button in self.fight_window_button_list:
                button.handle_event(event, mouse_pos)


class Player_Fight_Window:
    def __init__(self, x, y, image, width, height, start_time, duration, border_size, color, border_color):
        self.x = x
        self.y = y
        self.original_x = x
        self.image = image
        self.width = width
        self.height = height
        self.start_time = start_time
        self.duration = duration
        self.border_size = border_size
        self.color = color 
        self.border_color = border_color

        self.is_hit_animating = False
        self.hit_start_time = 0
        self.hit_duration = 0.3
        self.hit_distance = 40
        self.is_attacker = False
        self.is_character = False

    def start_hit_animation(self, is_attacker = False, is_character = False):
        self.is_hit_animating = True
        self.hit_start_time = pygame.time.get_ticks()
        self.is_attacker = is_attacker
        self.is_character = is_character

    def update_hit_animation(self, current_time):
        if not self.is_hit_animating:
            return False
        
        elapsed = (current_time - self.hit_start_time) / 1000.0
        progress = min(elapsed / self.hit_duration, 1.0)

        direction = 1 if self.is_character else -1
        
        if self.is_attacker:
            if progress < 0.5:
                move_progress = progress * 2
                self.x = self.original_x + (self.hit_distance * move_progress * direction)
            else:
                move_progress = (progress - 0.5) * 2
                self.x = self.original_x + (self.hit_distance * (1 - move_progress) * direction)
        else:
            pass

        if progress >= 1.0:
            self.is_hit_animating = False
            self.x = self.original_x
            return False
        
        return True
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, canvas, mouse_pos):
        current_rect = self.get_rect()

        pygame.draw.rect(canvas, self.border_color, current_rect, self.border_size)

        inner_rect = pygame.Rect(current_rect.x + self.border_size, current_rect.y + self.border_size, current_rect.width - self.border_size * 2, current_rect.height - self.border_size * 2)
        pygame.draw.rect(canvas, self.color, inner_rect)
    
    def update(self, current_time):
        elapsed = (current_time - self.start_time) / 1000.0
        progress = min(elapsed / self.duration, 1.0)

        return progress < 1.0


class Damage_Number:
    def __init__(self, damage, x, y, start_time, duration, color):
        self.damage = damage
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.start_time = start_time
        self.duration = duration
        self.x_shift = random.randint(-10, 10)
        self.alpha = 255
    
    def update(self, current_time):
        elapsed = (current_time - self.start_time) / 1000.0
        progress = min(elapsed / self.duration, 1.0)
        
        self.y = self.start_y - (progress * 30)
        self.x = self.start_x - (progress * self.x_shift)
        
        self.alpha = int(255 * (1 - progress))
        
        return progress < 1.0
    
    def is_finished(self, current_time):
        elapsed = (current_time - self.start_time) / 1000.0
        return elapsed >= self.duration
