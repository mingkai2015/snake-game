import pygame
import sys
from . import settings
from . import ui
from .snake import Snake
from .sprites import Food, Bomb, Explosion, Coin

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Snake 3D - PvZ Style")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"
        self.mode = "SINGLE"
        
        # Initialize Fonts
        self.font, self.title_font = ui.FontManager.load_fonts()
        
        self.snakes = []
        self.food = Food()
        self.bombs = []
        self.coins = []
        self.explosions = []
        self.score = [0, 0]
        self.start_time = 0
        self.time_remaining = settings.GAME_DURATION
        self.fullscreen = False
        self.last_move_time = 0
        
        self.buttons = {}
        self.setup_buttons()

    def setup_buttons(self):
        center_x = settings.SCREEN_WIDTH // 2
        self.buttons = {}
        
        self.buttons['MENU'] = [
            ui.Button(center_x - 100, 250, 200, 50, "Single Player", self.font, lambda: self.start_game("SINGLE")),
            ui.Button(center_x - 100, 320, 200, 50, "2 Player Versus", self.font, lambda: self.start_game("VERSUS")),
            ui.Button(center_x - 100, 390, 200, 50, "Quit", self.font, self.quit_game)
        ]
        
        self.buttons['UI'] = [
            ui.Button(settings.SCREEN_WIDTH - 110, 10, 100, 40, "Pause", self.font, self.toggle_pause),
            ui.Button(settings.SCREEN_WIDTH - 220, 10, 100, 40, "Restart", self.font, lambda: self.start_game(self.mode)),
            ui.Button(settings.SCREEN_WIDTH - 330, 10, 100, 40, "Exit", self.font, self.to_menu) 
        ]

        self.buttons['PAUSED'] = [
            ui.Button(center_x - 100, 250, 200, 50, "Resume", self.font, self.toggle_pause),
            ui.Button(center_x - 100, 320, 200, 50, "Main Menu", self.font, self.to_menu)
        ]
        
        self.buttons['GAMEOVER'] = [
            ui.Button(center_x - 100, 250, 200, 50, "Restart", self.font, lambda: self.start_game(self.mode)),
            ui.Button(center_x - 100, 320, 200, 50, "Main Menu", self.font, self.to_menu)
        ]

    def start_game(self, mode):
        self.mode = mode
        self.snakes = []
        self.score = [0, 0]
        self.last_move_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = settings.GAME_DURATION
        self.bombs = []
        self.coins = []
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
            self.snakes.append(Snake(spawn_margin, spawn_margin, settings.SNAKE_COLOR_1, settings.SNAKE_COLOR_2, p1_controls))

        elif mode == "VERSUS":
            p1_controls = {
                'up': [pygame.K_w], 'down': [pygame.K_s], 
                'left': [pygame.K_a], 'right': [pygame.K_d]
            }
            self.snakes.append(Snake(spawn_margin, spawn_margin, settings.SNAKE_COLOR_1, settings.SNAKE_COLOR_2, p1_controls))
            
            p2_controls = {
                'up': [pygame.K_UP], 'down': [pygame.K_DOWN], 
                'left': [pygame.K_LEFT], 'right': [pygame.K_RIGHT]
            }
            # Player 2 starts at Left-Bottom (parallel to P1 at Left-Top)
            self.snakes.append(Snake(spawn_margin, settings.GRID_HEIGHT - (spawn_margin + 1), (147, 112, 219), (75, 0, 130), p2_controls))
            
        self.food = Food(count=5)
        self.food.spawn([s.body for s in self.snakes])
        
        self.spawn_bomb()
        self.spawn_coins()
        
        self.state = "PLAYING"

    def spawn_coins(self):
        # Ensure 1 Yellow and 1 Red coin
        coin_types = [
            {'color': settings.COIN_YELLOW_COLOR, 'value': 3, 'exists': False},
            {'color': settings.COIN_RED_COLOR, 'value': 5, 'exists': False}
        ]
        
        for c in self.coins:
            if c.value == 3: coin_types[0]['exists'] = True
            if c.value == 5: coin_types[1]['exists'] = True
            
        all_bodies = {part for s in self.snakes for part in s.body}
        occupied = all_bodies.union(set(self.food.positions))
        if self.bombs:
            for b in self.bombs:
                if b.active: occupied.add(b.position)
        for c in self.coins:
            if c.active: occupied.add(c.position)
            
        for c_type in coin_types:
            if not c_type['exists']:
                new_coin = Coin(c_type['color'], c_type['value'])
                new_coin.spawn(occupied)
                if new_coin.active:
                    self.coins.append(new_coin)
                    occupied.add(new_coin.position)

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
        settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT = self.screen.get_size()
        settings.GRID_WIDTH = settings.SCREEN_WIDTH // settings.GRID_SIZE
        settings.GRID_HEIGHT = settings.SCREEN_HEIGHT // settings.GRID_SIZE
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

        if self.state == "PLAYING":
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            self.time_remaining = max(0, settings.GAME_DURATION - elapsed)
            if self.time_remaining == 0:
                self.state = "GAMEOVER"
                return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < settings.MOVE_DELAY:
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
                self.food.spawn([s.body for s in self.snakes], self.bombs[0].position if self.bombs else None, {c.position for c in self.coins if c.active})
            
            for c in self.coins[:]:
                if c.active and head == c.position:
                    # Yellow = 3 apples (30), Red = 5 apples (50)
                    points = 30 if c.value == 3 else 50
                    self.score[i] += points
                    # Optional: Grow snake? "Yellow coin worth 3 apples" usually implies score, maybe growth too?
                    # User said "worth 3 apples", implying score equivalence. 
                    # If it implies growth, 3 apples would be huge growth. 
                    # Standard interpretation is usually score. Let's stick to score for now or small growth?
                    # Let's do score only to avoid uncontrollable length.
                    self.coins.remove(c)
                    self.spawn_coins()
            
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
                            if (0 <= new_head_x < settings.GRID_WIDTH and 0 <= new_head_y < settings.GRID_HEIGHT):
                                snake.body.insert(0, (new_head_x, new_head_y))
                                snake.body.pop()
                            
        self.spawn_bomb()

    def draw_grid(self):
        for x in range(settings.GRID_WIDTH):
            for y in range(settings.GRID_HEIGHT):
                rect = pygame.Rect(x * settings.GRID_SIZE, y * settings.GRID_SIZE, settings.GRID_SIZE, settings.GRID_SIZE)
                color = settings.BG_COLOR_1 if (x + y) % 2 == 0 else settings.BG_COLOR_2
                pygame.draw.rect(self.screen, color, rect)

    def draw(self):
        self.draw_grid()
        
        if self.state == "MENU":
            title_surf = self.title_font.render("Snake 3D", True, (255, 255, 255))
            title_shadow = self.title_font.render("Snake 3D", True, (0, 0, 0))
            self.screen.blit(title_shadow, (settings.SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + 4, 104))
            self.screen.blit(title_surf, (settings.SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 100))
            
            for btn in self.buttons['MENU']:
                btn.draw(self.screen)
            
        elif self.state in ["PLAYING", "PAUSED", "GAMEOVER"]:
            self.food.draw(self.screen)
            for b in self.bombs:
                b.draw(self.screen)
            for c in self.coins:
                c.draw(self.screen)
                
            for snake in self.snakes:
                snake.draw(self.screen)
                
            for exp in self.explosions:
                exp.draw(self.screen)
            
            score_text = f"P1 Score: {self.score[0]}"
            if self.mode == "VERSUS":
                score_text += f" | P2 Score: {self.score[1]}"
            
            # Timer
            timer_text = f"Time: {self.time_remaining}"
            timer_surf = self.font.render(timer_text, True, (255, 255, 255))
            self.screen.blit(timer_surf, (settings.SCREEN_WIDTH // 2 - timer_surf.get_width() // 2, 10))

            score_surf = self.font.render(score_text, True, settings.TEXT_COLOR)
            self.screen.blit(score_surf, (10, 10))

            for btn in self.buttons['UI']:
                btn.draw(self.screen)
            
            if self.state == "PAUSED":
                s = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
                s.set_alpha(128)
                s.fill((0, 0, 0))
                self.screen.blit(s, (0, 0))
                
                pause_text = self.title_font.render("PAUSED", True, (255, 255, 255))
                self.screen.blit(pause_text, (settings.SCREEN_WIDTH//2 - pause_text.get_width()//2, 150))
                
                for btn in self.buttons['PAUSED']:
                    btn.draw(self.screen)
                
            if self.state == "GAMEOVER":
                s = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
                s.set_alpha(128)
                s.fill((50, 0, 0))
                self.screen.blit(s, (0, 0))
                
                msg = "GAME OVER"
                if self.mode == "VERSUS":
                    if self.time_remaining == 0:
                        if self.score[0] > self.score[1]:
                            msg = "Time's Up! P1 WINS!"
                        elif self.score[1] > self.score[0]:
                            msg = "Time's Up! P2 WINS!"
                        else:
                            msg = "Time's Up! DRAW!"
                    else:
                         # Existing death logic
                        if self.snakes[0].alive and not self.snakes[1].alive:
                            msg = "Player 1 WINS!"
                        elif not self.snakes[0].alive and self.snakes[1].alive:
                            msg = "Player 2 WINS!"
                        else:
                            msg = "DRAW!"
                else:
                    if self.time_remaining == 0:
                         msg = f"Time's Up! Score: {self.score[0]}"
                
                # Draw Podium if VS mode
                if self.mode == "VERSUS":
                    self.draw_podium(self.score[0], self.score[1])

                over_text = self.title_font.render(msg, True, (255, 255, 255))
                self.screen.blit(over_text, (settings.SCREEN_WIDTH//2 - over_text.get_width()//2, 50))
                
                for btn in self.buttons['GAMEOVER']:
                    btn.draw(self.screen)
        
        pygame.display.flip()

    def draw_podium(self, score1, score2):
        cx = settings.SCREEN_WIDTH // 2
        cy = settings.SCREEN_HEIGHT // 2 + 50
        
        # Platforms
        # 1st place is higher (center), 2nd is lower (left or right)
        # We are just showing 2 players. 
        # If P1 wins: P1 Center High, P2 Right Low
        # If P2 wins: P2 Center High, P1 Left Low
        # If Draw: Both same height
        
        p1_color = settings.SNAKE_COLOR_1
        p2_color = (147, 112, 219)
        
        rect_width = 80
        
        if score1 > score2:
            # P1 1st (Center), P2 2nd (Right)
            # 1st Place
            pygame.draw.rect(self.screen, (255, 215, 0), (cx - rect_width//2, cy, rect_width, 100))
            self.draw_snake_head_icon(cx, cy - 30, p1_color)
            self.draw_text("1", cx, cy + 20, (0,0,0))
            
            # 2nd Place
            pygame.draw.rect(self.screen, (192, 192, 192), (cx + rect_width//2 + 10, cy + 40, rect_width, 60))
            self.draw_snake_head_icon(cx + rect_width//2 + 10 + rect_width//2, cy + 40 - 30, p2_color)
            self.draw_text("2", cx + rect_width//2 + 10 + rect_width//2, cy + 60, (0,0,0))
            
        elif score2 > score1:
            # P2 1st (Center), P1 2nd (Left)
             # 1st Place
            pygame.draw.rect(self.screen, (255, 215, 0), (cx - rect_width//2, cy, rect_width, 100))
            self.draw_snake_head_icon(cx, cy - 30, p2_color)
            self.draw_text("1", cx, cy + 20, (0,0,0))
            
            # 2nd Place
            pygame.draw.rect(self.screen, (192, 192, 192), (cx - rect_width//2 - 10 - rect_width, cy + 40, rect_width, 60))
            self.draw_snake_head_icon(cx - rect_width//2 - 10 - rect_width//2, cy + 40 - 30, p1_color)
            self.draw_text("2", cx - rect_width//2 - 10 - rect_width//2, cy + 60, (0,0,0))
            
        else:
            # Draw - Same Height
            pygame.draw.rect(self.screen, (192, 192, 192), (cx - rect_width - 5, cy + 20, rect_width, 80))
            self.draw_snake_head_icon(cx - rect_width - 5 + rect_width//2, cy + 20 - 30, p1_color)
            
            pygame.draw.rect(self.screen, (192, 192, 192), (cx + 5, cy + 20, rect_width, 80))
            self.draw_snake_head_icon(cx + 5 + rect_width//2, cy + 20 - 30, p2_color)

    def draw_snake_head_icon(self, x, y, color):
        pygame.draw.circle(self.screen, color, (x, y), 20)
        # Eyes
        pygame.draw.circle(self.screen, (255, 255, 255), (x - 8, y - 8), 6)
        pygame.draw.circle(self.screen, (0, 0, 0), (x - 8, y - 8), 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (x + 8, y - 8), 6)
        pygame.draw.circle(self.screen, (0, 0, 0), (x + 8, y - 8), 2)

    def draw_text(self, text, x, y, color):
        surf = self.font.render(text, True, color)
        self.screen.blit(surf, (x - surf.get_width()//2, y - surf.get_height()//2))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

