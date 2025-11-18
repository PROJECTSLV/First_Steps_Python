from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import random

from .player import Player
from .obstacle import Obstacle

class GameEngine(Widget):
    score = NumericProperty(0)
    is_game_running = BooleanProperty(False)
    game_over = BooleanProperty(False)
    high_score = NumericProperty(0)
    status_text = StringProperty("Press SPACE to start")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player()
        self.obstacles = []
        self.obstacle_timer = 0
        self.obstacle_frequency = 2.0  # seconds between obstacles
        
        self.bind(size=self._update_bg)
        Window.bind(on_key_down=self._on_key_down)
        
        self.add_widget(self.player)
        
    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.1, 0.1, 0.3, 1)
            Rectangle(pos=self.pos, size=self.size)
    
    def _on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 32:  # SPACE
            if not self.is_game_running and not self.game_over:
                self.start_game()
            elif self.is_game_running:
                self.player.jump()
            elif self.game_over:
                self.restart_game()
    
    def start_game(self):
        self.is_game_running = True
        self.game_over = False
        self.score = 0
        self.obstacles = []
        self.obstacle_timer = 0
        self.status_text = ""
        
        # Clear existing obstacles
        for obstacle in self.obstacles[:]:
            self.remove_widget(obstacle)
        
        self.obstacles.clear()
        
        # Start game loop
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 1/60.)
    
    def restart_game(self):
        self.game_over = False
        self.start_game()
    
    def end_game(self):
        self.is_game_running = False
        self.game_over = True
        self.high_score = max(self.high_score, self.score)
        self.status_text = f"Game Over! Score: {self.score}\nPress SPACE to restart"
        Clock.unschedule(self.update)
    
    def update(self, dt):
        if not self.is_game_running:
            return
            
        # Update player
        self.player.update(dt)
        
        # Generate obstacles
        self.obstacle_timer += dt
        if self.obstacle_timer >= self.obstacle_frequency:
            self.generate_obstacle()
            self.obstacle_timer = 0
        
        # Update obstacles and check collisions
        for obstacle in self.obstacles[:]:
            obstacle.update(dt)
            
            if obstacle.collides_with_player(self.player):
                self.end_game()
                return
                
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.remove_widget(obstacle)
                self.score += 1
    
    def generate_obstacle(self):
        obstacle_type = random.randint(0, 2)
        new_obstacle = Obstacle(x_pos=self.width, obstacle_type=obstacle_type)
        self.obstacles.append(new_obstacle)
        self.add_widget(new_obstacle)
    
    def on_touch_down(self, touch):
        if self.is_game_running:
            self.player.jump()
        elif not self.game_over:
            self.start_game()
        elif self.game_over:
            self.restart_game()
        return True
