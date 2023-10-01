from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
class DropField(BoxLayout, DragBehavior):
    pass
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # self.orientation = "vertical"
    #     self.register_event_type("on_dropfile")
    #
    # def on_dropfile(self, touch):
    #     file_path = touch.profile.get("file_path", "")
    #     if file_path:
    #         pass
    #         # label = Label(text=file_path)
    #         # self.add_widget(label)
    #
    # def on_touch_up(self, touch):
    #     if self.collide_point(*touch.pos):
    #         self.dispatch("on_dropfile", touch)
    #     super().on_touch_up(touch)