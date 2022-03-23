from turtle import title
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.toast import toast
from kivy import platform
#from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import sqlite3 
from datetime import date
from kivymd.uix.label import MDLabel
    

class Login(MDScreen):
    #enter code for verification user here
    def login_user(self):
        username = self.username.text #this is how you get text from the fields. it's self.<textfield id>.text
        password = self.password.text
        if username != "" and password != "": #edit this to check for username and password verfifcation
            con = sqlite3.connect('journaldata.db')
            curs = con.cursor()
            check = f"SELECT username FROM user WHERE username = '{username}' AND password = '{password}';"
            curs.execute(check)
            if not curs.fetchone() :
                if platform == "android":
                    toast("Please enter a valid username or password", gravity=80)# gravity=80 is to ensure it pops up at the bottom of the screen for the phone, it would pop up in the center if this wasn't here
                else:
                    toast("Please enter a valid username or password")
            else:
                self.manager.transition.direction = "left"
                self.manager.current = "dashboard"  
                
            

            

            con.commit()
            con.close()

                
        else:# this section is to display an invalid message for a short period of time at the bottom of the screen
            if platform == "android":
                toast("Please fill all fields", gravity=80)# gravity=80 is to ensure it pops up at the bottom of the screen for the phone, it would pop up in the center if this wasn't here
            else:
                toast("Please fill all fields")


    
   

class Signup(MDScreen):
    #enter code for saving user
    #Required fields are set on the page so check if they're empty and do the toast thing I did in the login class for any errors
    #Ensure, when you are using the toast method to flash a message on the screen, to test for the platfrom being android, the else was for it to display on the laptop
    def signup_user(self):
        uname = self.ids.name.text
        username = self.ids.username.text
        password = self.ids.password.text
        confirm = self.ids.confirmpass.text
        if uname != "" and username != "" and password != "" and confirm != "" :
            if password == confirm:
                con = sqlite3.connect('journaldata.db')
                curs = con.cursor()
                curs.execute("INSERT INTO user VALUES(:name, :username, :password)",
                    {
                        'name' : uname,
                        'username': username,
                        'password': password
                    }
                )
               
 

                con.commit()
                con.close()

                self.manager.transition.direction = "right" #anything with self.manager is responsible for changing the screen
                self.manager.current = "login"
            else:
                if platform == "android":
                    toast("Not the same password! Please try again", gravity=80)
                else:
                    toast("Not the same password! Please try again")
       
        else:
            if platform == "android":
                toast("Please fill all fields", gravity=80)
            else:
                toast("Please fill all fields")
       

class Dashboard(MDScreen):
    pass

class Journal(MDScreen):
    #edit this function to receive the list of entry records from the query
    #firstly check if the person has any journal entries and if they do run the for loop(to the amount of entries they have)
    #the text variable will store the title and date of the entry
    def on_enter(self):
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        check = f"SELECT COUNT (*) FROM journalentries;"
        numentries = curs.execute(check)
        if numentries != 0:
            curs.execute("SELECT * FROM journalentries")
            entries = curs.fetchall()


            self.ids.entrylist.clear_widgets()
     
            for entry in entries:
                self.ids.entrylist.add_widget(
                    Entry(text=entry[2], text1=entry[0])
                )
     
                    

        con.commit()
        con.close()
               
                     

class JournalEntry(MDScreen):
    #add code to save entry
    def save(self):
        title = self.ids.title.text
        entry = self.ids.entry.text
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        curs.execute("INSERT INTO journalentries VALUES (:title, :entry, :date) ",
        {
            'title' : title,
            'entry' : entry,
            'date': date.today()

        }
        )

        self.ids.title.text = ''
        self.ids.entry.text = ''


        con.commit()
        con.close()
        self.manager.transition.direction = "right"
        self.manager.current = "journal"
        

class ChatBot(MDScreen):
    #add code to listen and respond to a user here
    #there's a label that says tap to speak, change it when to 'Listening' when the app is waiting for input,
    #change it to 'Speaking' when the app is speaking
    def talk(self):
        self.ids.chatbox.add_widget(UserMessage(text='blah'*30))
        self.ids.chatbox.add_widget(Response(text='blah'*30))
        

class Entry(BoxLayout):
    text = StringProperty()
    text1 = StringProperty()

class UserMessage(MDLabel):
    text = StringProperty()
    

class Response(MDLabel):
    text = StringProperty()
    
    

class SmallStepsApp(MDApp):
    def build(self):
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        curs.execute("""CREATE TABLE if not exists user (name text, username text, password text)""")
        curs.execute("""CREATE TABLE if not exists journalentries (title text, entry text, date text)""")
        curs.execute("""CREATE TABLE if not exists journal (title text, entry text, date text)""")
        


        con.commit()
        con.close()

        screen_manager = Builder.load_file("screenbuild.kv")
        return screen_manager

if __name__ == "__main__":
    SmallStepsApp().run()
