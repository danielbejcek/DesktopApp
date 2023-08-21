import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.logo_image = Image(
            source="Images/Logo.png",
            size_hint=(1.5,1.5),
            pos_hint={"center_x": .5, "center_y": 1}
                                )
        self.ids.LY1.add_widget(self.logo_image)




        self.enter_button = Button(
            text="",
            background_normal="Images/enter.png",
            # background_down="Images/enter.png",
            font_size=50,
            size_hint=(1,1),
            pos_hint={"center_x": .5, "center_y": .9}
                               )
        self.ids.LY1.add_widget(self.enter_button)



class WindowManager(ScreenManager):
    pass

class SaniStore(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="First"))
        return sm

if __name__ == "__main__":
    SaniStore().run()
