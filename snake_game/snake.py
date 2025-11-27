import pygame
from . import settings

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
        self.color1 = settings.FROZEN_COLOR_1
        self.color2 = settings.FROZEN_COLOR_2
        
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
                # Length - 2, restore original game state
                if len(self.body) > 2:
                    self.shrink(2)
            return 
            
        self.direction = self.next_direction

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision - Bounce Logic
        if not (0 <= new_head[0] < settings.GRID_WIDTH and 0 <= new_head[1] < settings.GRID_HEIGHT):
            # Reverse direction
            self.direction = (self.direction[0] * -1, self.direction[1] * -1)
            self.next_direction = self.direction
            
            if len(self.body) > 2:
                # Pop 2 from head to avoid self-collision (reversing into neck) and satisfy "length - 2"
                self.body.pop(0)
                self.body.pop(0)
                return
            else:
                # Length <= 2, just bounce and ignore self-collision for this step
                new_head = (head_x + self.direction[0], head_y + self.direction[1])
                
                if not (0 <= new_head[0] < settings.GRID_WIDTH and 0 <= new_head[1] < settings.GRID_HEIGHT):
                     pass
                
                # Force move without collision check
                self.body.insert(0, new_head)
                if self.grow_pending > 0:
                    self.grow_pending -= 1
                else:
                    self.body.pop()
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
            rect = pygame.Rect(x * settings.GRID_SIZE, y * settings.GRID_SIZE, settings.GRID_SIZE, settings.GRID_SIZE)
            
            pygame.draw.circle(surface, (30, 30, 30), (rect.centerx + 2, rect.centery + 4), settings.GRID_SIZE // 2)
            pygame.draw.circle(surface, self.color1, rect.center, settings.GRID_SIZE // 2 - 1)
            highlight_pos = (rect.centerx - settings.GRID_SIZE // 6, rect.centery - settings.GRID_SIZE // 6)
            pygame.draw.circle(surface, (255, 255, 255), highlight_pos, settings.GRID_SIZE // 6)
            
            if i == 0:
                pygame.draw.circle(surface, (255, 255, 255), (rect.centerx - 8 + (self.direction[0]*5), rect.centery - 8 + (self.direction[1]*5)), 6)
                pygame.draw.circle(surface, (0, 0, 0), (rect.centerx - 8 + (self.direction[0]*7), rect.centery - 8 + (self.direction[1]*7)), 2)
                pygame.draw.circle(surface, (255, 255, 255), (rect.centerx + 8 + (self.direction[0]*5), rect.centery + 8 + (self.direction[1]*5)), 6)
                pygame.draw.circle(surface, (0, 0, 0), (rect.centerx + 8 + (self.direction[0]*7), rect.centery + 8 + (self.direction[1]*7)), 2)
        
        if self.frozen_timer > 0 and len(self.body) > 0:
            # Draw Ice Block overlay on head
            head_rect = pygame.Rect(self.body[0][0] * settings.GRID_SIZE, self.body[0][1] * settings.GRID_SIZE, settings.GRID_SIZE, settings.GRID_SIZE)
            s = pygame.Surface((settings.GRID_SIZE, settings.GRID_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(s, (200, 200, 255, 100), (0,0,settings.GRID_SIZE, settings.GRID_SIZE))
            surface.blit(s, head_rect)

