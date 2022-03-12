from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock


class Login(MDScreen):
    pass

class Signup(MDScreen):
    pass

class Dashboard(MDScreen):
    pass

class Journal(MDScreen):
    pass

class JournalEntry(MDScreen):
    pass

class SmallStepsApp(MDApp):
      def build(self):
        screen_manager = Builder.load_file("screenbuild.kv")
        return screen_manager

if __name__ == "__main__":
    SmallStepsApp().run()