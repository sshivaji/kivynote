from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex


Window.clearcolor = (1, 1, 1, 1)

class KivyDraw(Widget):

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 1.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=3)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class KivyNoteBookApp(App):

    def build(self):
        parent = Widget()
        self.painter = KivyDraw()
        clearbtn = ColorButton(text='Clear', shorten=True)
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()

class ColorButton(Button):
    def __init__(self, **kwargs):
        super(ColorDownButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = get_color_from_hex('#000080')

 #   def on_press(self):
 #       self.background_color = self.background_color_down

 #   def on_release(self):
 #       self.background_color = self.background_color_normal


if __name__ == '__main__':
    KivyNoteBookApp().run()
