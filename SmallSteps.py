from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.toast import toast
from kivy import platform
#from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
    

class Login(MDScreen):
    #enter code for verification user here
    def login_user(self):
        username = self.username.text #this is how you get text from the fields. it's self.<textfield id>.text
        if username != "": #edit this to check for username and password verfifcation
            self.manager.transition.direction = "left"
            self.manager.current = "dashboard"  
        else:# this section is to display an invalid message for a short period of time at the bottom of the screen
            if platform == "android":
                toast("Invalid password or username", gravity=80)# gravity=80 is to ensure it pops up at the bottom of the screen for the phone, it would pop up in the center if this wasn't here
            else:
                toast("Invalid password or username")
   

class Signup(MDScreen):
    #enter code for saving user
    #Required fields are set on the page so check if they're empty and do the toast thing I did in the login class for any errors
    #Ensure, when you are using the toast method to flash a message on the screen, to test for the platfrom being android, the else was for it to display on the laptop
    def signup_user(self):


        self.manager.transition.direction = "right" #anything with self.manager is responsible for changing the screen
        self.manager.current = "login"
        

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
        self.manager.transition.direction = "right"
        self.manager.current = "journal"
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