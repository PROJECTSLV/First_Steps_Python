from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
import random


class Obstacle(Widget):
    speed = NumericProperty(5)

    def __init__(self, x_pos, obstacle_type=0, **kwargs):
        super().__init__(**kwargs)
        self.obstacle_type = obstacle_type

        if obstacle_type == 0:
            self.size = (30, 50)
            self.pos = (x_pos, 200)
            color = (0, 1, 0, 1)
        elif obstacle_type == 1:
            self.size = (30, 30)
            self.pos = (x_pos, 250)
            color = (1, 1, 0, 1)
        else:  # High obstacle
            self.size = (30, 80)
            self.pos = (x_pos, 200)
            color = (0, 0, 1, 1)

        with self.canvas:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self, dt):
        self.x -= self.speed
        self.rect.pos = self.pos

    def is_off_screen(self):
        return self.x < -50

    def collides_with_player(self, player):
        return (self.collide_widget(player) and
                abs(player.center_x - self.center_x) < 30 and
                abs(player.center_y - self.center_y) < 30)