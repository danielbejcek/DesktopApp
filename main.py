
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.event import EventDispatcher
from HoverButton import HoverBehavior
from kivy.uix.textinput import TextInput
from DataFrame import *
import pandas as pd

# Class that allows transitions between screens.
# Using this we are preventing creating redundant switch screen methods within each class.
class Transition:
    def transition(self, screen_name):
        self.manager.transition = WipeTransition()
        self.manager.transition.duration = 1
        self.manager.current = screen_name

    def home_page(self, instance):
        self.manager.transition.duration = 1
        self.manager.current = "Second"
        self.manager.transition = WipeTransition()


# Custom class HoverButton(original creator: 'Olivier POYEN') fills the role as a highlighter of a button.
# Once mouse is hovering over a specified widget, its custom events (on_enter,on_leave) are fired,
# allowing us to modify the properties of the widget.
class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)

        # Dictionary which consists of keys and values. Each key is a image before being selected with a mouse hover,
        # each value of a key is a image which is highlighted after it has been selected with a mouse hover.
        # Whenever we want to add additional button, that includes a highlight function, we just need to update the path within this dictionary.
        self.images_path = {"Images/inventory_text.png": "Images/inventory_text_selected.png",
                            "Images/import_text.png": "Images/import_text_selected.png",
                            "Images/home_button_icon.png":"Images/home_button_icon_selected.png",
                            "Images/notebook_closed.png":"Images/notebook_closed_selected.png",
                            "Images/notebook_opened.png":"Images/notebook_opened_selected.png",
                            "Images/minus_sign.png":"Images/minus_sign_selected.png",
                            "Images/plus_sign.png":"Images/plus_sign_selected.png",
                            "Images/lock_icon.png":"Images/unlocked_icon_selected.png",
                            "Images/unlocked_icon.png":"Images/lock_icon_selected.png"}

    # "on_button_hover" method loops trough the 'images_path' dictionary and looks for a element that is equal to a instance attribute.
    # In this case it's looking for a background_normal within the "inventory_button" widget. Once it finds a equal string,
    # it changes the source image for a highlighted one.
    def on_button_hover(self, instance):
        for key in self.images_path:
            if instance.background_normal in key:
                instance.background_normal = self.images_path[key]


    # Similar method to the previous one. Once the mouse hover leaves the designated area of a button.
    # It loops trough the dictionary and after it finds a corresponding string, it changes it back to the non-highlighted image.
    def on_button_hover_exit(self, instance):
        for key, value in self.images_path.items():
            if instance.background_normal in value:
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
        Clock.schedule_once(lambda dt: self.transition("Second"), 2)



class MainScreen(Screen, Transition):
    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.inventory_button = HoverButton(
            background_normal="Images/inventory_text.png",
            background_down="Images/inventory_text.png",
            font_size=15,
            size_hint=(.8, 1))

        self.ids.LY2.add_widget(self.inventory_button)
        self.inventory_button.bind(on_enter=self.inventory_button.on_button_hover, on_leave=self.inventory_button.on_button_hover_exit)
        # In order for a transition to work, we need to combine this on_release event with lambda.
        self.inventory_button.bind(on_release=lambda x: self.transition("Third"))



        self.import_button = HoverButton(
            background_normal="Images/import_text.png",
            background_down="Images/import_text.png",
            font_size=15,
            size_hint=(.8, 1))
        self.ids.LY2.add_widget(self.import_button)
        self.import_button.bind(on_enter=self.import_button.on_button_hover, on_leave=self.import_button.on_button_hover_exit)

class InventoryScreen(Screen, Transition):
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)

        self.home_button = HoverButton(
            background_normal="Images/home_button_icon.png",
            background_down="Images/home_button_icon.png",
            size_hint=(.065,.1),
            border=(0,0,0,0),
            pos_hint={"center_x": .93,"top_y": .95})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.ids.LY3.add_widget(self.home_button)

        self.current_state_image = Image(
            source="Images/current_state.png",
            size_hint=(.5, .5),
            pos_hint={"center_x": .16, "center_y": .9})
        self.ids.LY3.add_widget(self.current_state_image)

        self.lock_button = HoverButton(
            background_normal="Images/lock_icon.png",
            background_down="Images/unlocked_icon.png",
            size_hint=(.05, .09),
            border=(0,0,0,0),
            pos_hint={"center_x": .48, "center_y":.1})
        self.lock_button.bind(on_enter=self.lock_button.on_button_hover, on_leave=self.lock_button.on_button_hover_exit)
        self.lock_button.bind(on_release=self.update_components)
        self.ids.LY3.add_widget(self.lock_button)

        self.notebook_button = HoverButton(
            background_normal="Images/notebook_closed.png",
            background_down="Images/notebook_closed.png",
            size_hint=(.04, .1),
            pos_hint={"center_x": .38, "center_y": .91})
        self.notebook_button.bind(on_enter=self.notebook_button.on_button_hover, on_leave=self.notebook_button.on_button_hover_exit)
        self.notebook_button.bind(on_release=self.background_change)
        self.ids.LY3.add_widget(self.notebook_button)
    def update_components(self, instance):
        # Widgets are unlocked.
        if instance.background_normal == "Images/unlocked_icon_selected.png":
            instance.background_normal = "Images/unlocked_icon.png"
            instance.background_down = "Images/lock_icon.png"





        # Widgets are locked.
        elif instance.background_normal == "Images/lock_icon_selected.png":
            instance.background_normal = "Images/lock_icon.png"
            instance.background_down = "Images/unlocked_icon.png"



    # Whenever we load this screen for the first time, "add_widgets" is fired that fills the screen with scrollable database
    # of components and their respective amount. This fucntion is also applied when we return to this screen. Further in the code
    # we will use a "on_leave" function that clears all of the widgets to prevent the widgets from overlapping.
    def on_pre_enter(self, *args):
            self.add_widgets(self.ids.LY4)
            self.ids.LY4.bind(minimum_height=self.ids.LY4.setter('height'))

    # Method that changes visuals and also adds or clears widgets depending on the current notebook status.
    # This method is bound to a button click that traverses between an opened and closed.
    # Whenever we click a respective button and meet a condition thats states "notebook_closed",
    # we fire a "clear_widgets" function that deletes widgets from previous layout and adds new widgets to a new layout.
    def background_change(self, instance):
        if instance.background_normal and instance.background_down == "Images/notebook_closed.png":
            instance.size_hint=(.08,.1)
            instance.background_normal = "Images/notebook_opened.png"
            instance.background_down = "Images/notebook_opened.png"

            self.ids.LY4.clear_widgets()
            self.add_widgets(self.ids.LY5)

        # Same utility only the other way around. We delete widgets from new layout only to fire a "on_pre_enter" function,
        # that brings us back to the first layout with corresponding widgets included.
        elif instance.background_normal and instance.background_down == "Images/notebook_opened.png":
            instance.size_hint=(.04,.1)
            instance.background_normal="Images/notebook_closed.png"
            instance.background_down="Images/notebook_closed.png"

            self.ids.LY5.clear_widgets()
            self.on_pre_enter()

    # Method that creates widgets depending on the current layout. We switch between "notebook_opened" and "notebook_closed".
    # With series of for loops we create a database of warehouse stock. Under first condition, the database is scrollable
    # and set into two columns.
    def add_widgets(self, layer):
        if self.notebook_button.background_normal and self.notebook_button.background_down == "Images/notebook_closed.png":
            for component, amount in zip(components["Komponent"], components["Množství"]):
                self.component_label= Label(
                    text=component,
                    font_size=25,
                    padding=(200,0,0,0),
                    bold=False)

                self.amount_input = Label(
                    text=str(amount),
                    font_size=35,
                    padding=(350, 0, 0, 0),
                    bold=False)

                self.minus_sign = HoverButton(
                    background_normal="Images/minus_sign.png",
                    background_down="Images/minus_sign.png",
                    size_hint=(None, None),
                    width=90,
                    height=80,
                    disabled=False,
                    opacity=1)
                self.minus_sign.bind(on_enter=self.minus_sign.on_button_hover, on_leave=self.minus_sign.on_button_hover_exit)

                self.plus_sign = HoverButton(
                    background_normal="Images/plus_sign.png",
                    background_down="Images/plus_sign.png",
                    size_hint=(None, None),
                    width=80,
                    height=80,
                    disabled=False,
                    opacity=1)
                self.plus_sign.bind(on_enter=self.plus_sign.on_button_hover, on_leave=self.plus_sign.on_button_hover_exit)

                self.previous_amount = Label(
                    text=str(amount),
                    font_size=35,
                    padding=(100, 0, 0, 0),
                    disabled=True)


                layer.add_widget(self.component_label)
                layer.add_widget(self.amount_input)
                layer.add_widget(self.previous_amount)
                layer.add_widget(self.minus_sign)
                layer.add_widget(self.plus_sign)

                for divider in range(5):
                    self.divider_line_2 = Image(
                        source="Images/divider_3.png",
                        size_hint_y=None,
                        size_hint_x=.1,
                        height=2,
                        width=2,
                        fit_mode="fill")
                    layer.add_widget(self.divider_line_2)

        # In the second condition, we create a database into 4 columns to present a general overview of the warehouse stock.
        elif self.notebook_button.background_normal and self.notebook_button.background_down == "Images/notebook_opened.png":
            iteration_count = 0
            for component, amount in zip(components["Komponent"], components["Množství"]):
                self.component_label= Label(
                    text=component,
                    size_hint=(.8,1),
                    font_size=18)

                self.amount_input = Label(
                    text=str(amount),
                    size_hint=(.8,1),
                    font_size=22)
                layer.add_widget(self.component_label)
                layer.add_widget(self.amount_input)
                iteration_count += 1

                # In order to preserve a correct division by "divider_line". We need to add a new variable "iteration_count".
                # This divider is created only after a for loop has iterated twice, leading to a desired result, which is:
                # "Component  -  Amount , Component - Amount" and all of that is then underlined with a divider.
                if iteration_count == 2:
                    for divider in range(4):
                        self.divider_line = Image(
                            source="Images/divider_2.png",
                            size_hint_y=None,
                            height=10,
                            width=3)
                        layer.add_widget(self.divider_line)
                        iteration_count = 0



    # Function that resets the page of all the widgets, allowing us to return to the page without overlapping widgets.
    def on_leave(self, *args):
        self.ids.LY4.clear_widgets()
        self.ids.LY5.clear_widgets()
        self.notebook_button.size_hint = (.04, .1)
        self.notebook_button.background_normal = "Images/notebook_closed.png"
        self.notebook_button.background_down = "Images/notebook_closed.png"


class ImportScreen(Screen, Transition):
    def __init__(self,**kwargs):
        super(ImportScreen, self).__init__(**kwargs)
        pass




class WindowManager(ScreenManager):
    pass

class SaniStore(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="First"))
        sm.add_widget(MainScreen(name="Second"))
        sm.add_widget(InventoryScreen(name="Third"))
        sm.add_widget(ImportScreen(name="Fourth"))
        return sm


if __name__ == "__main__":
    SaniStore().run()
