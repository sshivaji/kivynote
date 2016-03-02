from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy import utils
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from itertools import cycle
from functools import partial

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
        self.draw_on_move = False
        self.line = None
        self.history = []

    def on_motion(self, dt):
        if self.draw_on_move:
            # print Window.mouse_pos
            # self.on_touch_down(Window.mouse_pos)
            with self.canvas:
                Color(*self.color)
                # Line(points=(Window.mouse_pos[0], Window.mouse_pos[1]), width=3)
                self.line.points += [Window.mouse_pos[0], Window.mouse_pos[1]]

    def on_touch_down(self, touch):
        # Make eraser color larger
        width = 10 if self.color == erase_color else 3

        if touch.is_double_tap:
            self.draw_on_move = not self.draw_on_move
            with self.canvas:
                Color(*self.color)
                self.line = Line(points=(touch.x, touch.y), width=width)
        else:
            with self.canvas:
                Color(*self.color)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=width)
                self.history.append(touch.ud['line'])

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
        # self.history = touch.ud['line']

class KivyNoteBookApp(App):

    def build(self):
        parent = Widget()
        self.painter = KivyDraw()
        Clock.schedule_interval(partial(self.painter.on_motion), 0.05)

        clearbtn = ColorButton(text='Clear', shorten=True, size_hint=(None,1))
        clearbtn.bind(on_release=self.clear_canvas)

        erasebtn = CustomToggleButton(text='Pen', shorten=True, size_hint=(None,1))
        erasebtn.bind(on_release=self.set_erase)

        self.colorbtn = ColorToggleButton(shorten=True, size_hint=(None, 1), painter = self.painter)
        self.colorbtn.bind(on_release=self.set_color)

        undo_btn = ColorButton(text='Undo', shorten=True, size_hint=(None, 1), painter = self.painter)
        undo_btn.bind(on_release=self.undo)


        savebtn = ColorButton(text='Save', shorten=True, size_hint=(None, 1), painter = self.painter)
        savebtn.bind(on_release=self.save)

        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(self.painter)

        button_layout = GridLayout(cols=5, spacing=5)
        button_layout.add_widget(clearbtn)
        button_layout.add_widget(erasebtn)
        button_layout.add_widget(savebtn)
        button_layout.add_widget(undo_btn)

        button_layout.add_widget(self.colorbtn)

        layout.add_widget(button_layout)

        # parent.add_widget(self.painter)
        parent.add_widget(layout)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        color_cycle = cycle(colors)
        # global current_color

        self.painter.color = get_color_from_hex(color_cycle.next())
        self.colorbtn.background_color = self.painter.color
        # self.set_color()
        # self.painter.color = self.painter.current_color

    def undo(self, obj):
        with self.painter.canvas:
            if len(self.painter.history)>0:
                el = self.painter.history.pop()
                self.painter.canvas.remove(el)

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

    def on_press(self):
        if self.state == 'down':
            self.text = 'Erase'
        else:
            self.text = 'Pen'

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
