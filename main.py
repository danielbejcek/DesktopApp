import os
import sys
if sys.__stdout__ is None or sys.__stderr__ is None:
    os.environ['KIVY_NO_CONSOLELOG'] = '1'
import kivy
import pandas as pd
import tabula
import io
import functools
from fpdf import FPDF
from PyPDF2 import PdfMerger
from kivy.config import Config
from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.graphics import Line
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from kivy.animation import Animation
from HoverButton import HoverBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.textinput import TextInput
from plyer import filechooser


""" Absolute paths to relevant data/folders."""
main_script_directory = os.path.abspath(os.path.dirname(__file__))
csv_file_path = os.path.join(main_script_directory, "Components_data.csv")
lucida_font_path = r"C:\Windows\Fonts\l_10646.ttf"
images_directory = os.path.join(main_script_directory, "Images")
pdf_component_directory = os.path.join(main_script_directory, "PDF Component folder")
kivy_file_path = os.path.join(main_script_directory,"sanistore.kv")
Builder.load_file(kivy_file_path)

"""
Class that allows transitions between screens.
Using this we are preventing creating redundant switch screen methods within each class.
"""
class Transition:
    def transition(self, screen_name):
        self.manager.transition = WipeTransition()
        self.manager.transition.duration = 1
        self.manager.current = screen_name

    def home_page(self, instance):
        self.manager.transition.duration = 1
        self.manager.current = "Second"
        self.manager.transition = WipeTransition()

"""
Custom class HoverButton(original creator: 'Olivier POYEN') fills the role as a highlighter of a button.
Once mouse is hovering over a specified widget, its custom events (on_enter,on_leave) are fired,
allowing us to modify the properties of the widget.
"""
class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)

        """
        Dictionary which consists of keys and values. Each key is a image before being selected with a mouse hover,
        each value of a key is a image which is highlighted after it has been selected with a mouse hover.
        Whenever we want to add additional button, that includes a highlight function, we just need to update the path within this dictionary.
        """
        self.images_path = {f"{images_directory}/inventory_text.png": f"{images_directory}/inventory_text_selected.png",
                            f"{images_directory}/import_text.png": f"{images_directory}/import_text_selected.png",
                            f"{images_directory}/export_text.png":f"{images_directory}/export_text_selected.png",
                            f"{images_directory}/exit_button.png":f"{images_directory}/exit_button_selected.png",
                            f"{images_directory}/home_button_icon.png":f"{images_directory}/home_button_icon_selected.png",
                            f"{images_directory}/notebook_closed.png":f"{images_directory}/notebook_closed_selected.png",
                            f"{images_directory}/notebook_opened.png":f"{images_directory}/notebook_opened_selected.png",
                            f"{images_directory}/minus_sign.png":f"{images_directory}/minus_sign_selected.png",
                            f"{images_directory}/plus_sign.png":f"{images_directory}/plus_sign_selected.png",
                            f"{images_directory}/lock_icon.png":f"{images_directory}/unlocked_icon_selected.png",
                            f"{images_directory}/unlocked_icon.png":f"{images_directory}/lock_icon_selected.png",
                            f"{images_directory}/pencil_edit.png":f"{images_directory}/pencil_icon_selected.png",
                            f"{images_directory}/closed_folder.png":f"{images_directory}/opened_folder.png",
                            f"{images_directory}/arrow_pick.png":f"{images_directory}/arrow_pick_selected.png",
                            f"{images_directory}/back_arrow_icon.png":f"{images_directory}/back_arrow_icon_selected.png",
                            f"{images_directory}/expand_arrow.png":f"{images_directory}/expand_arrow_selected.png",
                            f"{images_directory}/closed_box.png":f"{images_directory}/closed_box_selected.png",
                            f"{images_directory}/return_box.png":f"{images_directory}/return_box_selected.png",
                            f"{images_directory}/ship_box.png":f"{images_directory}/ship_box_selected.png",
                            f"{images_directory}/select_pdf_button.png":f"{images_directory}/select_pdf_button_selected.png",
                            f"{images_directory}/select_component_button.png":f"{images_directory}/select_component_button_selected.png",
                            f"{images_directory}/pdf_merge_icon.png":f"{images_directory}/pdf_merge_icon_selected.png"}

    """
    on_button_hover" method loops trough the 'images_path' dictionary and looks for a element that is equal to a instance attribute.
    In this case it's looking for a background_normal within the "inventory_button" widget. Once it finds a equal string,
    it changes the source image for a highlighted one.
    """
    def on_button_hover(self, instance):
        for key in self.images_path:
            if instance.background_normal in key:
                instance.background_normal = self.images_path[key]


    """
    Similar method to the previous one. Once the mouse hover leaves the designated area of a button.
    It loops trough the dictionary and after it finds a corresponding string, it changes it back to the non-highlighted image.
    """
    def on_button_hover_exit(self, instance):
        for key, value in self.images_path.items():
            if instance.background_normal in value:
                instance.background_normal = key

class WelcomeScreen(Screen, Transition):
    def __init__(self,  **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

        self.logo_image = Image(
            source=f"{images_directory}/Logo.png",
            size_hint=(1.5,1.5),
            opacity=0,
            pos_hint={"center_x": .5, "center_y": 1})
        self.ids.LY1.add_widget(self.logo_image)
        fade_in_image = Animation(opacity=1, duration=1.5)
        fade_in_image.start(self.logo_image)
        # In order for this function to perform as inteded, lambda needs to be used here.
        Clock.schedule_once(lambda dt: self.transition("Second"), 4)

class MainScreen(Screen, Transition):
    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.inventory_button = HoverButton(
            background_normal=f"{images_directory}/inventory_text.png",
            background_down=f"{images_directory}/inventory_text.png",
            pos_hint={"center_x": .2, "center_y": .9},
            size_hint=(.28, .1),
            border=(0, 0, 0, 0))
        self.inventory_button.bind(on_enter=self.inventory_button.on_button_hover, on_leave=self.inventory_button.on_button_hover_exit)
        # In order for a transition to work, we need to combine this on_release event with lambda.
        self.inventory_button.bind(on_release=lambda screen: self.transition("Third"))

        self.export_button = HoverButton(
            background_normal=f"{images_directory}/export_text.png",
            background_down=f"{images_directory}/export_text.png",
            pos_hint={"center_x": .162, "center_y": .8},
            size_hint=(.28, .1),
            border=(0, 0, 0, 0))
        self.export_button.bind(on_enter=self.export_button.on_button_hover, on_leave=self.export_button.on_button_hover_exit)
        self.export_button.bind(on_release=lambda screen: self.transition("Fifth"))

        self.import_button = HoverButton(
            background_normal=f"{images_directory}/import_text.png",
            background_down=f"{images_directory}/import_text.png",
            size_hint=(.28, .1),
            pos_hint={"center_x": .154, "center_y": .7},
            border=(0, 0, 0, 0))
        self.import_button.bind(on_enter=self.import_button.on_button_hover, on_leave=self.import_button.on_button_hover_exit)
        self.import_button.bind(on_release=lambda screen: self.transition("Fourth"))

        self.exit_button = HoverButton(
            background_normal=f"{images_directory}/exit_button.png",
            background_down=f"{images_directory}/exit_button.png",
            size_hint=(.06, .095),
            pos_hint={"center_x": .94, "center_y": .09},
            border=(0, 0, 0, 0))
        self.exit_button.bind(on_enter=self.exit_button.on_button_hover, on_leave=self.exit_button.on_button_hover_exit)
        self.exit_button.bind(on_release=self.exit_app)

        self.ids.LY2.add_widget(self.inventory_button)
        self.ids.LY2.add_widget(self.export_button)
        self.ids.LY2.add_widget(self.import_button)
        self.ids.LY2.add_widget(self.exit_button)

    def exit_app(self, instance):
        App.get_running_app().stop()

class InventoryScreen(Screen, Transition):
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)

        self.home_button = HoverButton(
            background_normal=f"{images_directory}/home_button_icon.png",
            background_down=f"{images_directory}/home_button_icon.png",
            size_hint=(.06,.095),
            border=(0,0,0,0),
            pos_hint={"center_x": .94,"center_y": .09})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.ids.LY3.add_widget(self.home_button)

        self.current_state_image = Image(
            source=f"{images_directory}/current_state.png",
            size_hint=(.3, .5),
            pos_hint={"center_x": .175, "center_y": .92})
        self.ids.LY3.add_widget(self.current_state_image)

        self.notebook_button = HoverButton(
            background_normal=f"{images_directory}/notebook_closed.png",
            background_down=f"{images_directory}/notebook_closed.png",
            background_disabled_normal=f"{images_directory}/notebook_closed_disabled.png",
            size_hint=(.04, .1),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .38, "center_y": .91})
        self.notebook_button.bind(on_enter=self.notebook_button.on_button_hover, on_leave=self.notebook_button.on_button_hover_exit)
        self.notebook_button.bind(on_release=self.background_change)
        self.ids.LY3.add_widget(self.notebook_button)

        self.lock_button = HoverButton(
            background_normal=f"{images_directory}/lock_icon.png",
            background_down=f"{images_directory}/unlocked_icon.png",
            background_disabled_normal=f"{images_directory}/lock_icon_disabled.png",
            size_hint=(.05, .09),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .45, "center_y": .91})
        self.lock_button.bind(on_enter=self.lock_button.on_button_hover, on_leave=self.lock_button.on_button_hover_exit)
        self.lock_button.bind(on_release=self.update_components)
        self.ids.LY3.add_widget(self.lock_button)

    """
    Method that controls the state of the "lock_button" widget. Once the background image of the lock_button is changed,
    we are firing widgets depending on the background. In order for the widgets to display properly in the UI, once the state is changed,
    all widgets are deleted and corresponding widgets take place immediately.
    """
    def update_components(self, instance):
        # Widgets are unlocked.
        if instance.background_normal == f"{images_directory}/unlocked_icon_selected.png":
            self.ids.LY4.clear_widgets()
            self.notebook_button.disabled = True
            instance.background_normal = f"{images_directory}/unlocked_icon.png"
            instance.background_down = f"{images_directory}/lock_icon.png"
            self.add_widgets(self.ids.LY4)

            with open(csv_file_path, 'rb') as f:
                contents = f.read()
            self.df = pd.read_csv(io.BytesIO(contents), encoding='utf-8')
            # self.df = pd.read_csv(csv_file_path, encoding='utf-8')

            """ 
            'final_count' list is filled with 0 for each component in the dataframe.
            Changes made to the component's amount are stored here and every component is under a corresponding index.
            When user is finished with the changes by 'locking' the interface, 'save_data' method is fired, which updates
            the original .csv database. Upon every return to 'unlocked' interface, new 'final_count' list with zero values is instantiated.
            """
            self.final_count = [0 for _ in self.df["Mnozstvi"]]

        # Widgets are locked.
        if instance.background_normal == f"{images_directory}/lock_icon_selected.png":
            self.save_data(self.final_count)
            self.ids.LY4.clear_widgets()
            self.notebook_button.disabled = False
            instance.background_normal = f"{images_directory}/lock_icon.png"
            instance.background_down = f"{images_directory}/unlocked_icon.png"
            self.add_widgets(self.ids.LY4)

    """
    Whenever we load this screen for the first time, "add_widgets" is fired that fills the screen with scrollable database
    of components and their respective amount. This fucntion is also applied when we return to this screen. Further in the code
    we will use a "on_leave" function that clears all of the widgets to prevent the widgets from overlapping.
    """
    def on_pre_enter(self, *args):
        with open(csv_file_path, 'rb') as f:
            contents = f.read()
        self.df = pd.read_csv(io.BytesIO(contents), encoding='utf-8')
        self.add_widgets(self.ids.LY4)

    """
    Method that changes visuals and also adds or clears widgets depending on the current notebook status.
    This method is bound to a button click that traverses between an opened and closed.
    Whenever we click a respective button and meet a condition thats states "notebook_closed",
    we fire a "clear_widgets" function that deletes widgets from previous layout and adds new widgets to a new layout.
    """
    def background_change(self, instance):
        if instance.background_normal and instance.background_down == f"{images_directory}/notebook_closed.png":
            instance.size_hint=(.08,.1)
            instance.background_normal = f"{images_directory}/notebook_opened.png"
            instance.background_down = f"{images_directory}/notebook_opened.png"
            self.ids.LY4.clear_widgets()
            self.add_widgets(self.ids.LY5)

            """
            Same utility only the other way around. We delete widgets from new layout only to fire a "on_pre_enter" function,
            that brings us back to the first layout with corresponding widgets included.
            """
        elif instance.background_normal and instance.background_down == f"{images_directory}/notebook_opened.png":
            instance.size_hint=(.04,.1)
            instance.background_normal=f"{images_directory}/notebook_closed.png"
            instance.background_down=f"{images_directory}/notebook_closed.png"
            self.ids.LY5.clear_widgets()
            self.on_pre_enter()

    """
    Method that creates widgets depending on the current layout. We switch between "notebook_opened" and "notebook_closed".
    With series of for loops we create a database of warehouse stock. Under first condition, the database is scrollable
    and set into two columns.

    "add_widgets" method now also servers as a bridge between locked and unlocked status of the stock.
    Whenever a lock icon is clicked and becomes unlocked, additional widgets are instantiated ("minus_sign", "plus_sign", "previous_amount").
    These widgets serve as a alternative mode that allows us to manually change the values on each component.

    Unfortunately we face a necessary redundancy in the upcoming code, in each for loop widgets are duplicated to prevent an error:
    "WidgetException: Cannot add <kivy.uix.label.Label object at 0x...>, it already has a parent".
    """
    def add_widgets(self, layer):

        """ Inteface is locked."""
        if self.notebook_button.background_normal and self.notebook_button.background_down == f"{images_directory}/notebook_closed.png":
            if self.lock_button.background_normal == f"{images_directory}/lock_icon.png":
                self.lock_button.disabled = False

                """ We created an empty list for later use."""
                self.new_amount_list = []

                for index, (component, amount) in enumerate(zip(self.df["Komponent"], self.df["Mnozstvi"])):

                    self.component_label= Label(
                        text=component,
                        font_size=20,
                        padding=(100,0,0,0),
                        bold=False)

                    self.amount_input = Label(
                        text=str(amount),
                        font_size=35,
                        padding=(60, 0, 0, 0),
                        bold=False)

                    self.minus_sign = HoverButton(
                        background_disabled_normal=f"{images_directory}/minus_sign_disabled.png",
                        size_hint=(None, None),
                        width=90,
                        height=80,
                        disabled=True,
                        padding=(0,0,0,0),
                        opacity=.2)

                    self.plus_sign = HoverButton(
                        background_disabled_normal=f"{images_directory}/plus_sign_disabled.png",
                        size_hint=(None, None),
                        width=80,
                        height=80,
                        disabled=True,
                        opacity=.2)

                    self.value_input_button = HoverButton(
                        background_disabled_normal=f"{images_directory}/pencil_edit.png",
                        border=(0, 0, 0, 0),
                        disabled=True,
                        opacity=(.05),
                        size_hint=(.25, .01),
                        padding=(0, 0, 50, 0))

                    """ Setting the number of columns explicitly to match the positioning of widgets."""
                    self.ids.LY4.cols = 5
                    self.ids.SW1.size_hint = (.484, .8)
                    layer.add_widget(self.component_label)
                    layer.add_widget(self.amount_input)
                    layer.add_widget(self.minus_sign)
                    layer.add_widget(self.plus_sign)
                    layer.add_widget(self.value_input_button)

                    for divider in range(5):
                        self.divider_line_3 = Image(
                            source=f"{images_directory}/divider_3.png",
                            size_hint_y=None,
                            size_hint_x=.1,
                            height=2,
                            width=2,
                            fit_mode="fill")
                        layer.add_widget(self.divider_line_3)

            """
            Condition that lets us set specific widgets from disabled=True to False, alowing us to use the "minus_sign" and "plus_sign" widgets
            to control the amount of the components. This condition is active only if the lock icon is pressed and becomes unlocked.
            """
            if self.lock_button.background_normal == f"{images_directory}/unlocked_icon.png":

                self.text_inputs_list = []

                """ Interface is unlocked."""
                for index, (component, amount) in enumerate(zip(self.df["Komponent"], self.df["Mnozstvi"])):

                    self.component_label_2 = Label(
                        text=component,
                        font_size=20,
                        padding=(175, 0, 0, 0),
                        bold=False)

                    self.amount_input_2 = Label(
                        text=str(amount),
                        font_size=35,
                        padding=(310, 0, 10, 0),
                        bold=False)

                    self.minus_sign_2 = HoverButton(
                        background_normal=f"{images_directory}/minus_sign.png",
                        background_down=f"{images_directory}/minus_sign.png",
                        size_hint=(None, None),
                        width=90,
                        height=80,
                        disabled=False,
                        opacity=1,
                        on_release=self.decrement_value)
                    self.minus_sign_2.bind(on_enter=self.minus_sign_2.on_button_hover, on_leave=self.minus_sign_2.on_button_hover_exit)
                    self.minus_sign_2.my_id = index

                    self.plus_sign_2 = HoverButton(
                        background_normal=f"{images_directory}/plus_sign.png",
                        background_down=f"{images_directory}/plus_sign.png",
                        size_hint=(None, None),
                        width=80,
                        height=80,
                        disabled=False,
                        opacity=1,
                        on_release=self.increment_value)
                    self.plus_sign_2.bind(on_enter=self.plus_sign_2.on_button_hover, on_leave=self.plus_sign_2.on_button_hover_exit)
                    self.plus_sign_2.my_id = index

                    """
                    "new_amount" Label is a widget that the user can modify according to his needs with the use of "plus_sign_2", "minus_sign_2" and "value_input_button" buttons.
                    Each iteration of this Label is then added to a list to help us connect it with corresponding components.
                    """
                    self.new_amount = Label(
                        text=str(0),
                        font_size=30,
                        padding=(110, 0, 0, 0),
                        disabled=False,
                        color=(1,1,1,0),
                        bold=True)
                    self.new_amount_list.append(self.new_amount)

                    """ Widget that allows the user to create a text_input field, which is automatically focused."""
                    self.value_input_button = HoverButton(
                        background_normal=f"{images_directory}/pencil_edit.png",
                        background_down=f"{images_directory}/pencil_edit.png",
                        border=(0, 0, 0, 0),
                        opacity=(.6),
                        size_hint=(.35, .01),
                        padding=(0, 0, 0, 0))
                    self.value_input_button.bind(on_enter=self.value_input_button.on_button_hover, on_leave=self.value_input_button.on_button_hover_exit)
                    self.value_input_button.bind(on_release=self.button_to_text)
                    self.value_input_button.my_id = index

                    """
                    Creating a empty text_input field in which user can enter numerical value.
                    After user validates the field with an press of a 'enter' button. Value from the text field is transfered into "new_amount" widget.
                    After validation, text field becomes disabled and hidden.
                    """
                    self.text_value_input = TextInput(
                        background_active=f"{images_directory}/border_icon.png",
                        background_disabled_normal=f"{images_directory}/border_icon.png",
                        multiline=False,
                        border=(0, 0, 0, 0),
                        halign="right",
                        input_filter="int",
                        font_size=30,
                        cursor_color=(0, 0, 0, 1),
                        foreground_color=(0, 0, 0, 1),
                        opacity=(0),
                        disabled=True,
                        size_hint=(.6, .2),
                        padding=(10, 22),
                        on_text_validate=self.custom_text_validate)
                    self.text_inputs_list.append(self.text_value_input)
                    self.text_value_input.my_id = index
                    self.text_value_input.bind(focus=self.unfocus_text_input)

                    """Custom configuration of a layout to fit widgets correctly."""
                    self.ids.SW1.size_hint = (.55,.8)
                    self.ids.LY4.cols = 7
                    layer.add_widget(self.component_label_2)
                    layer.add_widget(self.amount_input_2)
                    layer.add_widget(self.new_amount)
                    layer.add_widget(self.minus_sign_2)
                    layer.add_widget(self.plus_sign_2)
                    layer.add_widget(self.value_input_button)
                    layer.add_widget(self.text_value_input)

                    iteration_count = 0
                    for divider in range(7):
                        iteration_count += 1
                        self.divider_line_2 = Image(
                            source=f"{images_directory}/divider_3.png",
                            size_hint_y=None,
                            size_hint_x=.1,
                            height=2,
                            width=2,
                            fit_mode="fill")
                        layer.add_widget(self.divider_line_2)
                        if iteration_count > 6:
                            self.divider_line_2.opacity = (0)

            """
            In the second condition, we create a database into 4 columns to present a general overview of the warehouse stock.
            We are also setting the "lock_button.disabled" to True. Meaning once we are in this overview, we are not able to modify the values.
            """
        elif self.notebook_button.background_normal and self.notebook_button.background_down == f"{images_directory}/notebook_opened.png":
            self.lock_button.disabled = True
            iteration_count = 0
            """ Interface is in a notebook overview. """
            for component, amount in zip(self.df["Komponent"], self.df["Mnozstvi"]):
                self.component_label= Label(
                    text=component,
                    size_hint=(.8,1),
                    font_size=17)

                self.amount_input_3 = Label(
                    text=str(amount),
                    size_hint=(.8,1),
                    font_size=22,)

                """ Once a certain amount of components is bellow critical number, value will now be displayed in red color."""
                if amount < 11:
                    self.amount_input_3.color=(1,0,0,1)

                layer.add_widget(self.component_label)
                layer.add_widget(self.amount_input_3)
                iteration_count += 1

                """
                In order to preserve a correct division by "divider_line". We need to add a new variable "iteration_count".
                This divider is created only after a for loop has iterated twice, leading to a desired result, which is:
                "Component  -  Amount , Component - Amount" and all of that is then underlined with a divider.
                """
                if iteration_count == 2:
                    for divider in range(4):
                        self.divider_line = Image(
                            source=f"{images_directory}/divider_2.png",
                            size_hint_y=None,
                            height=10,
                            width=5)
                        layer.add_widget(self.divider_line)
                        iteration_count = 0

    """
    Method that allows us to change values of a "new_amount" Label. Each widget has its index as a 'Primary key',
    to help us navigate between the iterations and control which component's value we want to change.
    We are directly accessing an item in the "new_amount_list" which has been appended from the "new_amount" Label.
    With the use of "index" variable we are able to connect the specific item in the list to a widget created by the loop.
    Change of values in the "self.new_amount.text" Label is done by modifying the list items, not by accessing the "self.new_amount" widget directly.
    """
    def increment_value(self, index_id):
        index_plus = index_id.my_id
        value = "plus"
        if self.new_amount_list[index_plus].text == "":
            self.new_amount_list[index_plus].text = str(0)
        self.new_amount_list[index_plus].text = str(int(self.new_amount_list[index_plus].text) + 1)
        self.final_count[index_plus] += 1
        self.set_label_color(index_plus)

    def decrement_value(self, index_id):
        index_minus = index_id.my_id
        value = "minus"
        if self.new_amount_list[index_minus].text == "":
            self.new_amount_list[index_minus].text = str(0)
        self.new_amount_list[index_minus].text = str(int(self.new_amount_list[index_minus].text) - 1)
        self.final_count[index_minus] -= 1
        self.set_label_color(index_minus)

    """Method that allows us to display and immediately focus a new text input field."""
    def button_to_text(self, index_id):
        button_index = index_id.my_id
        self.text_inputs_list[button_index].disabled = False
        self.text_inputs_list[button_index].opacity = 1
        self.text_inputs_list[button_index].focused = True
        self.text_inputs_list[button_index].text = ""

    """
    After pressing enter, while text input widget is active, this method will transfer the value into the "new_amount" widget.
    To maintain proper functionality, if the "new_amount" value has not yet been modified (value = 0), new value will now be now added.
    Although if user decides to correct his previous value, the "new_amount" will be reset and equal to zero.
    """
    def custom_text_validate(self, index_id):
        value = "custom"
        self.text_index = index_id.my_id
        self.final_count[self.text_index] = 0
        self.text_inputs_list[self.text_index].disabled = True
        self.text_inputs_list[self.text_index].focused = False
        self.text_inputs_list[self.text_index].opacity = 0
        self.user_amount = self.text_inputs_list[self.text_index].text

        self.new_amount_list[self.text_index].text = str(self.user_amount)
        if self.text_inputs_list[self.text_index].text == "":
            self.user_amount = 0

        self.set_label_color(self.text_index)
        self.count_values(self.text_index, value)

    """
    To prevent the user to make changes in the database while still 'unlocked interface', we created an empty list "self.final_count".
    We want all the changes to the database occur only after we exit from the unlocked interface and enter into a locked interface (by clicking the lock_icon).
    Instead of making changes directly to the core database, we modify values inside the "self.final_count".
    Once user clicks a "plus_sign", "minus_sign" or "text_input_button", the list's components are updated on a corresponding index.
    """
    def count_values(self, index, value):
        if value == "plus":
            self.final_count[index] += 1

        elif value == "minus":
            self.final_count[index] -= 1

        elif value == "custom":
            self.final_count[index] += int(self.user_amount)

    """ Method which allows us to unfocus and disable a text input field as soon as it's not focused."""
    def unfocus_text_input(self, index_id, value):
        index = index_id.my_id
        if not value:
            self.text_inputs_list[index].disabled = True
            self.text_inputs_list[index].opacity = 0

    """
    Method that checks for the amount of components. As soon as value falls bellow 0, the color of the value turns red.
    Other way around if the value is above zero, the color turns green.
    """
    def set_label_color(self, index):
        if self.new_amount_list[index].text > str(0):
            self.new_amount_list[index].color = (0, 1, 0, 1)
        elif self.new_amount_list[index].text < str(0):
            self.new_amount_list[index].color = (1, 0, 0, 1)
        else:
            self.new_amount_list[index].color = (1, 1, 1, 0)

    """
    Method that is fired whenever the user clicks on "lock_icon" button to store the changed data into the database.
    We loop trough the CSV file and merge the pending changes in "self.final_count" list into the default database.
    """
    def save_data(self, final_count):
        for index, amount in enumerate(self.df["Mnozstvi"]):
            self.df.at[index, "Mnozstvi"] += self.final_count[index]
        self.df.to_csv(csv_file_path, encoding='utf-8', index=False)

    """ Function that cleans the page of all the widgets, allowing us to return to the page without overlapping widgets."""
    def on_leave(self, *args):
        self.ids.LY4.clear_widgets()
        self.ids.LY5.clear_widgets()
        self.notebook_button.size_hint = (.04, .1)
        self.notebook_button.background_normal = f"{images_directory}/notebook_closed.png"
        self.notebook_button.background_down = f"{images_directory}/notebook_closed.png"
        self.lock_button.background_normal = f"{images_directory}/lock_icon.png"
        self.lock_button.background_down = f"{images_directory}/unlocked_icon.png"
        self.notebook_button.disabled = False

class ImportScreen(Screen, Transition):
    pdf_paths_list = ListProperty([])
    component_file_text = StringProperty("")
    component_path = None

    def __init__(self,**kwargs):
        super(ImportScreen, self).__init__(**kwargs)
        self.anim = Animation(opacity=1, duration=.1)
        self.anim_fade = Animation(opacity=0, duration=1)

        self.home_button = HoverButton(
            background_normal=f"{images_directory}/home_button_icon.png",
            background_down=f"{images_directory}/home_button_icon.png",
            size_hint = (.06, .095),
            border=(0, 0, 0, 0),
            pos_hint = {"center_x": .94, "center_y": .09})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.ids.LY6.add_widget(self.home_button)

        self.select_pdf = HoverButton(
            background_normal=f"{images_directory}/select_pdf_button.png",
            background_down=f"{images_directory}/select_pdf_button.png",
            border=(0, 0, 0, 0),
            size_hint=(1,.1),
            pos_hint={"center_x": .55, "center_y": .75})
        self.select_pdf.bind(on_enter=self.select_pdf.on_button_hover, on_leave=self.select_pdf.on_button_hover_exit)
        self.select_pdf.bind(on_release=self.choose_pdf_file)
        self.select_pdf.bind(on_release=lambda clear_list: self.pdf_paths_list.clear())
        self.select_pdf.bind(on_release=lambda clear_layout: self.ids.LY55.clear_widgets())
        self.ids.LY6.add_widget(self.select_pdf)

        self.select_component = HoverButton(
            background_normal=f"{images_directory}/select_component_button.png",
            background_down=f"{images_directory}/select_component_button.png",
            border=(0, 0, 0, 0),
            size_hint=(1, .1),
            pos_hint={"center_x": .55, "center_y": .65})
        self.select_component.bind(on_enter=self.select_component.on_button_hover, on_leave=self.select_component.on_button_hover_exit)
        self.select_component.bind(on_release=self.choose_component_file)
        self.ids.LY6.add_widget(self.select_component)

        self.merge_pdf = HoverButton(
            background_normal=f"{images_directory}/pdf_merge_icon.png",
            background_down=f"{images_directory}/pdf_merge_icon_down.png",
            background_disabled_normal=f"{images_directory}/pdf_merge_icon_disabled.png",
            border=(0, 0, 0, 0),
            size_hint=(.06, .09),
            pos_hint={"center_x": .94, "center_y": .9})
        self.merge_pdf.bind(on_enter=self.merge_pdf.on_button_hover, on_leave=self.merge_pdf.on_button_hover_exit)
        self.merge_pdf.bind(on_release=self.merge_pdf_files)
        self.ids.LY6.add_widget(self.merge_pdf)

        self.merge_img = Image(
            source=f"{images_directory}/merge_success_img.png",
            pos_hint={"center_x": .85, "center_y": .6},
            size_hint=(.3, .3),
            border=(0, 0, 0, 0),
            opacity=0)
        self.ids.LY6.add_widget(self.merge_img)

        self.error_pdf_img = Image(
            source=f"{images_directory}/error_pdf.png",
            pos_hint={"center_x": .28, "center_y": .8},
            size_hint=(.3, .3),
            allow_stretch=True,
            border=(0, 0, 0, 0),
            opacity=0)
        self.ids.LY6.add_widget(self.error_pdf_img)

        self.error_component_img = Image(
            source=f"{images_directory}/error_component.png",
            pos_hint={"center_x": .28, "center_y": .49},
            size_hint=(.3, .3),
            allow_stretch=True,
            border=(0, 0, 0, 0),
            opacity=0)
        self.ids.LY6.add_widget(self.error_component_img)

    """
    Two methods bellow allow us to choose .pdf files that will later be merged together. 
    Once user selects a .pdf file, lambda function is fired to call a "handle_selection" method. 
    Within the lambda function, two arguments are passed: "selection" and "method".
    "Selection" is the selected file, while "method" keyword is the deciding argument.
    With use of the "method" keyword, we are able to differentiate which of the two methods called "handle_selection".
    User is able to select multiple .pdf files which are then appended to 'pdf_paths_list', 
    from which Labels with respective name are created.
    """
    def choose_pdf_file(self, instance):

        self.pdf_path = filechooser.open_file(
            title="Select a file ...",
            multiple=True,
            filters=[("PDF Files", "*.pdf")],
            on_selection=lambda selection: self.handle_selection(selection, method="pdf"))

        if self.pdf_path:
            for path in self.pdf_path:
                self.pdf_paths_list.append(path)


        self.anim = Animation(opacity=1, duration=1)
        self.anim.start(self.ids.merge_docs)

        pos_y =  .42
        for pdf in self.pdf_paths_list:
            self.pdf_text_label = Label(
                text=os.path.basename(pdf),
                pos_hint={"center_x": .29, "center_y": pos_y},
                size_hint=(.2, .2),
                font_size=22)
            self.ids.LY55.add_widget(self.pdf_text_label)
            pos_y -= .03

    def choose_component_file(self, instance):
        self.component_path = filechooser.open_file(
            title="Select a file ...",
            filters=[("PDF Files", "*.pdf")],
            on_selection=lambda selection: self.handle_selection(selection, method="component"))

    """
    After "handle_selection" method is called, it recieves an keyword argument called "method".
    Based on the recieved keyword arguments from the two methods above, it differentiates between the IF conditions and
    transfers the "self.file_name" into the StringProperty accordingly. Allowing the Label to appear with the correct
    selected file's name.
    """
    def handle_selection(self, selection, method):
        if selection:
            # Selecting only the file name, seperating the rest of the path.
            self.file_name = os.path.basename(selection[0])

            if method == "pdf":
                pass

            if method == "component":
                self.component_file_text = self.file_name

    def merge_pdf_files(self, instance):
        merger = PdfMerger()
        if self.component_path is not None:
            self.pdf_component = self.component_path

        else:
            """ If user closes the file browser window without selecting a file, pdf_component is no longer None, but becomes an empty list instead."""
            self.pdf_component = None

        if self.pdf_paths_list != [] and self.pdf_component is not None and self.pdf_component != []:
            for pdf in self.pdf_paths_list:
                merger.append(pdf)
            merger.append(self.pdf_component[0])

            user_home = os.path.expanduser("~")
            desktop_path = os.path.join(user_home, "Desktop")
            output_pdf_path = os.path.join(desktop_path, f"Komplet - {self.component_file_text}")
            merger.write(output_pdf_path)
            merger.close()
            self.anim.start(self.merge_img)
            self.anim.bind(on_complete=self.stop_anim)

        if self.pdf_paths_list == []:
            self.anim.start(self.error_pdf_img)
            self.anim.bind(on_complete=self.stop_anim)

        if self.pdf_component is None or self.pdf_component == []:
            self.anim.start(self.error_component_img)
            self.anim.bind(on_complete=self.stop_anim)
    def stop_anim(self, dt, instance):
        Clock.schedule_once(lambda dt: self.anim_fade.start(self.error_component_img),1)
        Clock.schedule_once(lambda dt: self.anim_fade.start(self.error_pdf_img),1)
        Clock.schedule_once(lambda dt: self.anim_fade.start(self.merge_img), 3)

    def on_leave(self, *args):
        self.ids.LY55.clear_widgets()
        self.pdf_paths_list.clear()
        self.component_file_text = ""
        self.component_path = None

class ExportScreen(Screen, Transition):
    """
    'data_store' is a variable that helps us control the data when screens are being switched.
    When set to 'False', all of the data generated with button widgets will be deleted when we leave the ExportScreen.
    When set to 'True', relevant data for the user will be kept in order to access them when the user decides to
    go back to the ExportScreen to modify his selection.
    """
    data_store = False
    def __init__(self, **kwargs):
        super(ExportScreen, self).__init__(**kwargs)
        self.anim = Animation(opacity=1, duration=.2)
        self.anim_fade = Animation(opacity=0, duration=1)

        self.error_img = Image(
            source=f"{images_directory}/error_number.png",
            allow_stretch=True,
            pos_hint={"center_x": .68, "center_y": .88},
            size_hint=(.2, .2),
            opacity=0)
        self.ids.LY8.add_widget(self.error_img)

        with open(csv_file_path, 'rb') as f:
            contents = f.read()
        self.df = pd.read_csv(io.BytesIO(contents), encoding='utf-8')

        self.transfered_dict = {}

        self.home_button = HoverButton(
            background_normal=f"{images_directory}/home_button_icon.png",
            background_down=f"{images_directory}/home_button_icon.png",
            size_hint=(.06, .095),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .94, "center_y": .09})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.home_button.bind(on_release=lambda button: (setattr(ExportScreen,"data_store",False)))
        self.ids.LY8.add_widget(self.home_button)

        self.next_page = HoverButton(
            background_normal=f"{images_directory}/closed_box.png",
            background_down=f"{images_directory}/closed_box.png",
            size_hint=(.07, .125),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .94, "center_y": .9})
        self.ids.LY8.add_widget(self.next_page)
        self.next_page.bind(on_enter=self.next_page.on_button_hover, on_leave=self.next_page.on_button_hover_exit)
        self.next_page.bind(on_release=lambda page: self.transition("Sixth"))
        self.next_page.bind(on_release=lambda button: (setattr(ExportScreen,"data_store", True)))
        self.next_page.bind(on_press=lambda dict: FinalExportScreen().recieve_dictionary(self.transfered_dict))
        self.next_page.bind(on_press=self.text_lose_focus)

    def on_pre_enter(self, *args):
        if not ExportScreen.data_store:
            self.tuple_list = []
            """Placeholder list for items in Components_data.csv"""
            self.children_list = ["x" for placeholder in range(37)]
            for index, component in enumerate(self.df["Komponent"]):
                self.component_label = Label(
                    text=component,
                    font_size=22,
                    size_hint=(1,None),
                    outline_color=(0, 0, 0, 1),
                    outline_width=2)

                self.arrow_button = HoverButton(
                    background_normal=f"{images_directory}/arrow_pick.png",
                    background_down=f"{images_directory}/arrow_pick.png",
                    background_disabled_normal=f"{images_directory}/arrow_pick_disabled.png",
                    size_hint=(.2, .05),
                    border=(0, 0, 0, 0))
                self.arrow_button.my_id = index
                self.arrow_button.bind(on_enter=self.arrow_button.on_button_hover,on_leave=self.arrow_button.on_button_hover_exit)
                self.arrow_button.bind(on_release=self.transfer_component)

                """'tuple_list' is storing our widgets and they are organized in a touples for later access."""
                tuple_data = (self.component_label, self.arrow_button)
                self.tuple_list.append(tuple_data)

                self.ids.LY9.add_widget(self.component_label)
                self.ids.LY9.add_widget(self.arrow_button)
        else:
            pass

    """
    Each press of a "arrow_button" will now generate 3 new widgets and corresponding "component_label", "arrow_button" will become disabled.
    All of the widgets are related to each other with the use of "component_index". We are using the "children_list" which is filled with appropriate amount
    of placeholders to maintain the correct number of indicies.
    """
    def transfer_component(self, index_id):
        """Each addition of a widget in the LY10 layout will increase the "size_hint" to match the layout's structure."""
        update_size_hint = lambda: (0.4, self.ids.LY10.size_hint[1] + .12)
        self.ids.LY10.size_hint = update_size_hint()

        self.component_index = index_id.my_id
        self.component_text = self.tuple_list[self.component_index][0]
        self.component_button = self.tuple_list[self.component_index][1]
        self.component_text.disabled = True
        self.component_button.disabled = True

        self.transfered_component = Label(
            text=self.component_text.text,
            markup=True,
            font_size=25,
            outline_color=(0, 0, 0, 1),
            outline_width=2)
        self.ids.LY10.add_widget(self.transfered_component)

        """
        Insted of using on_text_validate, usage of 'focus' function allows us to store the widgets 
        in 'self.transfered_dict' without the need to press enter on every instance. Simply clicking out of 
        focus of the text input field will perform equally.
        """
        self.amount_text = TextInput(
            background_active=f"{images_directory}/border_icon_2.png",
            background_normal=f"{images_directory}/border_icon_2.png",
            multiline=False,
            input_filter="int",
            border=(0, 0, 0, 0),
            cursor_color=(0, 0, 0, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=30,
            padding=(20,18,0,0),
            halign="center",
            size_hint=(.3,.4))
        self.amount_text.bind(focus=self.text_input_validate)
        self.amount_text.my_id = self.component_index
        self.ids.LY10.add_widget(self.amount_text)

        self.unselect_button = HoverButton(
            background_normal=f"{images_directory}/back_arrow_icon.png",
            background_down=f"{images_directory}/back_arrow_icon.png",
            border=(0, 0, 0, 0),
            size_hint=(.1,.02))
        self.unselect_button.my_id = self.component_index
        self.unselect_button.bind(on_release=self.clear_component)
        self.unselect_button.bind(on_enter=self.unselect_button.on_button_hover, on_leave=self.unselect_button.on_button_hover_exit)
        self.ids.LY10.add_widget(self.unselect_button)

        """Each placeholder in "children_list" at the specified index is being replaced with tuple consisting of (component, text, button)."""
        self.children_list[self.component_index] = (self.transfered_component,self.amount_text,self.unselect_button)

    """
    With "clear_component" method we are removing corresponding widgets. Each removal of a widget updates the GridLayout and decreases
    the height attribute of size_hint by .12.
    """
    def clear_component(self, index_id):
        """Each removal of a widget in the LY10 layout will decrease the "size_hint" to match the layout's structure."""
        update_size_hint = lambda: (0.4, self.ids.LY10.size_hint[1] - .12)
        self.ids.LY10.size_hint = update_size_hint()
        self.component_index = index_id.my_id

        """In order to remove widgets correctly, we need find the correct index in the "children_list first and only then unpack the tuple."""
        remove_children_0 = self.children_list[self.component_index][0]
        remove_children_1 = self.children_list[self.component_index][1]
        remove_children_2 = self.children_list[self.component_index][2]

        """We set the disable property of a "arrow_button" and "component_label" back to False so they can available again for use."""
        self.tuple_list[self.component_index][0].disabled = False
        self.tuple_list[self.component_index][1].disabled = False

        self.ids.LY10.remove_widget(remove_children_0)
        self.ids.LY10.remove_widget(remove_children_1)
        self.ids.LY10.remove_widget(remove_children_2)

        """
        Condition that checks if 'component_name' is in 'self.transfered_dict'. 
        If true, component will be removed from the dictionary along with the corresponding value.
        """
        if self.children_list[self.component_index][0].text in self.transfered_dict:
            self.transfered_dict.pop(self.children_list[self.component_index][0].text)

        """
        Method that validates the text_field input. After text_input recieves a valid value, component aswell as the value are transfered
        into a 'transfered_dict' as a component (key) and amount as (value). Once value from text_input field is removed, the corresponding key
        in a dictionary is also removed. Value parameter controls the focus of the text input field, once focus is lost 
        (press of a 'enter' button or mouse click outside of the boundary of the text_input field) '.update' function is fired.
        """
    def text_input_validate(self, index_id, value):
        self.component_index = index_id.my_id
        component_name = self.children_list[self.component_index][0].text
        component_amount = self.children_list[self.component_index][1].text

        """
        Verifying that text input has some integer value, if not, key is removed from the dictionary.
        We also verify that integer value is positive only, once negative value is registered, error message is displayed
        and he key is once again removed from the dictionary.
        """

        if not value:
            self.transfered_dict.update({component_name:component_amount})

            if self.transfered_dict[component_name] == "":
                self.transfered_dict.pop(component_name)

            elif component_amount < str(0):
                self.transfered_dict.pop(component_name)
                self.anim.start(self.error_img)
                self.anim.bind(on_complete=self.cancel_anim)

    def cancel_anim(self, dt, instance):
        Clock.schedule_once(lambda dt: self.anim_fade.start(self.error_img),1)

    """
    Method is fired when 'next_page' button is pressed. Meaning, when text_input is still selected (focused), this method
    will unfocus it and allow the value from the text input to be passed into the 'transfered_dict'.
    """
    def text_lose_focus(self, instance):
        if self.transfered_dict != {}:
            self.children_list[self.component_index][1].focus = False
        else:
            pass

    """
    Reseting widget's properties back to their original values including the layout's size_hint and clearing them from the layout.
    """
    def on_leave(self, *args):
        if not ExportScreen().data_store:
            update_size_hint = lambda: (0.4, 0)
            self.ids.LY10.size_hint = update_size_hint()
            self.tuple_list.clear()
            self.children_list.clear()
            self.transfered_dict.clear()
            self.ids.LY9.clear_widgets()
            self.ids.LY10.clear_widgets()
        else:
            pass

class FinalExportScreen(Screen, Transition):
    final_component_dict = {}
    def __init__(self, **kwargs):
        super(FinalExportScreen, self).__init__(**kwargs)
        self.anim = Animation(opacity=1, duration=.2)
        self.anim_fade = Animation(opacity=0, duration=1)

        self.export_img = Image(
            source=f"{images_directory}/export_successful.png",
            allow_stretch=True,
            pos_hint={"center_x": .85, "center_y": .6},
            size_hint=(.3, .3),
            opacity=0)
        self.ids.LY11.add_widget(self.export_img)

        self.textinput_dictionary = {}

        self.home_button = HoverButton(
            background_normal=f"{images_directory}/home_button_icon.png",
            background_down=f"{images_directory}/home_button_icon.png",
            size_hint=(.06, .095),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .94, "center_y": .09})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.home_button.bind(on_release=lambda button: (setattr(self, "data_store", False)))
        self.ids.LY11.add_widget(self.home_button)

        self.previous_page = HoverButton(
            background_normal=f"{images_directory}/return_box.png",
            background_down=f"{images_directory}/return_box.png",
            size_hint=(.07, .125),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .07, "center_y": .9})
        self.ids.LY11.add_widget(self.previous_page)
        self.previous_page.bind(on_enter=self.previous_page.on_button_hover, on_leave=self.previous_page.on_button_hover_exit)
        self.previous_page.bind(on_release=lambda page: self.transition("Fifth"))

        self.pdf_button = HoverButton(
            background_normal=f"{images_directory}/ship_box.png",
            background_down=f"{images_directory}/ship_box.png",
            size_hint=(.07, .125),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .94, "center_y": .9})
        self.pdf_button.bind(on_enter=self.pdf_button.on_button_hover, on_leave=self.pdf_button.on_button_hover_exit)
        self.pdf_button.bind(on_release=self.create_pdf)
        self.pdf_button.bind(on_release=self.animation)
        self.ids.LY11.add_widget(self.pdf_button)

        """ For every text input we create a label with corresponding name, both are then added to a new dictionary."""
        self.name_label = Label(text="")
        self.name_textinput = TextInput(
            border=(0, 0, 0, 0),
            multiline=False,
            cursor_color=(1, 1, 1, 1),
            foreground_color=(1, 1, 1, 1),
            background_color=(1, 1, 1, 0),
            font_size=25,
            halign="center",
            size_hint=(.2, .04),
            pos_hint={"center_x": .55, "center_y": .736},
            on_text_validate=self.create_label)
        self.ids.LY11.add_widget(self.name_textinput)
        self.name_textinput.bind(on_text_validate=self.next_on_validate)
        self.textinput_dictionary.update({self.name_textinput:self.name_label})

        self.system_label = Label(text="")
        self.system_textinput = TextInput(
            border=(0, 0, 0, 0),
            multiline=False,
            cursor_color=(1, 1, 1, 1),
            foreground_color=(1, 1, 1, 1),
            background_color=(1, 1, 1, 0),
            font_size=25,
            halign="center",
            size_hint=(.2, .04),
            pos_hint={"center_x": .55, "center_y": .614},
            on_text_validate=self.create_label)
        self.ids.LY11.add_widget(self.system_textinput)
        self.system_textinput.bind(on_text_validate=self.next_on_validate)
        self.textinput_dictionary.update({self.system_textinput:self.system_label})

        self.material_label = Label(text="")
        self.material_textinput = TextInput(
            border=(0, 0, 0, 0),
            multiline=False,
            cursor_color=(1, 1, 1, 1),
            foreground_color=(1, 1, 1, 1),
            background_color=(1, 1, 1, 0),
            font_size=25,
            halign="center",
            size_hint=(.2, .04),
            pos_hint={"center_x": .55, "center_y": .491},
            on_text_validate=self.create_label)
        self.ids.LY11.add_widget(self.material_textinput)
        self.material_textinput.bind(on_text_validate=self.next_on_validate)
        self.textinput_dictionary.update({self.material_textinput:self.material_label})

        self.contract_label = Label(text="")
        self.contract_textinput = TextInput(
            border=(0, 0, 0, 0),
            multiline=False,
            cursor_color=(1, 1, 1, 1),
            foreground_color=(1, 1, 1, 1),
            background_color=(1, 1, 1, 0),
            font_size=25,
            halign="center",
            size_hint=(.2, .04),
            pos_hint={"center_x": .55, "center_y": .3695},
            on_text_validate=self.create_label)
        self.ids.LY11.add_widget(self.contract_textinput)
        self.contract_textinput.bind(on_text_validate=self.next_on_validate)
        self.textinput_dictionary.update({self.contract_textinput:self.contract_label})

        self.height_label = Label(text="")
        self.height_textinput = TextInput(
            border=(0, 0, 0, 0),
            multiline=False,
            cursor_color=(1, 1, 1, 1),
            foreground_color=(1, 1, 1, 1),
            background_color=(1, 1, 1, 0),
            font_size=25,
            halign="center",
            size_hint=(.2, .04),
            pos_hint={"center_x": .55, "center_y": .245},
            on_text_validate=self.create_label)
        self.ids.LY11.add_widget(self.height_textinput)
        self.height_textinput.bind(on_text_validate=self.next_on_validate)
        self.textinput_dictionary.update({self.height_textinput:self.height_label})

        self.date_label = Label(text="")
        self.date_textinput = TextInput(
            border=(0, 0, 0, 0),
            multiline=False,
            cursor_color=(1, 1, 1, 1),
            foreground_color=(1, 1, 1, 1),
            background_color=(1, 1, 1, 0),
            font_size=25,
            halign="center",
            size_hint=(.2, .04),
            pos_hint={"center_x": .55, "center_y": .12},
            on_text_validate=self.create_label)
        self.ids.LY11.add_widget(self.date_textinput)
        self.textinput_dictionary.update({self.date_textinput:self.date_label})

        self.ids.LY13.add_widget(self.name_label)
        self.ids.LY13.add_widget(self.system_label)
        self.ids.LY13.add_widget(self.material_label)
        self.ids.LY13.add_widget(self.contract_label)
        self.ids.LY13.add_widget(self.height_label)
        self.ids.LY13.add_widget(self.date_label)

    """ Method that allows the 'Enter' button to move and focus the next TextInput. """
    def next_on_validate(self, instance):
        next = instance._get_focus_next("focus_next")
        if next:
            instance.focus = False
            next.focus = True

    """
    Method that updates the labels within the "self.textinput_dictionary. After user validates the text input with enter,
    corresponding label is updated with the user's text.
    """
    def create_label(self, instance):
        label = self.textinput_dictionary[instance]
        label.color = (0, 0, 0, 1)
        label.text = instance.text

        if instance == self.name_textinput:
            label.font_size = 35
            label.bold = True
            label.pos_hint = {"center_x": .5, "center_y": .95}

        if instance == self.system_textinput:
            label.text = f"SYSTEM: {instance.text}"
            label.font_size = 20
            label.pos_hint = {"center_x": .5, "center_y": .75}

        if instance == self.material_textinput:
            label.underline = True
            label.font_size = 15
            label.pos_hint = {"center_x": .133, "center_y": .9}
            label.text_size = (150, None)
            label.size = label.texture_size

        if instance == self.contract_textinput:
            label.font_size = 20
            label.pos_hint = {"center_x": .85, "center_y": .9}

        if instance == self.height_textinput:
            label.font_size = 15
            label.pos_hint = {"center_x": .133, "center_y": .8}
            label.text_size = (150, None)
            label.size = label.texture_size

        if instance == self.date_textinput:
            label.text = f"DATUM: {instance.text.replace('/','.')}"
            label.font_size = 15
            label.pos_hint = {"center_x": .16, "center_y": .02}
            label.text_size = (200, None)
            label.size = label.texture_size

    def create_pdf(self, instance):
        final_dictionary = FinalExportScreen.final_component_dict

        width = 210
        height = 297
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        with open(lucida_font_path, "rb") as font_file:
            font_contents = font_file.read()

        pdf.add_font("Lucida Sans Unicode Regular", style="", fname=lucida_font_path, uni=True)
        pdf.rect(10,10,190,277)
        pdf.set_margins(10, 0, 10)
        pdf.set_auto_page_break(False)
        pdf.image(os.path.join(images_directory, 'SaniLogo.png'), 179, 279, 20, 7)

        # Name
        pdf.set_font("Lucida Sans Unicode Regular", "", 25)
        pdf.cell(0,40, self.name_label.text,0,1, "C")

        # System
        pdf.set_font("Lucida Sans Unicode Regular", "", 15)
        pdf.set_xy(0, 85)
        pdf.cell(0, 0, self.system_label.text, 0, 0, "C")

        # Material
        pdf.set_font("Lucida Sans Unicode Regular", "U", 20)
        pdf.set_xy(10, 40)
        pdf.cell(0, 0, self.material_label.text, 0, 0, "L")

        # Contract
        pdf.set_font("Lucida Sans Unicode Regular", "", 20)
        pdf.set_xy(150, 40)
        pdf.multi_cell(50, 10, self.contract_label.text,1, "L")

        # Height
        pdf.set_font("Lucida Sans Unicode Regular", "", 10)
        pdf.set_xy(10, 60)
        pdf.cell(0, 0, self.height_label.text, 0, 0, "L")

        # Date
        pdf.set_font("Lucida Sans Unicode Regular", "", 10)
        pdf.set_y(285)
        pdf.cell(0,0, self.date_label.text,0,2, "L")

        # Table
        y = 90
        y2 = 90
        pdf.set_auto_page_break(True)

        """
        Two different conditions to for a better interpretation of the table
        Once the amount of dictionary items is greater then 12, PDF table is divided into two columns
        to keep all of the components in one page.
        """
        if final_dictionary != {} and len(final_dictionary) <= 12:
            for index, (key, value) in enumerate(final_dictionary.items()):
                pdf.set_font("Lucida Sans Unicode Regular", "", 13)
                pdf.set_xy(40, y)
                pdf.multi_cell(100, 15, key, 1)

                pdf.set_font("Lucida Sans Unicode Regular", "", 15)
                pdf.set_xy(140, y)
                pdf.multi_cell(30, 15, str(value), 1, "C")
                y += 15

        elif final_dictionary != {} and len(final_dictionary) >= 13:
            for index, (key, value) in enumerate(final_dictionary.items()):
                if index <= 9:
                    pdf.set_font("Lucida Sans Unicode Regular", "", 11)
                    pdf.set_xy(10, y)
                    pdf.multi_cell(80, 15, key, 1)

                    pdf.set_font("Lucida Sans Unicode Regular", "", 15)
                    pdf.set_xy(90, y)
                    pdf.multi_cell(20, 15, str(value), 1, "C")
                    y += 15

                elif index >= 9:
                    pdf.set_font("Lucida Sans Unicode Regular", "", 11)
                    pdf.set_xy(110, y2)
                    pdf.multi_cell(70, 15, key, 1)

                    pdf.set_font("Lucida Sans Unicode Regular", "", 15)
                    pdf.set_xy(180, y2)
                    pdf.multi_cell(20, 15, str(value), 1, "C")
                    y2 += 15
        else:
            pass

        """ 
        Exporting the PDF file into a subfolder 'PDF Component folder' with the use of an absolute path. 
        '.replace('/','.')' needs to be introduced to prevent an error which causes the program to crash.
        When user decides to set the date for example: '28/02/2022', FPDF understands the '/' as a path separator,
        which leads to a non-existing directory. '.replace('/','.')' takes the slash symbol and replaces it with a period.
        """

        pdf_output_path = os.path.join("PDF Component folder",f"{self.name_label.text.replace('/','.')}, {self.date_label.text[7::].replace('/','.')}.pdf")
        pdf.output(pdf_output_path)

        """
        Using Pandas 'merge' we manage both default database which holds all of the components aswell as the new array,
        which is created from 'final_dictionary'. This dictionary is then merged into the default database (Components_data.csv), which allows us to 
        subtract the exact amount of components and keep the database up to date.
        """
        with open(csv_file_path, 'rb') as f:
            contents = f.read()
        df = pd.read_csv(io.BytesIO(contents), encoding='utf-8')
        df2 = pd.DataFrame.from_dict(final_dictionary, orient="index", columns=["Mnozstvi"])
        df2 = df2.reset_index()
        df2 = df2.rename(columns={"index": "Komponent"})

        merge_df = df.merge(df2, on="Komponent", how="left")
        merge_df["Mnozstvi_x"] = merge_df["Mnozstvi_x"].sub(pd.to_numeric(merge_df["Mnozstvi_y"], errors="coerce"),fill_value=0)
        merge_df = merge_df.drop(columns=["Mnozstvi_y"])
        merge_df = merge_df.rename(columns={'Mnozstvi_x': 'Mnozstvi'})
        merge_df["Mnozstvi"] = merge_df["Mnozstvi"].astype(int)
        merge_df.to_csv(csv_file_path, encoding='utf-8', index=False)

    def animation(self, instance):
        self.anim.start(self.export_img)
        self.anim.bind(on_complete=self.cancel_anim)

    def cancel_anim(self, dt, instance):
        Clock.schedule_once(lambda dt: self.anim_fade.start(self.export_img), 1)

    """
    Method that recieves 'transfered_dict' dictionary from ExportScreen Class in order to interpret the data correctly.
    """
    def recieve_dictionary(self, transfered_dict):
        FinalExportScreen.final_component_dict.update(transfered_dict)

    def on_pre_enter(self, *args):
        for item, value in self.final_component_dict.items():
            self.pdf_component = Label(
                text=item,
                markup=True,
                font_size=15,
                padding=(0, 10, 0, 0),
                color=(0,0,0,1))

            self.pdf_component_amount = Label(
                text=value,
                markup=True,
                font_size=15,
                padding=(0,10,0,0),
                color=(0, 0, 0, 1))
            self.ids.LY12.add_widget(self.pdf_component)
            self.ids.LY12.add_widget(self.pdf_component_amount)

            for divider in range(2):
                self.divider_line = Image(
                    source=f"{images_directory}/divider.png",
                    size_hint_y=None,
                    height=4,
                    width=3)
                self.ids.LY12.add_widget(self.divider_line)

    def on_leave(self, *args):
        FinalExportScreen().final_component_dict.clear()
        self.ids.LY12.clear_widgets()

class WindowManager(ScreenManager):
    pass

class SaniStore(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="First"))
        sm.add_widget(MainScreen(name="Second"))
        sm.add_widget(InventoryScreen(name="Third"))
        sm.add_widget(ImportScreen(name="Fourth"))
        sm.add_widget(ExportScreen(name="Fifth"))
        sm.add_widget(FinalExportScreen(name="Sixth"))
        self.icon = os.path.join(images_directory, "SaniStore_logo.png")
        return sm
    def get_images_directory(self):
        return images_directory

if __name__ == "__main__":
    SaniStore().run()
