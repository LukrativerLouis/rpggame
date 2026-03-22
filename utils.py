import pygame

import pygame

class Button:
    def __init__(self, position, size, color=[100, 100, 100], change_color=None, func=None, text='', font="arial", font_size=16, font_color=[0, 0, 0]):
        self.center_pos = pygame.Vector2(position)
        self.size_original = pygame.Vector2(size)
        self.color = color
        self.change_color = change_color if change_color else color
        self.func = func
        
        self.is_pressed = False
        self.is_hovered = False
        
        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_color = font_color
        self.txt_surf = self.font.render(self.txt, True, self.font_color)
        
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = position
        
        self.shrink_scale = 0.95

    def handle_event(self, event, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_pressed and self.is_hovered and self.func:
                    self.func()
                self.is_pressed = False

    def draw(self, surface, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.change_color if self.is_hovered else self.color
        
        scale = self.shrink_scale if self.is_pressed else 1.0
        current_w = int(self.size_original.x * scale)
        current_h = int(self.size_original.y * scale)
        
        draw_surf = pygame.Surface((current_w, current_h)).convert_alpha()
        draw_surf.fill(current_color)
        
        if len(current_color) == 4:
            draw_surf.set_alpha(current_color[3])

        text_w = int(self.txt_surf.get_width() * scale)
        text_h = int(self.txt_surf.get_height() * scale)
        scaled_txt = pygame.transform.smoothscale(self.txt_surf, (text_w, text_h))
        
        text_rect = scaled_txt.get_rect(center=(current_w // 2, current_h // 2))
        draw_surf.blit(scaled_txt, text_rect)

        draw_rect = draw_surf.get_rect(center=self.center_pos)
        surface.blit(draw_surf, draw_rect)

    def set_text(self, new_text):
        if self.txt != new_text:
            self.txt = new_text
            self.txt_surf = self.font.render(self.txt, True, self.font_color)

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
    return pygame.draw.rect(canvas, color, rect, thickness)

def create_tooltip(canvas, x, y, width, height, text, text_color, color = "black"):
    create_rectangle(canvas, x, y, width, height, 0, color)
    show_text(canvas, text, x + width / 2, y + height / 2, text_color, True)

pygame.font.init()
font = pygame.font.SysFont("arial", 20)

def debug(canvas, info, y, x, color, center = False):

    debug_surf = font.render(str(info), True, color)

    if center:
        debug_rect = debug_surf.get_rect(center=(x, y))
    else:
        debug_rect = debug_surf.get_rect(topleft=(x, y))

    canvas.blit(debug_surf, debug_rect)

def show_text(canvas, info, x = 100, y = 100, color= "Green", center = False):
    debug(canvas, info, y, x, color, center)
