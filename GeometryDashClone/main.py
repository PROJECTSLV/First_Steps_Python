from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from game.game_engine import GameEngine

class GeometryDashApp(App):
    def build(self):
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '600')
        Config.set('graphics', 'resizable', '0')
        
        game = GameEngine()
        return game

if __name__ == '__main__':
    GeometryDashApp().run()
