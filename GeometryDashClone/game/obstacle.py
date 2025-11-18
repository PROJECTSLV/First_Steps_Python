from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
import random

class Obstacle(Widget):
    speed = NumericProperty(5)
    
    def __init__(self, x_pos, obstacle_type=0, **kwargs):
        super().__init__(**kwargs)
        self.obstacle_type = obstacle_type
        
        if obstacle_type == 0:  # Ground spike
            self.size = (30, 50)
            self.pos = (x_pos, 200)
        elif obstacle_type == 1:  # Flying obstacle
            self.size = (30, 30)
            self.pos = (x_pos, 250)
        else:  # High obstacle
            self.size = (30, 80)
            self.pos = (x_pos, 200)
    
    def update(self, dt):
        self.x -= self.speed
        
    def is_off_screen(self):
        return self.x < -50
    
    def collides_with_player(self, player):
        return (self.collide_widget(player) and 
                abs(player.center_x - self.center_x) < 30 and 
                abs(player.center_y - self.center_y) < 30)
