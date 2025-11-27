import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 25
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60
MOVE_DELAY = 200  # 200ms (5 moves/sec)

# Colors
BG_COLOR_1 = (124, 181, 31)  # Light grass
BG_COLOR_2 = (113, 168, 26)  # Dark grass
SNAKE_COLOR_1 = (50, 205, 50) # Lime Green
SNAKE_COLOR_2 = (34, 139, 34) # Forest Green
FROZEN_COLOR_1 = (135, 206, 235) # Sky Blue (Frozen)
FROZEN_COLOR_2 = (70, 130, 180)  # Steel Blue
FOOD_COLOR = (255, 69, 0)     # Red-Orange
BOMB_COLOR = (50, 50, 50)     # Dark Grey
BOMB_HIGHLIGHT = (255, 0, 0)  # Red
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (139, 69, 19)  # Wood brown
BUTTON_HOVER_COLOR = (160, 82, 45)

# Fonts
FONT = None
TITLE_FONT = None

# Initialize pixel art font dictionary
PIXEL_FONT = {
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
            if char in PIXEL_FONT:
                grid = PIXEL_FONT[char]
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

class DummyFont:
    def render(self, text, antialias, color):
        width = len(text) * 20
        height = 40
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        return s

    def size(self, text):
        return (len(text) * 20, 40)

try:
    if not pygame.get_init():
        pygame.init()
    if not pygame.font.get_init():
        pygame.font.init()
        
    FONT_PATH = pygame.font.match_font('arial')
    if FONT_PATH:
        FONT = pygame.font.Font(FONT_PATH, 30)
        TITLE_FONT = pygame.font.Font(FONT_PATH, 60)
    else:
        raise Exception("Font match failed")
except Exception as e:
    print(f"Warning: Primary font loading failed ({e}). Using PixelFont fallback.")
    FONT = PixelFont(scale=3)
    TITLE_FONT = PixelFont(scale=6)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        
        pygame.draw.rect(surface, (60, 30, 10), (self.rect.x, self.rect.y + 5, self.rect.width, self.rect.height), border_radius=10)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (160, 90, 40), self.rect, 3, border_radius=10)
        
        text_surf = FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.action:
                self.action()

class Explosion:
    def __init__(self, x, y):
        self.x = x * GRID_SIZE + GRID_SIZE // 2
        self.y = y * GRID_SIZE + GRID_SIZE // 2
        self.particles = []
        for _ in range(20):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.randint(20, 40)
            color = random.choice([(255, 50, 50), (255, 150, 0), (255, 255, 0)])
            self.particles.append({'x': self.x, 'y': self.y, 'vx': vx, 'vy': vy, 'life': life, 'color': color})
        
    def update(self):
        alive = False
        for p in self.particles:
            if p['life'] > 0:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= 1
                alive = True
        return alive
        
    def draw(self, surface):
        for p in self.particles:
            if p['life'] > 0:
                alpha = min(255, p['life'] * 10)
                s = pygame.Surface((4, 4), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p['color'], alpha), (2, 2), 2)
                surface.blit(s, (p['x'] - 2, p['y'] - 2))

class Bomb:
    def __init__(self):
        self.position = (-1, -1)
        self.active = False
    
    def spawn(self, occupied_positions):
        if self.active: return
        pass
            
    def force_spawn(self, occupied_positions):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in occupied_positions:
                self.position = (x, y)
                self.active = True
                break

    def draw(self, surface):
        if not self.active: return
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        # Draw Bomb Body
        c = rect.center
        pygame.draw.circle(surface, (30, 30, 30), c, GRID_SIZE // 2 - 2) # Outline
        pygame.draw.circle(surface, (60, 60, 60), (c[0]-2, c[1]-2), GRID_SIZE // 2 - 4) # Highlight
        
        # Wick
        pygame.draw.line(surface, (150, 100, 50), c, (c[0] + 5, c[1] - 10), 2)
        
        # Spark
        if pygame.time.get_ticks() % 200 < 100:
            spark_pos = (c[0] + 5, c[1] - 10)
            pygame.draw.circle(surface, (255, 255, 0), spark_pos, 4)
            pygame.draw.circle(surface, (255, 50, 0), spark_pos, 2)

class Snake:
    def __init__(self, x, y, color1, color2, controls):
        self.body = [(x, y), (x-1, y), (x-2, y)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.color1 = color1
        self.color2 = color2
        self.original_color1 = color1
        self.original_color2 = color2
        self.controls = controls
        self.grow_pending = 0
        self.alive = True
        self.frozen_timer = 0
        
    def freeze(self, duration_frames):
        self.frozen_timer = duration_frames
        self.color1 = FROZEN_COLOR_1
        self.color2 = FROZEN_COLOR_2
        
    def handle_event(self, event):
        if not self.alive or event.type != pygame.KEYDOWN: return
        
        new_dir = None
        if event.key in self.controls.get('up', []):
            new_dir = (0, -1)
        elif event.key in self.controls.get('down', []):
            new_dir = (0, 1)
        elif event.key in self.controls.get('left', []):
            new_dir = (-1, 0)
        elif event.key in self.controls.get('right', []):
            new_dir = (1, 0)
            
        if new_dir:
            if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
                self.next_direction = new_dir

    def update(self):
        if not self.alive: return
        
        # Frozen Logic
        if self.frozen_timer > 0:
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                # Unfreeze
                self.color1 = self.original_color1
                self.color2 = self.original_color2
            # Fix: Always return if frozen (or just unfrozen this frame), to prevent immediate move
            # The user reported exit after freeze. 
            # If we return here, we skip move logic.
            return 
            
        self.direction = self.next_direction

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision - Bounce Logic
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            if len(self.body) > 2:
                self.body.pop()
                self.body.pop()
            else:
                self.alive = False
                return
            
            self.direction = (self.direction[0] * -1, self.direction[1] * -1)
            self.next_direction = self.direction
            new_head = (head_x + self.direction[0], head_y + self.direction[1])
            
            if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                 self.alive = False
                 return

        danger_zone = self.body[:]
        if self.grow_pending == 0:
            danger_zone.pop()
        
        if new_head in danger_zone:
            self.alive = False
            return

        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
            
    def shrink(self, amount):
        for _ in range(amount):
            if len(self.body) > 0:
                self.body.pop()
        if len(self.body) == 0:
            self.alive = False

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            pygame.draw.circle(surface, (30, 30, 30), (rect.centerx + 2, rect.centery + 4), GRID_SIZE // 2)
            pygame.draw.circle(surface, self.color1, rect.center, GRID_SIZE // 2 - 1)
            highlight_pos = (rect.centerx - GRID_SIZE // 6, rect.centery - GRID_SIZE // 6)
            pygame.draw.circle(surface, (255, 255, 255), highlight_pos, GRID_SIZE // 6)
            
            if i == 0:
                pygame.draw.circle(surface, (255, 255, 255), (rect.centerx - 8 + (self.direction[0]*5), rect.centery - 8 + (self.direction[1]*5)), 6)
                pygame.draw.circle(surface, (0, 0, 0), (rect.centerx - 8 + (self.direction[0]*7), rect.centery - 8 + (self.direction[1]*7)), 2)
                pygame.draw.circle(surface, (255, 255, 255), (rect.centerx + 8 + (self.direction[0]*5), rect.centery + 8 + (self.direction[1]*5)), 6)
                pygame.draw.circle(surface, (0, 0, 0), (rect.centerx + 8 + (self.direction[0]*7), rect.centery + 8 + (self.direction[1]*7)), 2)
        
        if self.frozen_timer > 0 and len(self.body) > 0:
            # Draw Ice Block overlay on head
            head_rect = pygame.Rect(self.body[0][0] * GRID_SIZE, self.body[0][1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(s, (200, 200, 255, 100), (0,0,GRID_SIZE, GRID_SIZE))
            surface.blit(s, head_rect)

class Food:
    def __init__(self, count=5):
        self.positions = []
        self.count = count

    def spawn(self, snake_bodies, bomb_pos=None):
        while len(self.positions) < self.count:
            self._add_one(snake_bodies, bomb_pos)

    def _add_one(self, snake_bodies, bomb_pos):
        all_body_parts = {part for body in snake_bodies for part in body}
        occupied = all_body_parts.union(set(self.positions))
        if bomb_pos:
            occupied.add(bomb_pos)
            
        attempts = 0
        while attempts < 50:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)
            
            if pos in occupied:
                attempts += 1
                continue
                
            too_close = False
            for other_pos in self.positions:
                dist = abs(x - other_pos[0]) + abs(y - other_pos[1])
                if dist < 8:
                    too_close = True
                    break
            
            if not too_close:
                self.positions.append(pos)
                return
            
            attempts += 1
            
        while True:
             x = random.randint(0, GRID_WIDTH - 1)
             y = random.randint(0, GRID_HEIGHT - 1)
             pos = (x, y)
             if pos not in occupied:
                 self.positions.append(pos)
                 return

    def remove(self, pos):
        if pos in self.positions:
            self.positions.remove(pos)

    def draw(self, surface):
        for pos in self.positions:
            x, y = pos
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.circle(surface, (30, 30, 30), (rect.centerx + 2, rect.centery + 4), GRID_SIZE // 2 - 2)
            pygame.draw.circle(surface, FOOD_COLOR, rect.center, GRID_SIZE // 2 - 2)
            pygame.draw.ellipse(surface, (50, 205, 50), (rect.centerx - 5, rect.top + 2, 10, 8))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Snake 3D - PvZ Style")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"
        self.mode = "SINGLE"
        
        self.snakes = []
        self.food = Food()
        self.bombs = []
        self.explosions = []
        self.score = [0, 0]
        self.fullscreen = False
        self.last_move_time = 0
        
        self.buttons = {}
        self.setup_buttons()

    def setup_buttons(self):
        center_x = SCREEN_WIDTH // 2
        self.buttons = {}
        
        self.buttons['MENU'] = [
            Button(center_x - 100, 250, 200, 50, "Single Player", lambda: self.start_game("SINGLE")),
            Button(center_x - 100, 320, 200, 50, "2 Player Versus", lambda: self.start_game("VERSUS")),
            Button(center_x - 100, 390, 200, 50, "Quit", self.quit_game)
        ]
        
        self.buttons['UI'] = [
            Button(SCREEN_WIDTH - 110, 10, 100, 40, "Pause", self.toggle_pause),
            Button(SCREEN_WIDTH - 220, 10, 100, 40, "Restart", lambda: self.start_game(self.mode)),
            Button(SCREEN_WIDTH - 330, 10, 100, 40, "Exit", self.to_menu) 
        ]

        self.buttons['PAUSED'] = [
            Button(center_x - 100, 250, 200, 50, "Resume", self.toggle_pause),
            Button(center_x - 100, 320, 200, 50, "Main Menu", self.to_menu)
        ]
        
        self.buttons['GAMEOVER'] = [
            Button(center_x - 100, 250, 200, 50, "Restart", lambda: self.start_game(self.mode)),
            Button(center_x - 100, 320, 200, 50, "Main Menu", self.to_menu)
        ]

    def start_game(self, mode):
        self.mode = mode
        self.snakes = []
        self.score = [0, 0]
        self.last_move_time = pygame.time.get_ticks()
        self.bombs = []
        self.explosions = []
        
        self.buttons['UI'][0].text = "Pause"
        
        spawn_margin = 8 
        
        if mode == "SINGLE":
            p1_controls = {
                'up': [pygame.K_w, pygame.K_UP], 
                'down': [pygame.K_s, pygame.K_DOWN], 
                'left': [pygame.K_a, pygame.K_LEFT], 
                'right': [pygame.K_d, pygame.K_RIGHT]
            }
            self.snakes.append(Snake(spawn_margin, spawn_margin, SNAKE_COLOR_1, SNAKE_COLOR_2, p1_controls))

        elif mode == "VERSUS":
            p1_controls = {
                'up': [pygame.K_w], 'down': [pygame.K_s], 
                'left': [pygame.K_a], 'right': [pygame.K_d]
            }
            self.snakes.append(Snake(spawn_margin, spawn_margin, SNAKE_COLOR_1, SNAKE_COLOR_2, p1_controls))
            
            p2_controls = {
                'up': [pygame.K_UP], 'down': [pygame.K_DOWN], 
                'left': [pygame.K_LEFT], 'right': [pygame.K_RIGHT]
            }
            self.snakes.append(Snake(GRID_WIDTH - (spawn_margin + 1), GRID_HEIGHT - (spawn_margin + 1), (147, 112, 219), (75, 0, 130), p2_controls))
            
        self.food = Food(count=5)
        self.food.spawn([s.body for s in self.snakes])
        
        self.spawn_bomb()
        
        self.state = "PLAYING"

    def spawn_bomb(self):
        if len(self.bombs) < 1:
            b = Bomb()
            all_bodies = {part for s in self.snakes for part in s.body}
            occupied = all_bodies.union(set(self.food.positions))
            b.force_spawn(occupied)
            self.bombs.append(b)

    def quit_game(self):
        self.running = False

    def toggle_pause(self):
        if self.state == "PLAYING":
            self.state = "PAUSED"
            self.buttons['UI'][0].text = "Resume"
        elif self.state == "PAUSED":
            self.state = "PLAYING"
            self.buttons['UI'][0].text = "Pause"

    def to_menu(self):
        self.state = "MENU"

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.update_dimensions()

    def update_dimensions(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT
        SCREEN_WIDTH, SCREEN_HEIGHT = self.screen.get_size()
        GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
        GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
        self.setup_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.update_dimensions()

            if self.state in self.buttons:
                 for btn in self.buttons[self.state]:
                     btn.handle_event(event)
            
            if self.state in ["PLAYING", "PAUSED", "GAMEOVER"]:
                 for btn in self.buttons['UI']:
                     btn.handle_event(event)

            if self.state == "PLAYING":
                for snake in self.snakes:
                    snake.handle_event(event)

    def update(self):
        if self.state != "PLAYING":
            return
            
        self.explosions = [e for e in self.explosions if e.update()]

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < MOVE_DELAY:
            return
        
        self.last_move_time = current_time
        
        for i, s in enumerate(self.snakes):
            if len(s.body) == 0:
                s.alive = False

        active_snakes = [s for s in self.snakes if s.alive]
        if not active_snakes:
            self.state = "GAMEOVER"
            return

        if self.mode == "SINGLE" and not self.snakes[0].alive:
            self.state = "GAMEOVER"
            return
        
        if self.mode == "VERSUS":
            alive_count = sum(1 for s in self.snakes if s.alive)
            if alive_count <= 1:
                self.state = "GAMEOVER"
                return

        for i, snake in enumerate(self.snakes):
            snake.update()
            
            if not snake.alive: continue
            
            head = snake.body[0]
            
            if head in self.food.positions:
                snake.grow_pending += 1
                self.score[i] += 10
                self.food.remove(head)
                self.food.spawn([s.body for s in self.snakes], self.bombs[0].position if self.bombs else None)
            
            for b in self.bombs:
                if b.active and head == b.position:
                    self.explosions.append(Explosion(head[0], head[1]))
                    snake.shrink(2)
                    self.bombs.remove(b)
                    self.spawn_bomb()
                    break
            
            if self.mode == "VERSUS":
                for other_snake in self.snakes:
                    if other_snake != snake and other_snake.alive:
                        if head in other_snake.body:
                            snake.freeze(25)
                            snake.direction = (snake.direction[0]*-1, snake.direction[1]*-1)
                            snake.next_direction = snake.direction
                            new_head_x = head[0] + snake.direction[0]
                            new_head_y = head[1] + snake.direction[1]
                            if (0 <= new_head_x < GRID_WIDTH and 0 <= new_head_y < GRID_HEIGHT):
                                snake.body.insert(0, (new_head_x, new_head_y))
                                snake.body.pop()
                            
        self.spawn_bomb()

    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                color = BG_COLOR_1 if (x + y) % 2 == 0 else BG_COLOR_2
                pygame.draw.rect(self.screen, color, rect)

    def draw(self):
        self.draw_grid()
        
        if self.state == "MENU":
            title_surf = TITLE_FONT.render("Snake 3D", True, (255, 255, 255))
            title_shadow = TITLE_FONT.render("Snake 3D", True, (0, 0, 0))
            self.screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + 4, 104))
            self.screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 100))
            
            for btn in self.buttons['MENU']:
                btn.draw(self.screen)
            
        elif self.state in ["PLAYING", "PAUSED", "GAMEOVER"]:
            self.food.draw(self.screen)
            for b in self.bombs:
                b.draw(self.screen)
                
            for snake in self.snakes:
                snake.draw(self.screen)
                
            for exp in self.explosions:
                exp.draw(self.screen)
            
            score_text = f"P1 Score: {self.score[0]}"
            if self.mode == "VERSUS":
                score_text += f" | P2 Score: {self.score[1]}"
            
            score_surf = FONT.render(score_text, True, TEXT_COLOR)
            self.screen.blit(score_surf, (10, 10))

            for btn in self.buttons['UI']:
                btn.draw(self.screen)
            
            if self.state == "PAUSED":
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                s.set_alpha(128)
                s.fill((0, 0, 0))
                self.screen.blit(s, (0, 0))
                
                pause_text = TITLE_FONT.render("PAUSED", True, (255, 255, 255))
                self.screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, 150))
                
                for btn in self.buttons['PAUSED']:
                    btn.draw(self.screen)
                
            if self.state == "GAMEOVER":
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                s.set_alpha(128)
                s.fill((50, 0, 0))
                self.screen.blit(s, (0, 0))
                
                msg = "GAME OVER"
                if self.mode == "VERSUS":
                    if self.snakes[0].alive and not self.snakes[1].alive:
                        msg = "Player 1 WINS!"
                    elif not self.snakes[0].alive and self.snakes[1].alive:
                        msg = "Player 2 WINS!"
                    else:
                        msg = "DRAW!"
                
                over_text = TITLE_FONT.render(msg, True, (255, 255, 255))
                self.screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 150))
                
                for btn in self.buttons['GAMEOVER']:
                    btn.draw(self.screen)
                
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
