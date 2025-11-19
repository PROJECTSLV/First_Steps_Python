from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from game.game_engine import GameEngine


class GeometryDashApp(App):
    def build(self):
        Window.size = (800, 600)

        game = GameEngine()
        return game


if __name__ == '__main__':
    GeometryDashApp().run()
