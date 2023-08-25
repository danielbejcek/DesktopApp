import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.event import EventDispatcher
from HoverButton import HoverBehavior

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

        self.logo_image = Image(
            source="Images/Logo.png",
            size_hint=(1.5,1.5),
            opacity=0,
            pos_hint={"center_x": .5, "center_y": 1})
        self.ids.LY1.add_widget(self.logo_image)
        fade_in_image = Animation(opacity=1, duration=1)
        fade_in_image.start(self.logo_image)
        Clock.schedule_once(self.switch_screen, 3)

    def switch_screen(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = "Second"

# Custom class HoverButton(original creator: 'Olivier POYEN') fills the role as a highlighter of a button,
# once mouse is hovering over a specified widget, its custom events (on_enter,on_leave) are fired,
# allowing us to modify the properties of the widget.
class HoverButton(Button, HoverBehavior):
    def on_button_hover(self, instance):
        instance.background_normal = "Images/inventory_text_selected.png"

    def on_button_hover_exit(self, instance):
        instance.background_normal = "Images/inventory_text.png"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)

        self.inventory_button = HoverButton(
            background_normal="Images/inventory_text.png",
            background_down="Images/inventory_text.png",
            font_size=15,
            size_hint=(.8, .8),
            pos_hint={"center_x": .4, "center_y": 1})
        self.inventory_button.bind(on_enter=self.inventory_button.on_button_hover, on_leave=self.inventory_button.on_button_hover_exit)
        Clock.schedule_once(self.add_button, 1)

    def add_button(self, instance):
        self.ids.LY2.add_widget(self.inventory_button)













class WindowManager(ScreenManager):
    pass

class SaniStore(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="First"))
        sm.add_widget(MainScreen(name="Second"))
        return sm

if __name__ == "__main__":
    SaniStore().run()
