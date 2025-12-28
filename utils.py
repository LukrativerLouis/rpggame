import pygame

class Button:
    def __init__(self, position, size, color=[100, 100, 100], change_color=None, func=None, text='', font="arial", font_size=16, font_color=[0, 0, 0]):
        self.color = color
        self.size_original = size
        self.size = size
        self.func = func
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=position)
        self.center_pos = position

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

        self.update_text_position()
        
        self.current_color = self.color

        self.is_clicked = False
        self.click_timer = 0
        self.shrink_scale = 0.96

    def update_text_position(self):
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

    def draw(self, surface, mouse_pos):
        self.update_animation()
        self.check_mouseover(mouse_pos)

        ratio = self.size[0] / self.size_original[0]

        draw_surf = pygame.Surface(self.size).convert_alpha() 
        draw_surf.fill(self.current_color)

        scaled_txt_w = int(self.txt_surf.get_width() * ratio)
        scaled_txt_h = int(self.txt_surf.get_height() * ratio)
        
        scaled_txt_surf = pygame.transform.smoothscale(self.txt_surf, (scaled_txt_w, scaled_txt_h))

        scaled_txt_rect = scaled_txt_surf.get_rect(center=(self.size[0] // 2, self.size[1] // 2))

        draw_surf.blit(scaled_txt_surf, scaled_txt_rect)
        surface.blit(draw_surf, self.rect)

    def check_mouseover(self, pos):
        if not self.is_clicked:
            self.current_color = self.color
            if self.rect.collidepoint(pos):
                self.current_color = self.change_color

    def click(self, pos, *args):
        if self.rect.collidepoint(pos):
            self.animate_click()
            if self.func:
                return self.func(*args)
            
    def animate_click(self):
        self.is_clicked = True
        self.click_timer = pygame.time.get_ticks()

        # Calculate new shrunk size
        new_width = int(self.size_original[0] * self.shrink_scale)
        new_height = int(self.size_original[1] * self.shrink_scale)
        self.size = (new_width, new_height)
        
        # Important: Re-center the rect so it shrinks to middle, not top-left
        self.surf = pygame.transform.scale(self.surf, self.size)
        self.rect = self.surf.get_rect(center=self.center_pos)
        self.update_text_position()

    def update_animation(self):
        if self.is_clicked:
            if pygame.time.get_ticks() - self.click_timer > 100:
                self.is_clicked = False
                self.size = self.size_original
                self.surf = pygame.transform.scale(self.surf, self.size)
                self.rect = self.surf.get_rect(center = self.center_pos)
                self.update_text_position()

def create_rectangle(canvas, x, y, width, height, thickness, color = "black"):
    """
    canvas is the screen or surface to draw on -
    color is the color of the rectangle standard is black -
    x is the horizontal left and right -
    y is vertical up and down -
    width in pixel -
    height in pixel -
    thickness 0 is filled after that its thickness of the border
    """

    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(canvas, color, rect, thickness)

pygame.font.init()
font = pygame.font.SysFont("arial", 20)

def debug(canvas, info, y, x, color, center = False):

    debug_surf = font.render(str(info), True, color)

    if center:
        debug_rect = debug_surf.get_rect(center=(x, y))
    else:
        debug_rect = debug_surf.get_rect(topleft=(x, y))

    canvas.blit(debug_surf, debug_rect)

def show_text(canvas, info, y= 100, x= 100, color= "Green", center = False):
    debug(canvas, info, y, x, color, center)
