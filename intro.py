import pygame
from settings import *

class Intro:
    def __init__(self):
        self.set_target_size = (256, 256)
        self.image_list = []
        self.load_images()

        self.start_time = pygame.time.get_ticks()
        self.frame_duration = 150

        # rotations
        self.rotations_done = 0
        self.max_rotations = 2

        # states
        self.animation_finished = False
        # CHANGE TO SHOW INTRO
        self.fade_out_complete = True
        self.wait_duration = 500

        self.alpha = 0
        self.fade_speed = 2

        self.font_size = 30
        self.font = pygame.font.Font(PIXELIFY_FONT_PATH, self.font_size)
        self.text_surface = self.font.render("lucrative games", True, (255, 255, 255))

    def load_images(self):
        for i in range(1, 6):
            img = pygame.image.load(f"assets/intro/coin{i}.png").convert_alpha()
            scale_img = pygame.transform.scale(img, self.set_target_size)
            self.image_list.append(scale_img)

    def draw(self, canvas, x, y):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time

        fade_duration = 1000
        total_anim_duration = self.frame_duration * len(self.image_list) * self.max_rotations

        if not self.animation_finished:
            self.alpha = min(255, int((elapsed / fade_duration) * 255))
            
            idx = (elapsed // self.frame_duration) % len(self.image_list)
            
            if elapsed >= total_anim_duration:
                self.animation_finished = True
                self.end_time = now
        
        elif now - self.end_time < self.wait_duration:
            self.alpha = 255
            idx = 0 
            
        else:
            fade_out_elapsed = now - (self.end_time + self.wait_duration)
            self.alpha = max(0, 255 - int((fade_out_elapsed / fade_duration) * 255))
            idx = 0
            
            if self.alpha <= 0:
                self.fade_out_complete = True

        img = self.image_list[idx].copy()
        img.set_alpha(self.alpha)
        
        temp_text = self.text_surface.copy()
        temp_text.set_alpha(self.alpha)

        canvas.blit(img, img.get_rect(center=(x, y)))
        canvas.blit(temp_text, temp_text.get_rect(center=(x, y + 100)))