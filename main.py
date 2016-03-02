from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy import utils
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from itertools import cycle


Window.clearcolor = (1, 1, 1, 1)
erase_color = (1,1,1,1)

colors = [utils.hex_colormap['blue'], utils.hex_colormap['green'], utils.hex_colormap['red'], utils.hex_colormap['purple'], utils.hex_colormap['orange'], utils.hex_colormap['brown'], utils.hex_colormap['black']]
color_cycle = cycle(colors)
# print (utils.hex_colormap)
# current_color = None

class KivyDraw(Widget):
    def __init__(self, **kwargs):
        super(KivyDraw, self).__init__(**kwargs)
        # global current_color
        self.color = get_color_from_hex(color_cycle.next())
        self.previous_color = None
    def on_touch_down(self, touch):
        color = self.color
        width = 3
        with self.canvas:
            Color(*color)
            # print(color)
            if color == erase_color:
                # print("Erase color!!")
                width = 10
            d = 1.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=width)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class KivyNoteBookApp(App):

    def build(self):
        parent = Widget()
        self.painter = KivyDraw()
        clearbtn = ColorButton(text='Clear', shorten=True, size_hint=(None,1))
        clearbtn.bind(on_release=self.clear_canvas)
       
        erasebtn = CustomToggleButton(text='Erase', shorten=True, size_hint=(None,1))
        erasebtn.bind(on_release=self.set_erase)

        colorbtn = ColorToggleButton(text='Color', shorten=True, size_hint=(None,1), painter = self.painter)
        colorbtn.bind(on_release=self.set_color)

        savebtn = ColorButton(text='Save', shorten=True, size_hint=(None,1), painter = self.painter)
        savebtn.bind(on_release=self.save)

        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(self.painter)

        button_layout = GridLayout(cols=4, spacing=5)
        button_layout.add_widget(clearbtn)
        button_layout.add_widget(erasebtn)
        button_layout.add_widget(colorbtn)
        button_layout.add_widget(savebtn)

        layout.add_widget(button_layout)

        # parent.add_widget(self.painter)
        parent.add_widget(layout)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        color_cycle = cycle(colors)
        # global current_color

        self.painter.color = get_color_from_hex(color_cycle.next())
        # self.painter.color = self.painter.current_color

    def set_color(self, obj):
        # self.painter.canvas.clear()
        # blue, green, red, purple, orange, brown, black
        # self.painter.color = colors
        # global current_color
        # current_color = get_color_from_hex(color_cycle.next())
        self.painter.color = get_color_from_hex(color_cycle.next())

    def set_erase(self, obj):
        if self.painter.color == erase_color:
            self.painter.color = self.painter.previous_color
            # self.painter.previous_color = self.painter.color
            # self.painter.color = get_color_from_hex('#000080')
        else:
            self.painter.previous_color = self.painter.color
            self.painter.color = erase_color

    def save(self, obj):
        pass


class ColorButton(Button):
    def __init__(self, **kwargs):
        super(ColorButton, self).__init__(**kwargs)
        # self.background_normal = ""
        # self.background_down = ""
        # self.background_color = get_color_from_hex('#000080')

class CustomToggleButton(ToggleButton):
    def __init__(self, **kwargs):
        super(CustomToggleButton, self).__init__(**kwargs)
        # self.background_normal = ""
        # self.background_down = utils.hex_colormap['blue']
        # self.background_color = get_color_from_hex('#000080')


class ColorToggleButton(Button):
    def __init__(self, **kwargs):
        super(ColorToggleButton, self).__init__(**kwargs)
        self.painter = kwargs['painter']
        # print(self.painter)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = get_color_from_hex('#000080')

   # def on_press(self):
       # self.background_color = self.background_color_down

    def on_release(self):
       # self.background_color = self.background_color_normal
       # current_color = color_cycle.next()
       # print(current_color)
       self.painter.color = get_color_from_hex(color_cycle.next())

       self.background_color = self.painter.color

if __name__ == '__main__':
    KivyNoteBookApp().run()
