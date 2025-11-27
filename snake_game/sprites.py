import pygame
import random
import math
from . import settings

class Explosion:
    def __init__(self, x, y):
        self.x = x * settings.GRID_SIZE + settings.GRID_SIZE // 2
        self.y = y * settings.GRID_SIZE + settings.GRID_SIZE // 2
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
            x = random.randint(0, settings.GRID_WIDTH - 1)
            y = random.randint(0, settings.GRID_HEIGHT - 1)
            if (x, y) not in occupied_positions:
                self.position = (x, y)
                self.active = True
                break

    def draw(self, surface):
        if not self.active: return
        x, y = self.position
        rect = pygame.Rect(x * settings.GRID_SIZE, y * settings.GRID_SIZE, settings.GRID_SIZE, settings.GRID_SIZE)
        
        # Draw Bomb Body
        c = rect.center
        pygame.draw.circle(surface, (30, 30, 30), c, settings.GRID_SIZE // 2 - 2) # Outline
        pygame.draw.circle(surface, (60, 60, 60), (c[0]-2, c[1]-2), settings.GRID_SIZE // 2 - 4) # Highlight
        
        # Wick
        pygame.draw.line(surface, (150, 100, 50), c, (c[0] + 5, c[1] - 10), 2)
        
        # Spark
        if pygame.time.get_ticks() % 200 < 100:
            spark_pos = (c[0] + 5, c[1] - 10)
            pygame.draw.circle(surface, (255, 255, 0), spark_pos, 4)
            pygame.draw.circle(surface, (255, 50, 0), spark_pos, 2)

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
            x = random.randint(0, settings.GRID_WIDTH - 1)
            y = random.randint(0, settings.GRID_HEIGHT - 1)
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
             x = random.randint(0, settings.GRID_WIDTH - 1)
             y = random.randint(0, settings.GRID_HEIGHT - 1)
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
            rect = pygame.Rect(x * settings.GRID_SIZE, y * settings.GRID_SIZE, settings.GRID_SIZE, settings.GRID_SIZE)
            pygame.draw.circle(surface, (30, 30, 30), (rect.centerx + 2, rect.centery + 4), settings.GRID_SIZE // 2 - 2)
            pygame.draw.circle(surface, settings.FOOD_COLOR, rect.center, settings.GRID_SIZE // 2 - 2)
            pygame.draw.ellipse(surface, (50, 205, 50), (rect.centerx - 5, rect.top + 2, 10, 8))

