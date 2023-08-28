
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
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

# Class that allows transitions between screens.
# Using this we are preventing creating redundant switch screen methods within each class.
class Transition:
    def transition(self, direction, screen_name):
        self.manager.transition.direction = direction
        self.manager.current = screen_name

    def home(self, instance):
        self.manager.transition.direction = "right"
        self.manager.current = "Second"



# Custom class HoverButton(original creator: 'Olivier POYEN') fills the role as a highlighter of a button.
# Once mouse is hovering over a specified widget, its custom events (on_enter,on_leave) are fired,
# allowing us to modify the properties of the widget.
class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)

        # Empty dictionary which consists of keys and values. Each key is a image before being selected with a mouse hover.
        # each value of a key is a image which is highlighted after it has been selected with a mouse hover.
        # Whenever we want to add additional button, that includes a highlight function, we just need to update the path within this dictionary.
        self.images_path = {"Images/inventory_text.png": "Images/inventory_text_selected.png",
                            "Images/import_text.png": "Images/import_text_selected.png"}

    # "on_button_hover" method loops trough the 'images_path' dictionary and looks for a element that is equal to a instance atribute.
    # In this case it's looking for a background_normal within the "inventory_button" widget. Once it finds a equal string,
    # it changes the source image for a highlighted one.
    def on_button_hover(self, instance):
        for key in self.images_path:
            if instance.background_normal == key:
                instance.background_normal = self.images_path[key]


    # Similar method to the previous one. Once the mouse hover leaves the designated area of a button.
    # It loops trough the dictionary and after it finds a corresponding string, it changes it back to the non-highlighted image.
    def on_button_hover_exit(self, instance):
        for key, value in self.images_path.items():
            if instance.background_normal == value:
                instance.background_normal = key

class WelcomeScreen(Screen, Transition):
    def __init__(self,  **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

        self.logo_image = Image(
            source="Images/Logo.png",
            size_hint=(1.5,1.5),
            opacity=0,
            pos_hint={"center_x": .5, "center_y": 1})
        self.ids.LY1.add_widget(self.logo_image)
        fade_in_image = Animation(opacity=1, duration=1)
        fade_in_image.start(self.logo_image)

        # In order for this function to perform as inteded, lambda needs to be used here.
        Clock.schedule_once(lambda dt: self.transition("left", "Second"), 1)



class MainScreen(Screen, Transition):
    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.inventory_button = HoverButton(
            background_normal="Images/inventory_text.png",
            background_down="Images/inventory_text.png",
            font_size=15,
            size_hint=(.8, 1),
            on_release=lambda x: self.transition("left", "Third"))
        Clock.schedule_once(self.add_button, 1)
        self.inventory_button.bind(on_enter=self.inventory_button.on_button_hover, on_leave=self.inventory_button.on_button_hover_exit)
        # self.inventory_button.bind(on_release=Transition.transition("left","Third"))



        self.import_button = HoverButton(
            background_normal="Images/import_text.png",
            background_down="Images/import_text.png",
            font_size=15,
            size_hint=(.8, 1))
        self.import_button.bind(on_enter=self.import_button.on_button_hover, on_leave=self.import_button.on_button_hover_exit)



    def add_button(self, instance):
        self.ids.LY2.add_widget(self.inventory_button)
        self.ids.LY2.add_widget(self.import_button)



class InventoryScreen(Screen):
    pass




class WindowManager(ScreenManager):
    pass

class SaniStore(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="First"))
        sm.add_widget(MainScreen(name="Second"))
        sm.add_widget(InventoryScreen(name="Third"))
        return sm


if __name__ == "__main__":
    SaniStore().run()
