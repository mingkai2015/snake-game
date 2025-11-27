import pygame
from . import settings

# Initialize pixel art font dictionary
PIXEL_FONT_DATA = {
    'A': [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
    'B': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,1,0]],
    'C': [[0,1,1],[1,0,0],[1,0,0],[1,0,0],[0,1,1]],
    'D': [[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,1,0]],
    'E': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,1,1]],
    'F': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,0,0]],
    'G': [[0,1,1],[1,0,0],[1,0,1],[1,0,1],[0,1,1]],
    'H': [[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
    'I': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[1,1,1]],
    'J': [[0,0,1],[0,0,1],[0,0,1],[1,0,1],[0,1,0]],
    'K': [[1,0,1],[1,0,1],[1,1,0],[1,0,1],[1,0,1]],
    'L': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
    'M': [[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]],
    'N': [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]], 
    'O': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    'P': [[1,1,0],[1,0,1],[1,1,0],[1,0,0],[1,0,0]],
    'Q': [[0,1,0],[1,0,1],[1,0,1],[1,1,0],[0,0,1]],
    'R': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,0,1]],
    'S': [[0,1,1],[1,0,0],[0,1,0],[0,0,1],[1,1,0]],
    'T': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
    'U': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
    'V': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    'W': [[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,0,1]],
    'X': [[1,0,1],[0,1,0],[0,1,0],[0,1,0],[1,0,1]],
    'Y': [[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0]],
    'Z': [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1]],
    ' ': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    '1': [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[1,1,1]],
    '2': [[0,1,0],[1,0,1],[0,0,1],[0,1,0],[1,1,1]],
    '3': [[1,1,0],[0,0,1],[0,1,0],[0,0,1],[1,1,0]],
    '4': [[1,0,0],[1,0,0],[1,0,1],[1,1,1],[0,0,1]],
    '5': [[1,1,1],[1,0,0],[1,1,0],[0,0,1],[1,1,0]],
    '6': [[0,1,1],[1,0,0],[1,1,0],[1,0,1],[0,1,0]],
    '7': [[1,1,1],[0,0,1],[0,0,1],[0,1,0],[0,1,0]],
    '8': [[0,1,0],[1,0,1],[0,1,0],[1,0,1],[0,1,0]],
    '9': [[0,1,0],[1,0,1],[0,1,1],[0,0,1],[0,1,0]],
    '0': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    ':': [[0,0,0],[0,1,0],[0,0,0],[0,1,0],[0,0,0]],
    '-': [[0,0,0],[0,0,0],[1,1,1],[0,0,0],[0,0,0]],
    '|': [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
}

class PixelFont:
    def __init__(self, scale=2):
        self.scale = scale
        self.char_w = 3
        self.char_h = 5
        self.spacing = 1
        
    def render(self, text, antialias, color):
        text = text.upper()
        width = 0
        for char in text:
            width += (self.char_w + self.spacing) * self.scale
        
        height = self.char_h * self.scale
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        
        current_x = 0
        for char in text:
            if char in PIXEL_FONT_DATA:
                grid = PIXEL_FONT_DATA[char]
                for r, row in enumerate(grid):
                    for c, pixel in enumerate(row):
                        if pixel:
                            pygame.draw.rect(s, color, (current_x + c * self.scale, r * self.scale, self.scale, self.scale))
            current_x += (self.char_w + self.spacing) * self.scale
            
        return s

    def size(self, text):
        text = text.upper()
        width = 0
        for char in text:
            width += (self.char_w + self.spacing) * self.scale
        height = self.char_h * self.scale
        return (width, height)

class Button:
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False

    def draw(self, surface):
        color = settings.BUTTON_HOVER_COLOR if self.hovered else settings.BUTTON_COLOR
        
        pygame.draw.rect(surface, (60, 30, 10), (self.rect.x, self.rect.y + 5, self.rect.width, self.rect.height), border_radius=10)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (160, 90, 40), self.rect, 3, border_radius=10)
        
        text_surf = self.font.render(self.text, True, settings.TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.action:
                self.action()

class FontManager:
    @staticmethod
    def load_fonts():
        font = None
        title_font = None
        
        try:
            if not pygame.font.get_init():
                pygame.font.init()
                
            font_path = pygame.font.match_font('arial')
            if font_path:
                font = pygame.font.Font(font_path, 30)
                title_font = pygame.font.Font(font_path, 60)
            else:
                raise Exception("Font match failed")
        except Exception as e:
            print(f"Warning: Primary font loading failed ({e}). Using PixelFont fallback.")
            font = PixelFont(scale=3)
            title_font = PixelFont(scale=6)
            
        return font, title_font

