from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty

class Player(Widget):
    velocity_y = NumericProperty(0)
    is_jumping = BooleanProperty(False)
    gravity = NumericProperty(-15)
    jump_force = NumericProperty(20)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (40, 40)
        self.pos = (100, 200)
    
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_force
            self.is_jumping = True
    
    def update(self, dt):
        # Apply gravity
        self.velocity_y += self.gravity * dt
        
        # Update position
        self.y += self.velocity_y
        
        # Ground collision
        if self.y <= 200:
            self.y = 200
            self.velocity_y = 0
            self.is_jumping = False
