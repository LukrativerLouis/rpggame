import pygame

pygame.font.init()
font = pygame.font.SysFont("arial", 20)

def debug(canvas, info, y, x, color):

    debug_surf = font.render(str(info), True, color)
    debug_rect = debug_surf.get_rect(topleft=(x, y))

    canvas.blit(debug_surf, debug_rect)

def show_text(canvas, info, y= 100, x= 100, color= "Green"):
    debug(canvas, info, y, x, color)

