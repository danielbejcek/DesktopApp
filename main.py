import kivy
import pandas as pd
import tabula
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.event import EventDispatcher
from HoverButton import HoverBehavior
from kivy.uix.textinput import TextInput
from DropField import *
from plyer import filechooser
from kivy.lang import Builder




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

        # Dictionary which consists of keys and values. Each key is a image before being selected with a mouse hover,
        # each value of a key is a image which is highlighted after it has been selected with a mouse hover.
        # Whenever we want to add additional button, that includes a highlight function, we just need to update the path within this dictionary.
        self.images_path = {"Images/inventory_text.png": "Images/inventory_text_selected.png",
                            "Images/import_text.png": "Images/import_text_selected.png",
                            "Images/export_text.png":"Images/export_text_selected.png",
                            "Images/exit_button.png":"Images/exit_button_selected.png",
                            "Images/home_button_icon.png":"Images/home_button_icon_selected.png",
                            "Images/notebook_closed.png":"Images/notebook_closed_selected.png",
                            "Images/notebook_opened.png":"Images/notebook_opened_selected.png",
                            "Images/minus_sign.png":"Images/minus_sign_selected.png",
                            "Images/plus_sign.png":"Images/plus_sign_selected.png",
                            "Images/lock_icon.png":"Images/unlocked_icon_selected.png",
                            "Images/unlocked_icon.png":"Images/lock_icon_selected.png",
                            "Images/pencil_edit.png":"Images/pencil_icon_selected.png",
                            "Images/closed_folder.png":"Images/opened_folder.png",
                            "Images/arrow_pick.png":"Images/arrow_pick_selected.png"}

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
            size_hint=(.2, .04),
            border=(0, 0, 0, 0))

        self.ids.LY2.add_widget(self.inventory_button)
        self.inventory_button.bind(on_enter=self.inventory_button.on_button_hover, on_leave=self.inventory_button.on_button_hover_exit)
        # In order for a transition to work, we need to combine this on_release event with lambda.
        self.inventory_button.bind(on_release=lambda x: self.transition("Third"))


        self.import_button = HoverButton(
            background_normal="Images/import_text.png",
            background_down="Images/import_text.png",
            font_size=15,
            size_hint=(.2, .04),
            border=(0, 0, 0, 0))
        self.ids.LY2.add_widget(self.import_button)
        self.import_button.bind(on_enter=self.import_button.on_button_hover, on_leave=self.import_button.on_button_hover_exit)
        self.import_button.bind(on_release=lambda x: self.transition("Fourth"))

        self.export_button = HoverButton(
            background_normal="Images/export_text.png",
            background_down="Images/export_text.png",
            font_size=30,
            size_hint=(.2, .04),
            border=(0, 0, 0, 0))
        self.export_button.bind(on_enter=self.export_button.on_button_hover, on_leave=self.export_button.on_button_hover_exit)
        self.export_button.bind(on_release=lambda x: self.transition("Fifth"))
        self.ids.LY2.add_widget(self.export_button)

        self.exit_button = HoverButton(
            background_normal="Images/exit_button.png",
            background_down="Images/exit_button.png",
            size_hint=(.06, .09),
            pos_hint={"center_x": .93, "center_y": .09},
            border=(0, 0, 0, 0))
        self.exit_button.bind(on_enter=self.exit_button.on_button_hover, on_leave=self.exit_button.on_button_hover_exit)
        self.exit_button.bind(on_release=self.exit_app)
        self.ids.LY25.add_widget(self.exit_button)
    def exit_app(self, instance):
        App.get_running_app().stop()
class InventoryScreen(Screen, Transition):
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)

        # Load the CSV file from the directory.
        self.load_data()

        # Empty list in wich we store all the numerical values from our CSV database.
        # This list later servers as a merge between the values that are to be changed in the database.
        self.final_count = []
        for self.final_amount in (self.df["Množství"]):
            self.final_count.append(self.final_amount)

        self.home_button = HoverButton(
            background_normal="Images/home_button_icon.png",
            background_down="Images/home_button_icon.png",
            size_hint=(.06,.095),
            border=(0,0,0,0),
            pos_hint={"center_x": .94,"center_y": .09})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.ids.LY3.add_widget(self.home_button)

        self.current_state_image = Image(
            source="Images/current_state.png",
            size_hint=(.3, .5),
            pos_hint={"center_x": .175, "center_y": .92})
        self.ids.LY3.add_widget(self.current_state_image)

        self.notebook_button = HoverButton(
            background_normal="Images/notebook_closed.png",
            background_down="Images/notebook_closed.png",
            background_disabled_normal="Images/notebook_closed_disabled.png",
            size_hint=(.04, .1),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .38, "center_y": .91})
        self.notebook_button.bind(on_enter=self.notebook_button.on_button_hover, on_leave=self.notebook_button.on_button_hover_exit)
        self.notebook_button.bind(on_release=self.background_change)
        self.ids.LY3.add_widget(self.notebook_button)

        self.lock_button = HoverButton(
            background_normal="Images/lock_icon.png",
            background_down="Images/unlocked_icon.png",
            background_disabled_normal="Images/lock_icon_disabled.png",
            size_hint=(.05, .09),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .45, "center_y": .91})
        self.lock_button.bind(on_enter=self.lock_button.on_button_hover, on_leave=self.lock_button.on_button_hover_exit)
        self.lock_button.bind(on_release=self.update_components)
        self.ids.LY3.add_widget(self.lock_button)

    # Method that controls the state of the "lock_button" widget. Once the background image of the lock_button is changed,
    # we are firing widgets depending on the background. In order for the widgets to display properly in the UI, once the state is changed,
    # all widgets are deleted and corresponding widgets take place immediately.
    def update_components(self, instance):
        # Widgets are unlocked.
        if instance.background_normal == "Images/unlocked_icon_selected.png":
            self.ids.LY4.clear_widgets()
            self.notebook_button.disabled = True
            instance.background_normal = "Images/unlocked_icon.png"
            instance.background_down = "Images/lock_icon.png"
            self.add_widgets(self.ids.LY4)

        # Widgets are locked.
        if instance.background_normal == "Images/lock_icon_selected.png":
            self.ids.LY4.clear_widgets()
            self.notebook_button.disabled = False
            instance.background_normal = "Images/lock_icon.png"
            instance.background_down = "Images/unlocked_icon.png"
            self.add_widgets(self.ids.LY4)

    # Whenever we load this screen for the first time, "add_widgets" is fired that fills the screen with scrollable database
    # of components and their respective amount. This fucntion is also applied when we return to this screen. Further in the code
    # we will use a "on_leave" function that clears all of the widgets to prevent the widgets from overlapping.
    def on_pre_enter(self, *args):
            self.add_widgets(self.ids.LY4)

    """
    Method that changes visuals and also adds or clears widgets depending on the current notebook status.
    This method is bound to a button click that traverses between an opened and closed.
    Whenever we click a respective button and meet a condition thats states "notebook_closed",
    we fire a "clear_widgets" function that deletes widgets from previous layout and adds new widgets to a new layout.
    """
    def background_change(self, instance):
        if instance.background_normal and instance.background_down == "Images/notebook_closed.png":
            instance.size_hint=(.08,.1)
            instance.background_normal = "Images/notebook_opened.png"
            instance.background_down = "Images/notebook_opened.png"
            self.ids.LY4.clear_widgets()
            self.add_widgets(self.ids.LY5)

        # Same utility only the other way around. We delete widgets from new layout only to fire a "on_pre_enter" function,
        # that brings us back to the first layout with corresponding widgets included."""
        elif instance.background_normal and instance.background_down == "Images/notebook_opened.png":
            instance.size_hint=(.04,.1)
            instance.background_normal="Images/notebook_closed.png"
            instance.background_down="Images/notebook_closed.png"
            self.ids.LY5.clear_widgets()
            self.on_pre_enter()

    """
    Loading the .csv file with necessary data.
    """
    def load_data(self):
        data_file = "Components_data.csv"
        self.df = pd.read_csv(data_file)

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

        # Interface is locked.
        if self.notebook_button.background_normal and self.notebook_button.background_down == "Images/notebook_closed.png":
            if self.lock_button.background_normal == "Images/lock_icon.png":
                self.lock_button.disabled = False


                # Updates the .csv file with modified values. Whenever user has finished making changes in the unlocked interface,
                # proceeds to click the lock icon button, only then the changes in the database are saved.
                self.save_data(self.final_count)

                # We created an empty list for later use.
                self.new_amount_list = []

                for index, (component, amount) in enumerate(zip(self.df["Komponent"], self.df["Množství"])):

                    self.component_label= Label(
                        text=component,
                        font_size=25,
                        padding=(100,0,0,0),
                        bold=False)

                    self.amount_input = Label(
                        text=str(amount),
                        font_size=35,
                        padding=(60, 0, 0, 0),
                        bold=False)

                    self.minus_sign = HoverButton(
                        background_disabled_normal="Images/minus_sign_disabled.png",
                        size_hint=(None, None),
                        width=90,
                        height=80,
                        disabled=True,
                        padding=(0,0,0,0),
                        opacity=.2)

                    self.plus_sign = HoverButton(
                        background_disabled_normal="Images/plus_sign_disabled.png",
                        size_hint=(None, None),
                        width=80,
                        height=80,
                        disabled=True,
                        opacity=.2)

                    self.value_input_button = HoverButton(
                        background_disabled_normal="Images/pencil_edit.png",
                        border=(0, 0, 0, 0),
                        disabled=True,
                        opacity=(.05),
                        size_hint=(.25, .01),
                        padding=(0, 0, 50, 0))

                    # Setting the number of columns explicitly to match the positioning of widgets.
                    self.ids.LY4.cols = 5
                    self.ids.SW1.size_hint = (.484, .8)
                    layer.add_widget(self.component_label)
                    layer.add_widget(self.amount_input)
                    layer.add_widget(self.minus_sign)
                    layer.add_widget(self.plus_sign)
                    layer.add_widget(self.value_input_button)

                    for divider in range(5):
                        self.divider_line_3 = Image(
                            source="Images/divider_3.png",
                            size_hint_y=None,
                            size_hint_x=.1,
                            height=2,
                            width=2,
                            fit_mode="fill")
                        layer.add_widget(self.divider_line_3)

            # Condition that lets us set specific widgets from disabled=True to False, alowing us to use the "minus_sign" and "plus_sign" widgets
            # to control the amount of the components. This condition is active only if the lock icon is pressed and becomes unlocked.
            if self.lock_button.background_normal == "Images/unlocked_icon.png":

                self.text_inputs_list = []

                # Interface is unlocked.
                for index, (component, amount) in enumerate(zip(self.df["Komponent"], self.df["Množství"])):

                    self.component_label_2 = Label(
                        text=component,
                        font_size=25,
                        padding=(175, 0, 0, 0),
                        bold=False)

                    self.amount_input_2 = Label(
                        text=str(amount),
                        font_size=35,
                        padding=(310, 0, 10, 0),
                        bold=False)

                    self.minus_sign_2 = HoverButton(
                        background_normal="Images/minus_sign.png",
                        background_down="Images/minus_sign.png",
                        size_hint=(None, None),
                        width=90,
                        height=80,
                        disabled=False,
                        opacity=1,
                        on_release=self.decrement_value)
                    self.minus_sign_2.bind(on_enter=self.minus_sign_2.on_button_hover, on_leave=self.minus_sign_2.on_button_hover_exit)
                    self.minus_sign_2.my_id = index

                    self.plus_sign_2 = HoverButton(
                        background_normal="Images/plus_sign.png",
                        background_down="Images/plus_sign.png",
                        size_hint=(None, None),
                        width=80,
                        height=80,
                        disabled=False,
                        opacity=1,
                        on_release=self.increment_value)
                    self.plus_sign_2.bind(on_enter=self.plus_sign_2.on_button_hover, on_leave=self.plus_sign_2.on_button_hover_exit)
                    self.plus_sign_2.my_id = index


                    # "new_amount" Label is a widget that the user can modify according to his needs with the use of "plus_sign_2", "minus_sign_2" and "value_input_button" buttons.
                    # Each iteration of this Label is then added to a list to help us connect it with corresponding components.
                    self.new_amount = Label(
                        text=str(0),
                        font_size=30,
                        padding=(110, 0, 0, 0),
                        disabled=False,
                        color=(1,1,1,0),
                        bold=True)
                    self.new_amount_list.append(self.new_amount)

                    # Widget that allows the user to create a text_input field, which is automatically focused.
                    self.value_input_button = HoverButton(
                        background_normal="Images/pencil_edit.png",
                        background_down="Images/pencil_edit.png",
                        border=(0, 0, 0, 0),
                        opacity=(.6),
                        size_hint=(.35, .01),
                        padding=(0, 0, 0, 0))
                    self.value_input_button.bind(on_enter=self.value_input_button.on_button_hover, on_leave=self.value_input_button.on_button_hover_exit)
                    self.value_input_button.bind(on_release=self.button_to_text)
                    self.value_input_button.my_id = index

                    # Creating a empty text_input field in which user can enter numerical value.
                    # After user validates the field with an press of a 'enter' button. Value from the text field is transfered into "new_amount" widget.
                    # After validation, text field becomes disabled and hidden.
                    self.text_value_input = TextInput(
                        background_active="Images/border_icon.png",
                        background_disabled_normal="Images/border_icon.png",
                        multiline=False,
                        border=(0, 0, 0, 0),
                        halign="right",
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

                    # Custom configuration of a layout to fit widgets correctly.
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
                            source="Images/divider_3.png",
                            size_hint_y=None,
                            size_hint_x=.1,
                            height=2,
                            width=2,
                            fit_mode="fill")
                        layer.add_widget(self.divider_line_2)
                        if iteration_count > 6:
                            self.divider_line_2.opacity = (0)




        # In the second condition, we create a database into 4 columns to present a general overview of the warehouse stock.
        # We are also setting the "lock_button.disabled" to True. Meaning once we are in this overview, we are not able to modify the values.
        elif self.notebook_button.background_normal and self.notebook_button.background_down == "Images/notebook_opened.png":
            self.lock_button.disabled = True
            iteration_count = 0

            for component, amount in zip(self.df["Komponent"], self.df["Množství"]):
                self.component_label= Label(
                    text=component,
                    size_hint=(.8,1),
                    font_size=18)

                self.amount_input_3 = Label(
                    text=str(amount),
                    size_hint=(.8,1),
                    font_size=22,)

                # Once a certain amount of components is bellow critical number, value will now be displayed in red color.
                if amount < 11:
                    self.amount_input_3.color=(1,0,0,1)

                layer.add_widget(self.component_label)
                layer.add_widget(self.amount_input_3)
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
                            width=5)
                        layer.add_widget(self.divider_line)
                        iteration_count = 0

    # Method that allows us to change values of a "new_amount" Label. It's directly connected to the database and it's being updated real-time.
    # Each widget has its index as a 'Primary key' to help us navigate between the iterations and control which component's value we want to change.
    # We are directly accessing an item in the "new_amount_list" which has been appended from the "new_amount" Label.
    # With the use of "index" variable we are able to connect the specific item in the list to a widget created by the loop.
    # Change of values in the "self.new_amount.text" Label is done by modifying the list items, not by accessing the "self.new_amount" widget directly.
    def increment_value(self, index_id):
        index_plus = index_id.my_id
        value = "plus"
        self.new_amount_list[index_plus].text = str(int(self.new_amount_list[index_plus].text) + 1)
        self.set_label_color(index_plus)
        self.count_values(index_plus, value)


    def decrement_value(self, index_id):
        index_minus = index_id.my_id
        value = "minus"
        self.new_amount_list[index_minus].text = str(int(self.new_amount_list[index_minus].text) - 1)
        self.set_label_color(index_minus)
        self.count_values(index_minus, value)

    # Method that allows us to display and immediately focus a new text input field.
    def button_to_text(self, index_id):
        button_index = index_id.my_id
        self.text_inputs_list[button_index].disabled = False
        self.text_inputs_list[button_index].opacity = 1
        self.text_inputs_list[button_index].focused = True

    # After pressing enter, while text input widget is active, this method will transfer the value into the "new_amount" widget.
    # To maintain proper functionality, if the "new_amount" value has not yet been modified (value = 0), new value will now be now added.
    # Although if user decides to correct his previous value, the "new_amount" will be reset and equal to the original value.
    def custom_text_validate(self, index_id):
        value = "custom"
        self.text_index = index_id.my_id
        self.text_inputs_list[self.text_index].disabled = True
        self.text_inputs_list[self.text_index].focused = False
        self.text_inputs_list[self.text_index].opacity = 0

        self.user_amount = int(self.text_inputs_list[self.text_index].text)
        if self.new_amount_list[self.text_index].text == str(0):
            self.new_amount_list[self.text_index].text = str(self.user_amount)
        elif self.new_amount_list[self.text_index].text != str(0):
            self.new_amount_list[self.text_index].text = str(self.user_amount)
            self.final_count[self.text_index] = self.df.at[self.text_index, "Množství"]
        self.set_label_color(self.text_index)
        self.count_values(self.text_index, value)

    # To prevent the user to make changes in the database while still 'unlocked interface' we created an empty list "self.final_count".
    # We want all the changes to the database occur only after we exit from the unlocked interface and enter into a locked interface (by clicking the lock_icon).
    # Instead of making changes directly to the core database, we appended all of the component amounts into "self.final_count" list and make changes there.
    # Once user clicks a "plus_sign", "minus_sign" or "text_input_button", the list's components are updated on a corresponding index.
    def count_values(self, index, value):
        if value == "plus":
            self.final_count[index] += 1

        elif value == "minus":
            self.final_count[index] -= 1

        elif value == "custom":
            self.final_count[index] += self.user_amount



    # Method which allows us to unfocus and disable a text input field as soon as it's not focused.
    def unfocus_text_input(self, index_id, value):
        index = index_id.my_id
        if not value:
            self.text_inputs_list[index].disabled = True
            self.text_inputs_list[index].opacity = 0



    # Method that checks for the amount of components. As soon as value falls bellow 0, the color of the value turns red.
    # Other way around if the value is above zero, the color turns green.
    def set_label_color(self, index):
        if self.new_amount_list[index].text > str(0):
            self.new_amount_list[index].color = (0, 1, 0, 1)
        elif self.new_amount_list[index].text < str(0):
            self.new_amount_list[index].color = (1, 0, 0, 1)
        else:
            self.new_amount_list[index].color = (1, 1, 1, 0)


    # Method that is fired whenever the user clicks on "lock_icon" button to store the changed data into the database.
    # We loop trough the CSV file and merge the pending changes in "self.final_count" list into the default database.
    def save_data(self, final_count):
        for index, amount in enumerate(self.df["Množství"]):
            self.df.at[index, "Množství"] = self.final_count[index]

        data_file = "Components_data.csv"
        self.df.to_csv(data_file, index=False)



    # Function that cleans the page of all the widgets, allowing us to return to the page without overlapping widgets.
    def on_leave(self, *args):
        self.ids.LY4.clear_widgets()
        self.ids.LY5.clear_widgets()
        self.notebook_button.size_hint = (.04, .1)
        self.notebook_button.background_normal = "Images/notebook_closed.png"
        self.notebook_button.background_down = "Images/notebook_closed.png"
        self.lock_button.background_normal = "Images/lock_icon.png"
        self.lock_button.background_down = "Images/unlocked_icon.png"
        self.notebook_button.disabled = False


class ImportScreen(Screen, Transition, DropField):
    # opacity_value = NumericProperty(0)
    source_image_1 = StringProperty("Images/importscreen_edit_2.png")



    def __init__(self,**kwargs):
        super(ImportScreen, self).__init__(**kwargs)

        data_file = "Components_data.csv"
        self.base_df = pd.read_csv(data_file)

        # self.drop_field = DropField(size_hint=(1, None))
        # self.drop_field.bind(on_dropfile=self.on_file_drop)
        # self.ids.LY6.add_widget(self.drop_field)


        self.home_button = HoverButton(
            background_normal="Images/home_button_icon.png",
            background_down="Images/home_button_icon.png",
            size_hint=(.065, .1),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .94, "top_y": .94})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.ids.LY6.add_widget(self.home_button)

        self.open_file_button = HoverButton(
            background_normal="Images/closed_folder.png",
            background_down="Images/closed_folder.png",
            size_hint=(.1,.15),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .24, "center_y": .4})
        self.open_file_button.bind(on_release=self.choose_file)
        self.open_file_button.bind(on_enter=self.open_file_button.on_button_hover, on_leave=self.open_file_button.on_button_hover_exit)

        self.ids.LY6.add_widget(self.open_file_button)

        self.result_image = Image(
            source="Images/border_black_edit.png",
            allow_stretch=True,
            pos_hint={"center_x": .5, "center_y": .5})


    """
    Method that pops up a Windows browser, from which user can select a file to work with.
    If user selects a new .pdf file, previous widget will be cleared to prevent overlapping.
    """
    def choose_file(self, instance):
        self.path = filechooser.open_file(title="Select a file ...", filters=[("PDF Files", "*.pdf")])
        if self.path:

            self.open_file_button.opacity = 0
            self.source_image_1 = "Images/importscreen_edit_2_blurred.png"
            # self.opacity_value = 1
            self.ids.LY65.clear_widgets()
            self.create_table(self.path)
            self.ids.LYimage.add_widget(self.result_image)
        elif self.path == None:
            print("No file selected")


    """
    Method that pulls data from imported .pdf file and selects the first index from the list. 
    Argument needs to be passed as a string (self.path[0]) not a list.
    """
    def create_table(self, pdf_file):
        tables = tabula.read_pdf(str(pdf_file[0]), pages="all")
        user_df = pd.concat(tables)

        col_component = user_df.columns[0]
        col_amount = user_df.columns[1]
        component = user_df[col_component]
        amount = user_df[col_amount]
        data_frame = {"Component": component, "Amount": amount}
        print(data_frame["Component"])
        print(self.base_df["Komponent"])
        # corresponding_component = []
        # if data_frame["Component"] in self.base_df["Komponent"]:
        #     corresponding_component.append(self.base_df["Amount"])
        # print(corresponding_component)


        for index, (component, amount) in enumerate(zip(data_frame["Component"], data_frame["Amount"])):
            self.imported_component = Label(
                text=component,
                font_size=20,
                color=(1, 1, 1, 1),
                bold=False)
            self.ids.LY65.add_widget(self.imported_component)

            self.imported_amount = Label(
                text=str(amount),
                font_size=20,
                color=(1,1,1,1),
                bold=True)
            self.ids.LY65.add_widget(self.imported_amount)

            # self.correspnding_amount = Label


            for divider in range(2):
                self.divider_line = Image(
                    source="Images/divider_3.png",
                    size_hint_y=None,
                    height=10,
                    width=5)
                self.ids.LY65.add_widget(self.divider_line)


    def on_leave(self, *args):
        self.ids.LY65.clear_widgets()
        self.opacity_value = 0





    # def on_file_drop(self, instance, touch):
    #     file_path = touch.profile.get("file_path", "")
    #     if file_path:
    #         print("I have been deployed")


class ExportScreen(Screen, Transition):

    def __init__(self, **kwargs):
        super(ExportScreen, self).__init__(**kwargs)
        self.df = pd.read_csv("Components_data.csv")

        self.home_button = HoverButton(
            background_normal="Images/home_button_icon.png",
            background_down="Images/home_button_icon.png",
            size_hint=(.06, .095),
            border=(0, 0, 0, 0),
            pos_hint={"center_x": .94, "center_y": .09})
        self.home_button.bind(on_enter=self.home_button.on_button_hover, on_leave=self.home_button.on_button_hover_exit)
        self.home_button.bind(on_release=self.home_page)
        self.ids.LY8.add_widget(self.home_button)

        # Setting "size_hint" of LY10 layout explicitly so we can modify its values in python code.
        # self.ids.LY10.size_hint = (.4,.06)

    def on_pre_enter(self, *args):
        self.tuple_list = []
        self.children_list = []

        for placeholder in range(38):
            x = "x"
            self.children_list.append(x)

        for index, component in enumerate(self.df["Komponent"]):
            self.component_label = Label(
                text=component,
                font_size=20,
                size_hint=(1,None))

            self.arrow_button = HoverButton(
                background_normal="Images/arrow_pick.png",
                background_down="Images/arrow_pick.png",
                background_disabled_normal="Images/arrow_pick_disabled.png",
                size_hint=(.2, .05),
                border=(0, 0, 0, 0))
            self.arrow_button.my_id = index
            self.arrow_button.bind(on_enter=self.arrow_button.on_button_hover,on_leave=self.arrow_button.on_button_hover_exit)
            self.arrow_button.bind(on_release=self.transfer_component)




            tuple_data = (self.component_label, self.arrow_button)
            self.tuple_list.append(tuple_data)

            self.ids.LY9.add_widget(self.component_label)
            self.ids.LY9.add_widget(self.arrow_button)

    """
    "self.component_list.items()" returns a list of tuples where each tuple contains a Label (key) and a Button (value).
    With use of a "list(..)" we convert it into a regular list. "[index]" extracts the tuple at the specified index from the list.
    Label, button is a tuple unpacking operation. It assigns the first element of the selected tuple to the variable label 
    and the second element to the variable button. This way when a button is pressed, both of the widgets will be disabled.
    """
    def transfer_component(self, index_id):
        # Each addition of a widget in the LY10 layout will increase the "size_hint" to match the layout's structure.
        update_size_hint = lambda: (0.4, self.ids.LY10.size_hint[1] + 0.06)
        self.ids.LY10.size_hint = update_size_hint()

        self.component_index = index_id.my_id
        self.component_text = self.tuple_list[self.component_index][0]
        self.component_button = self.tuple_list[self.component_index][1]
        self.component_text.disabled = True
        self.component_button.disabled = True


        self.transfered_component = Label(
            text=self.component_text.text,
            font_size=30)
        self.ids.LY10.add_widget(self.transfered_component)

        self.amount_text = TextInput(
            background_active="Images/border_icon.png",
            background_normal="Images/border_icon.png",
            multiline=False,
            border=(0, 0, 0, 0),
            font_size=35,
            padding=(10,20,0,0),
            halign="center",
            size_hint=(.2,.3))
        self.ids.LY10.add_widget(self.amount_text)

        self.unselect_button = Button(
            text="X",
            size_hint=(.2,.2))
        self.unselect_button.my_id = self.component_index
        self.unselect_button.bind(on_release=self.clear_component)
        self.ids.LY10.add_widget(self.unselect_button)
        print(f"Selected index is: {self.component_index}")



        self.children_list[self.component_index] = (self.transfered_component,self.amount_text,self.unselect_button)



    def clear_component(self, index_id):
        # Each removal of a widget in the LY10 layout will decrease the "size_hint" to match the layout's structure.
        update_size_hint = lambda: (0.4, self.ids.LY10.size_hint[1] - 0.06)
        self.ids.LY10.size_hint = update_size_hint()


        self.component_index = index_id.my_id
        print(f"Deleted index is: {self.component_index}")
        remove_children_0 = self.children_list[self.component_index][0]
        remove_children_1 = self.children_list[self.component_index][1]
        remove_children_2 = self.children_list[self.component_index][2]

        self.tuple_list[self.component_index][0].disabled = False
        self.tuple_list[self.component_index][1].disabled = False

        self.ids.LY10.remove_widget(remove_children_0)
        self.ids.LY10.remove_widget(remove_children_1)
        self.ids.LY10.remove_widget(remove_children_2)










    def on_leave(self, *args):
        update_size_hint = lambda: (0.4, .02)
        self.ids.LY10.size_hint = update_size_hint()
        self.tuple_list.clear()
        self.children_list.clear()
        self.ids.LY9.clear_widgets()
        self.ids.LY10.clear_widgets()
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
        return sm


if __name__ == "__main__":
    SaniStore().run()
