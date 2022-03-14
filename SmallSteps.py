from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty


class Login(MDScreen):
    pass

class Signup(MDScreen):
    pass

class Dashboard(MDScreen):
    pass

class Journal(MDScreen):
    
    def on_enter(self):
        for i in range(0,10):
            self.ids.entrylist.add_widget(
                Entry(line_color=(0.2, 0.2, 0.2, 0.8),
                    style="elevated",
                    text="plan",
                    md_bg_color=get_color_from_hex("#f6eeee"),)
            )
    

class Entry(MDCard, RoundedRectangularElevationBehavior):
    text = StringProperty()
    
class JournalEntry(MDScreen):
    pass

class SmallStepsApp(MDApp):
      def build(self):
        screen_manager = Builder.load_file("screenbuild.kv")
        return screen_manager

if __name__ == "__main__":
    SmallStepsApp().run()