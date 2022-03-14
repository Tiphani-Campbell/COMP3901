from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
#from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


class Login(MDScreen):
    #enter code for verification user here
    def login_user(self):
        pass
   

class Signup(MDScreen):
    #enter code for saving user
    def signup_user(self):
        pass

class Dashboard(MDScreen):
    pass

class Journal(MDScreen):
    #edit this function to receive the list of entry records from the query
    #firstly check if the person has any journal entries and if they do run the for loop(to the amount of entries they have)
    #the text variable will store the title and date of the entry
    def on_enter(self):
        for i in range(0,10):
            self.ids.entrylist.add_widget(
                Entry(text='date', text1='title')
            )

class JournalEntry(MDScreen):
    #add code to save entry
    def save(self):
        pass

class Entry(BoxLayout):
    text = StringProperty()
    text1 = StringProperty()

class SmallStepsApp(MDApp):
      def build(self):
        screen_manager = Builder.load_file("screenbuild.kv")
        return screen_manager

if __name__ == "__main__":
    SmallStepsApp().run()