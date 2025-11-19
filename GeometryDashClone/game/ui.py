from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty


class ScoreDisplay(Label):
    score = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = f"Score: {self.score}"
        self.font_size = '20sp'
        self.color = (1, 1, 1, 1)
        self.bold = True
    
    def on_score(self):
        self.text = f"Score: {self.score}"


class GameOverDisplay(BoxLayout):
    final_score = NumericProperty(0)
    high_score = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.6, 0.4)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
