import pygame

class Button:
    def __init__(self, position, size, color=[100, 100, 100], change_color=None, func=None, text='', font="arial", font_size=16, font_color=[0, 0, 0]):
        self.center_pos = pygame.Vector2(position)
        self.size_original = pygame.Vector2(size)
        self.color = color
        if change_color is None:
            self.change_color = self._generate_hover_color(self.color)
        else:
            self.change_color = change_color
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

    def _generate_hover_color(self, color):
        brightness = sum(color[:3]) / 3
        
        if brightness > 200:
            return [max(0, c - 40) for c in color]
        else:
            return [min(255, c + 40) for c in color]

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

    def set_function(self, new_func):
        self.func = new_func

    def set_pos(self, new_pos):
        self.center_pos = pygame.Vector2(new_pos)
        self.rect.center = new_pos

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

def draw_health_bar(canvas, x, y, visual_val, actual_val, max_val, bar_width, bar_height, border_value):
    ratio = bar_width / max_val if max_val > 0 else 0

    yellow_width = visual_val * ratio
    red_width = actual_val * ratio

    border = create_rectangle(canvas, x, y, bar_width, bar_height, border_value, "black")

    if yellow_width > 0:
        w = max(0, yellow_width - border_value * 2)
        create_rectangle(canvas, x + border_value, y + border_value, w, bar_height - border_value * 2, 0, "yellow")

    if red_width > 0:
        w = max(0, red_width - border_value * 2)
        create_rectangle(canvas, x + border_value, y + border_value, w, bar_height - border_value * 2, 0, "red")

    show_text(canvas, f"{int(actual_val)}/{int(max_val)}", border.centerx, border.centery, "white", True)

    return visual_val

def draw_progression_bar(canvas, x, y, actual_val, max_val, bar_width, bar_height, border_value, bar_color_string = "red", border_color = "black", text_color = "white", extra_text = None):
    ratio = bar_width / max_val if max_val > 0 else 0

    red_width = actual_val * ratio

    border = create_rectangle(canvas, x, y, bar_width, bar_height, border_value, border_color)

    if red_width > 0:
        w = max(0, red_width - border_value * 2)
        create_rectangle(canvas, x + border_value, y + border_value, w, bar_height - border_value * 2, 0, bar_color_string)

    if extra_text:
        show_text(canvas, f"{extra_text}: {int(actual_val)}/{int(max_val)}", border.centerx, border.centery, text_color, True)
    else:
        show_text(canvas, f"{int(actual_val)}/{int(max_val)}", border.centerx, border.centery, text_color, True)

class SliderToggle:
    def __init__(self, pos, size, font, label, initial_state=False, on_toggle=None, bg_on = "green", bg_off = "red", knob_color = "white", text_color = "black"):
        self.font = font
        self.label = label
        self.state = initial_state
        self.on_toggle = on_toggle

        self.width, self.height = size
        self.center_x, self.center_y = pos

        self.anim_progress = 1.0 if self.state else 0.0
        self.anim_speed = 0.15

        self.bg_on = pygame.Color(bg_on)
        self.bg_off = pygame.Color(bg_off)
        self.knob_color = pygame.Color(knob_color)
        self.text_color = pygame.Color(text_color)

        self.text_surface = self.font.render(self.label, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        
        spacing = 20

        total_width = self.text_rect.width + spacing + self.width
        left_edge = self.center_x - total_width // 2

        self.text_rect.midleft = (left_edge, self.center_y)

        self.slider_rect = pygame.Rect(
            self.text_rect.right + spacing,
            self.center_y - self.height // 2,
            self.width,
            self.height
        )
        self.knob_radius = self.height // 2 - 4

    def toggle(self):
        self.state = not self.state
        if self.on_toggle:
            self.on_toggle(self.state)

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and self.slider_rect.collidepoint(mouse_pos):
            self.toggle()

    def update(self, pos):
        target = 1.0 if self.state else 0.0
        if self.anim_progress < target:
            self.anim_progress = min(self.anim_progress + self.anim_speed, target)
        elif self.anim_progress > target:
            self.anim_progress = max(self.anim_progress - self.anim_speed, target)
        
        self.center_x, self.center_y = pos

    def draw(self, screen):
        # Text
        screen.blit(self.text_surface, self.text_rect)

        # Hintergrund des Sliders
        bg_color = self.bg_on.lerp(self.bg_off, 1.0 - self.anim_progress)
        pygame.draw.rect(screen, bg_color, self.slider_rect, border_radius=self.height // 2)

        # Knopf
        knob_x = self.slider_rect.left + int(self.anim_progress * (self.width - self.height)) + self.height // 2
        knob_center = (knob_x, self.slider_rect.centery)
        pygame.draw.circle(screen, self.knob_color, knob_center, self.knob_radius)

    def get_state(self):
        return self.state

class VolumeSlider:
    def __init__(self, center_pos, size, font, label, initial_value=50, on_change=None, text_color = "black", slider_color = "white", slider_picker_color = "black"):
        self.center_x, self.y = center_pos
        self.slider_width, self.slider_height = size
        self.font = font
        self.label = label
        self.value = initial_value  # 0 - 100
        self.on_change = on_change
        self.text_color = text_color
        self.slider_color = slider_color
        self.slider_picker_color = slider_picker_color
        self.dragging = False

        self.label_surface = self.font.render(self.label, True, self.text_color)
        self.label_rect = self.label_surface.get_rect()

        self.total_width = self.label_rect.width + 20 + self.slider_width + 40

        self.x = self.center_x - self.total_width // 2

        self._recalculate_rects()

    def _recalculate_rects(self):
        self.label_rect.topleft = (self.x, self.y)

        self.slider_x = self.label_rect.right + 20
        self.slider_y = self.y + self.label_rect.height // 2 - self.slider_height // 2
        self.handle_rect = pygame.Rect(
            self.slider_x + (self.slider_width * self.value / 100),
            self.slider_y,
            10,
            self.slider_height
        )

    def set_position(self, center_pos):
        self.center_x, self.y = center_pos
        self.x = self.center_x - self.total_width // 2
        self._recalculate_rects()

    def draw(self, surface):
        surface.blit(self.label_surface, self.label_rect)

        pygame.draw.rect(
            surface,
            self.slider_color,
            (self.slider_x, self.slider_y + self.slider_height // 2 - 3, self.slider_width, 6),
            border_radius=3
        )

        pygame.draw.rect(surface, self.slider_picker_color, self.handle_rect)

        value_surface = self.font.render(f"{self.value}", True, self.slider_picker_color)
        surface.blit(value_surface, (self.slider_x + self.slider_width + 15, self.slider_y - 2))

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(mouse_pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = min(max(mouse_pos[0], self.slider_x), self.slider_x + self.slider_width)
            self.handle_rect.x = new_x
            self.value = int(((self.handle_rect.x - self.slider_x) / self.slider_width) * 100)
            if self.on_change:
                self.on_change(self.value)

def get_font(size):
    return pygame.font.Font(None, size)

class Text_Input_Box():
    def __init__(self, x, y, width, height, background_color, border_color, text_color, label_text = None, label_color = "white", focused_color = "green"):
        self.text = ""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background_color = background_color
        self.border_color = border_color
        self.text_color = text_color
        self.label_text = label_text
        self.label_color = label_color
        self.focused_color = focused_color
        self.focused = False
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def clear(self):
        self.text = ""

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.background_color, self.rect)
        pygame.draw.rect(canvas, self.border_color, self.rect, 2)
        show_text(canvas, self.text, self.rect.centerx, self.rect.centery, self.text_color, True)
        if self.label_text:
            show_text(canvas, self.label_text, self.rect.x + 2, self.rect.y - 30, self.label_color, False)
        if self.focused:
            pygame.draw.rect(canvas, self.focused_color, self.rect, 4)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
            self.focused = not self.focused
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.rect.collidepoint(mouse_pos):
            self.focused = False

        if self.focused:
            if event.type == pygame.TEXTINPUT and len(self.text) <= 20:
                self.text += event.text

            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
