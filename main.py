from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout

Window.clearcolor = (1, 1, 1, 1)
erase_color = (1,1,1,1)
class KivyDraw(Widget):
    def __init__(self, **kwargs):
        super(KivyDraw, self).__init__(**kwargs)
        self.color = None
    
    def on_touch_down(self, touch):
        if not self.color:
            color = (random(), random(), random())
            print(color)
        else:
            color = self.color
        with self.canvas:
            Color(*color)
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
       
        erasebtn = ColorButton(text='Erase', shorten=True)
        erasebtn.bind(on_release=self.set_erase) 
        parent.add_widget(self.painter)
        layout = BoxLayout(orientation = 'horizontal', padding=5, spacing=5)
        layout.add_widget(clearbtn)
        layout.add_widget(erasebtn)
        parent.add_widget(layout)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        self.painter.color = None

    def set_erase(self, obj):
        self.painter.color = erase_color

class ColorButton(Button):
    def __init__(self, **kwargs):
        super(ColorButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = get_color_from_hex('#000080')

 #   def on_press(self):
 #       self.background_color = self.background_color_down

 #   def on_release(self):
 #       self.background_color = self.background_color_normal


if __name__ == '__main__':
    KivyNoteBookApp().run()
