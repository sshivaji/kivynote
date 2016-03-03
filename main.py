from random import random
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy import utils
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from itertools import cycle
from functools import partial


Window.clearcolor = (1, 1, 1, 1)
erase_color = (1,1,1,1)

colors = [utils.hex_colormap['blue'], utils.hex_colormap['green'], utils.hex_colormap['red'], utils.hex_colormap['purple'], utils.hex_colormap['orange'], utils.hex_colormap['brown'], utils.hex_colormap['black']]
color_cycle = cycle(colors)

class MyPopup(Popup):
    def show_popup(self):
        mytext= ""

        content = BoxLayout(orientation="vertical")

        content.add_widget(Label(text=mytext, font_size=20))

        mybutton = Button(text="Got It!", size_hint=(1,.20), font_size=20)
        content.add_widget(mybutton)

        mypopup = Popup(content = content,
                title = "Including Itens",
                auto_dismiss = False,
                size_hint = (.7, .5),
                font_size = 20)
        mybutton.bind(on_press=mypopup.dismiss)
        mypopup.open()


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
        # super(KivyDraw, self).on_motion(touch)

        if self.draw_on_move:
            # print Window.mouse_pos
            # self.on_touch_down(Window.mouse_pos)
            with self.canvas:
                Color(*self.color)
                # Line(points=(Window.mouse_pos[0], Window.mouse_pos[1]), width=3)
                self.line.points += [Window.mouse_pos[0], Window.mouse_pos[1]]

    def on_touch_down(self, touch):
        super(KivyDraw, self).on_touch_down(touch)
        # if not self.collide_point(touch.x, touch.y):
        #     return False
            # return True
        # Make eraser color larger
        width = 10 if self.color == erase_color else 3

        if touch.is_double_tap:
            self.draw_on_move = not self.draw_on_move
            with self.canvas:
                Color(*self.color)
                self.line = Line(points=(touch.x, touch.y), width=width)
                # Rectangle(pos=(touch.x, touch.y), texture=texture, size=texture_size)
        elif self.keyboard_mode:
            def set_caption(t):
                print(t.content.text)
                mylabel = CoreLabel(text=t.content.text, font_size=25, color=self.color, position=(Window.mouse_pos[0], Window.mouse_pos[1]))
                # Force refresh to compute things and generate the texture
                mylabel.refresh()
                texture = mylabel.texture
                texture_size = list(texture.size)
                with self.canvas:
                    Rectangle(pos=(touch.x, touch.y), texture=texture, size=texture_size)

            Popup(title="Enter text here",
              content=TextInput(text='', focus=False, multiline=False),
              size_hint=(0.6, 0.6),
              on_dismiss=set_caption).open()
        else:
            with self.canvas:
                Color(*self.color)
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=width)
                self.history.append(touch.ud['line'])


    def on_touch_move(self, touch):
        super(KivyDraw, self).on_touch_move(touch)

        touch.ud['line'].points += [touch.x, touch.y]
        # self.history = touch.ud['line']

class KivyNoteBookApp(App):
    def to_window(self, x, y):
        return [100,100]

    def build(self):
        self.y = None
        parent = Widget()
        self.painter = KivyDraw()
        self.painter.keyboard_mode = False

        # self.painter._keyboard = Window.request_keyboard(self.painter._keyboard_closed, self)
        # self.painter._keyboard.bind(on_key_down=self.painter._on_keyboard_down)
        Clock.schedule_interval(partial(self.painter.on_motion), 0.05)

        clearbtn = ColorButton(text='Clear', shorten=True, size_hint=(None,1))
        clearbtn.bind(on_release=self.clear_canvas)

        erasebtn = CustomToggleButton(text='Pen', default='Pen', down='Erase', shorten=True, size_hint=(None,1))
        erasebtn.bind(on_release=self.set_erase)

        self.colorbtn = ColorToggleButton(shorten=True, size_hint=(None, 1), painter = self.painter)
        self.colorbtn.bind(on_release=self.set_color)

        undo_btn = ColorButton(text='Undo', shorten=True, size_hint=(None, 1), painter = self.painter)
        undo_btn.bind(on_release=self.undo)

        savebtn = ColorButton(text='Save', shorten=True, size_hint=(None, 1), painter = self.painter)
        savebtn.bind(on_release=self.save)

        keyboard_btn = CustomToggleButton(text='T', default='T', down='T', shorten=True, size_hint=(None, 1), painter = self.painter)
        keyboard_btn.bind(on_release=self.keyboard_input)

        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(self.painter)

        button_layout = GridLayout(cols=6, spacing=5)
        button_layout.add_widget(clearbtn)
        button_layout.add_widget(erasebtn)
        button_layout.add_widget(savebtn)
        button_layout.add_widget(undo_btn)
        button_layout.add_widget(keyboard_btn)

        button_layout.add_widget(self.colorbtn)

        layout.add_widget(button_layout)

        # parent.add_widget(self.painter)
        parent.add_widget(layout)
        return parent

    def keyboard_input(self, obj):
        self.painter.keyboard_mode = not self.painter.keyboard_mode

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
        self.painter.color = get_color_from_hex(color_cycle.next())

    def set_erase(self, obj):
        if self.painter.color == erase_color:
            self.painter.color = self.painter.previous_color
        else:
            self.painter.previous_color = self.painter.color
            self.painter.color = erase_color

    def save(self, obj):
        pass


class ColorButton(Button):
    def __init__(self, **kwargs):
        super(ColorButton, self).__init__(**kwargs)

class CustomToggleButton(ToggleButton):
    def __init__(self, **kwargs):
        super(CustomToggleButton, self).__init__(**kwargs)
        self.down = kwargs['down']
        self.default = kwargs['default']

    def on_press(self):
        if self.state == 'down':
            self.text = self.down
        else:
            self.text = self.default

class ColorToggleButton(Button):
    def __init__(self, **kwargs):
        super(ColorToggleButton, self).__init__(**kwargs)
        self.painter = kwargs['painter']
        # print(self.painter)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = get_color_from_hex('#000080')

     def on_release(self):
       self.painter.color = get_color_from_hex(color_cycle.next())
       self.background_color = self.painter.color

if __name__ == '__main__':
    KivyNoteBookApp().run()
