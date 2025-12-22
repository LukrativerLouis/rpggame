import pygame

pygame.font.init()
font = pygame.font.Font(None, 30)

def debug(info, y, x, color):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, color)
    debug_rect = debug_surf.get_rect(topleft=(x, y))

    display_surface.blit(debug_surf, debug_rect)

def show_text(info, y= 100, x= 100, color= "Green"):
    debug(info, y, x, color)