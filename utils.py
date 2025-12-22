import pygame

class Button:
    def __init__(self, position, size, color=[100, 100, 100], change_color=None, func=None, text='', font="Segoe Print", font_size=16, font_color=[0, 0, 0]):
        self.color = color
        self.size = size
        self.func = func
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=position)

        if change_color:
            self.change_color = change_color
        else:
            self.change_color = color

        if len(color) == 4:
            self.surf.set_alpha(color[3])

        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_color = font_color
        self.txt_surf = self.font.render(self.txt, 1, self.font_color)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])
        
        self.current_color = self.color

    def draw(self, surface, mouse_pos):
        self.check_mouseover(mouse_pos)

        self.surf.fill(self.current_color)
        self.surf.blit(self.txt_surf, self.txt_rect)
        surface.blit(self.surf, self.rect)

    def check_mouseover(self, pos):
        self.current_color = self.color
        if self.rect.collidepoint(pos):
            self.current_color = self.change_color

    def click(self, pos, *args):
        if self.rect.collidepoint(pos):
            if self.func:
                return self.func(*args)
            print(f"Button '{self.txt}' clicked!")

class Text:
    def __init__(self, msg, position, clr=[100, 100, 100], font="Segoe Print", font_size=15, mid=False):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.txt_surf = self.font.render(msg, 1, clr)

        if len(clr) == 4:
            self.txt_surf.set_alpha(clr[3])

        if mid:
            self.position = self.txt_surf.get_rect(center=position)


    def draw(self, screen):
        screen.blit(self.txt_surf, self.position)