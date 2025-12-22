import pygame
from character import *
from settings import *
from debug import *


class Game():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.character = Character()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

    def start(self):

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            show_text("Gold: ")
            

            pygame.display.update()

            self.clock(60)


Game().start()