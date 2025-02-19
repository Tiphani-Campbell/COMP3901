from turtle import title
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty
from kivymd.toast import toast
from kivy import platform
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import sqlite3 
from datetime import date
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import ScreenManager
from plyer import tts
import csv
import random
import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import os
import pickle
import numpy as np

global respon, CurrFeeling, un
CurrFeeling = ""
un = ""
respon=[]

class WindowManager(ScreenManager):
    Builder.load_file("screenbuild.kv")  

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
                global un
                un = username

                


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
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        if uname != "" and username != "" and password != "" and confirm != "" :
            testing  = f"SELECT COUNT (*) FROM user WHERE username = ?;"
            val = curs.execute(testing, (username,)).fetchone()[0]
            print (val)
            if val == 0:
                if password == confirm:
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
                    toast("Username is taken! Please try again", gravity=80)
                else:
                    toast("Username is taken! Please try again")
        
        else:
            if platform == "android":
                toast("Please fill all fields", gravity=80)
            else:
                toast("Please fill all fields")
       

class Dashboard(MDScreen):
    
    #edit this section to generate the recommended plans from the database.  - needs to be updated/displays everything doesnt check for disorder
    def on_enter(self):
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        if CurrFeeling != "":
            allplans = "SELECT plans, exercises FROM plantypes WHERE disorder = ?"
            plans=curs.execute(allplans,(CurrFeeling,)).fetchall()

            self.ids.reclist.clear_widgets()

            if CurrFeeling == "Anxiety":
                plans = plans[0:4]
                for plan in plans:
                    self.ids.reclist.add_widget(RecommendedPlans(plan_title= plan[0], exercises=plan[1] + " " + "exercises"))
            elif CurrFeeling == "Normal":
                plans = plans[0:2]
                for plan in plans:
                    self.ids.reclist.add_widget(RecommendedPlans(plan_title= plan[0], exercises=plan[1] + " " + "exercises"))
            else:
                plans = plans[0:3]
                for plan in plans:
                    self.ids.reclist.add_widget(RecommendedPlans(plan_title= plan[0], exercises=plan[1] + " " + "exercises"))

                
            

        con.commit()
        con.close()
        
    

class Journal(MDScreen):
    #edit this function to receive the list of entry records from the query
    #firstly check if the person has any journal entries and if they do run the for loop(to the amount of entries they have)
    #the text variable will store the title and date of the entry
    def on_enter(self):
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        check = f"SELECT COUNT (*) FROM journalentries WHERE username = '{un}';"
        numentries = curs.execute(check)
        print (numentries)
        if numentries != 0:
            curs.execute("SELECT * FROM journalentries WHERE username = ?", (un,))
            entries = curs.fetchall()


            self.ids.entrylist.clear_widgets()
     
            for entry in entries:
                self.ids.entrylist.add_widget(
                    Entry(text=entry[3], text1=entry[1])
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
        task2= "DELETE FROM journalentries WHERE title=? OR entry = ? AND username = ?"
        curs.execute(task2, (title,entry, un,))
        curs.execute("INSERT INTO journalentries VALUES (:username, :title, :entry, :date) ",
        {
            'username' : un,
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
    global questions, getquest, track, CurrFeeling
    track = [1,2,3,4,5,6, 7, 8]

    def getquest(qlist):  #generates question list
        global questionlist 
        questionlist = qlist

    def questions(): #loops through list one by one
        questlist = questionlist
        closing = "It was nice talking with you \nNow I will be calculating a feeling based on your answers."
        if questlist != []:
            question = questlist.pop(0)
            return question 
        else:
            
            print (respon)

            array = np.array(respon)

            newarr= array.reshape(1,-1)

            disorder = pickle.load(open('disorder.pkl','rb'))

            print(disorder.predict(newarr))
            global CurrFeeling
            CurrFeeling= disorder.predict(newarr)[0]
            if CurrFeeling==1:
                print("Anxiety")
                CurrFeeling="Anxiety"
            elif CurrFeeling==2:
                print("Depression")
                CurrFeeling="Depression"
            elif CurrFeeling==3:
                print("Loneliness")
                CurrFeeling="Loneliness"
            elif CurrFeeling==4:
                print("Stress")
                CurrFeeling="Stress"
            elif CurrFeeling==5:
                print("Normal")
                CurrFeeling="Normal"
            respon.clear()
            return closing


    
    def clearchat(self):
        self.ids.chatbox.clear_widgets()
        respon.clear()

    def on_enter(self):
        n = track.pop()
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        query = f"SELECT * FROM questions WHERE rowid = '{n}';"
        get = curs.execute(query).fetchall()
            
        
        con.commit()
        con.close()

        quest = list(sum(get, ())) 

        greeting = "Hi, let's chat for a bit"
        first = quest.pop(0)
       

        self.ids.chatbox.add_widget(Response(text=greeting))
        tts.speak(greeting)
        self.ids.chatbox.add_widget(Response(text=first))
        tts.speak(first) 
        getquest(quest)

    #add code to process text message here
    def sendmess(self):
        
        responlistT=["yes","sometimes", "yeah", "yep", "yea", "maybe", "a little", "i am","sure"]
        responlistF=["no","never", "not really", "nah", "nope"]
        usermess=self.ids.usertext.text
        if usermess!="":
            size=0
            if len(usermess)<6:
                size = 0.12
            elif len(usermess)< 11:
                size = 0.2
            elif len(usermess) < 16:
                size = 0.22
            elif len(usermess)<21:
                size=0.28
            elif len(usermess)<26:
                size = 0.3
            else:
                size = 0.4
            self.ids.chatbox.add_widget(UserMessage(text=usermess, size_hint_x = size))
            usermess=usermess.lower()
            if any(x in usermess for x in responlistT):
                #print("1")
                respon.append(1)
            else:
            #print("0")
                respon.append(0)

            next = questions()#calls for the next question in the list
            if next == "It was nice talking with you \nNow I will be calculating a feeling based on your answers.":
                tts.speak(next)
                self.ids.chatbox.add_widget(Response(text=next))
                self.ids.usertext.text = ""
                FPredict="I am predicting that your current feeling is " + CurrFeeling
                tts.speak(FPredict)
                self.ids.chatbox.add_widget(Response(text=FPredict))
                self.ids.usertext.text = ""
            else:
                tts.speak(next)
                self.ids.chatbox.add_widget(Response(text=next))
                self.ids.usertext.text = ""

        
     #add code to listen to user here and also test if the platform is android before doing the talk fucntion.
     # if it is android, display a message 'This feature is available on PC only'.  
    
    def talk(self):
        import winsound
        beepfreq = 1000
        due = 1000
        winsound.Beep(beepfreq, due)

        #Sampling frequency
        freq = 44100
        #Recording duration
        duration = 5
        #Start recorder with the given values of 
        #duration and sample frequency
        recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=2)

        # Record audio for the given number of seconds
        sd.wait()
        if os.path.exists("recording1.wav"):
            os.remove("recording1.wav")
        wv.write("recording1.wav", recording, freq, sampwidth=2)
        

    def stoptalk(self):
        
        #Initiаlize  reсоgnizer  сlаss  (fоr  reсоgnizing  the  sрeeсh)
        r = sr.Recognizer()
        #Reading Audio file as source
         # listening  the  аudiо  file  аnd  stоre  in  аudiо_text  vаriаble
        with sr.AudioFile('recording1.wav') as source:
            audio_text = r.listen(source)
        #recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            try:
                # using google speech recognition
                textr = r.recognize_google(audio_text)
                print('Converting audio transcripts into text ...')
                print(textr)
            except:
                print('Sorry.. run again...')

        size=0

        if len(textr)<6:
            size = 0.12
        elif len(textr)< 11:
            size = 0.2
        elif len(textr) < 16:
            size = 0.22
        elif len(textr)<21:
            size=0.28
        elif len(textr)<26:
            size = 0.3
        else:
            size = 0.4

        self.ids.chatbox.add_widget(UserMessage(text=textr, size_hint_x = size))
        responlistT=["yes","sometimes", "yeah", "yep", "yea", "maybe", "a little", "i am","ya"]
        print ("IM here")
        textr=textr.lower()
        if any(x in textr for x in responlistT):
           #print("1")
           respon.append(1)
        else:
           #print("0")
            respon.append(0)
        #tts.speak(textr) 
        next = questions() #calls for the next question in the list
        if next == "It was nice talking with you \nNow I will be calculating a feeling based on your answers.":
            tts.speak(next)
            self.ids.chatbox.add_widget(Response(text=next))
            self.ids.usertext.text = ""
            FPredict="I am predicting that your current feeling is " + CurrFeeling
            tts.speak(FPredict)
            self.ids.chatbox.add_widget(Response(text=FPredict))
            self.ids.usertext.text = ""
        else:
            tts.speak(next)
            self.ids.chatbox.add_widget(Response(text=next))
            self.ids.usertext.text = ""
        

class Progress(MDScreen):
    #write code here to mark an exercise complete
    plan_title = StringProperty()
    def complete(self):
        ptype = self.ids.title
        comp = "COMPLETED"
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        dotask= "DELETE FROM usersplans WHERE username = ? AND plans = ?"
        curs.execute(dotask, (un, ptype,))
        curs.execute("INSERT INTO usersplans VALUES (:username, :plans, :exercises) ",
        {
            'username': un,
            'plans' : ptype,
            'exercises': comp

        }
        )

       
        con.commit()
        con.close()
       
        self.manager.transition.direction = "right"
        self.manager.current = "plans"

class ChosenPlan(MDScreen):
    #edit this section to show all chosen plans
    def on_enter(self):
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        check = f"SELECT COUNT (*) FROM usersplans WHERE username = '{un}';"
        numplans = curs.execute(check)
        if numplans != 0:
            curs.execute("SELECT * FROM usersplans WHERE username = ?", (un,))
            currentplans = curs.fetchall()


            MDApp.get_running_app().screen_manager.get_screen("plans").ids.aclist.clear_widgets()


     
            for current in currentplans:
                self.ids.aclist.add_widget(ActivePlans(plan_title=current[1], exercises= current[2]))
                 

        con.commit()
        con.close()

class Entry(BoxLayout):
    text = StringProperty()
    text1 = StringProperty()
    
    def open_menu(self):
        self.menu_list=[
            {
                "text": "View Entry",
                "viewclass":"OneLineListItem",
                "on_release": lambda x = "View":self.viewentry()
            },
            {
                "text" : "Delete Entry",
                "viewclass": "OneLineListItem",
                "on_release": lambda x = "Delete" :self.deleteentry()
            }
        ]

        
        self.menu = MDDropdownMenu(
            caller =self.ids.menubutton,
            items = self.menu_list,
            width_mult = 2
        )
        self.menu.open()

    #works now, so edit this to view entry
    def viewentry(self):
        title = self.ids.title.text
        date = self.ids.date.text
        entry = Entry(text=date, text1=title)
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        task1 = curs.execute("SELECT * FROM journalentries WHERE username = :u AND title = :t AND date = :d",
            {
                'u': un,
                't' : title,
                'd': date
            }
        ).fetchone()
        entryinfo = task1[2]
        
        con.commit()
        con.close()
            
        
        MDApp.get_running_app().screen_manager.transition.direction = "left"
        MDApp.get_running_app().screen_manager.current = "journalentry"
        MDApp.get_running_app().screen_manager.get_screen("journalentry").ids.title.text = title
        MDApp.get_running_app().screen_manager.get_screen("journalentry").ids.entry.text = entryinfo
        
    

        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        check = f"SELECT COUNT (*) FROM journalentries WHERE username = '{un}';"
        numentries = curs.execute(check)
        if numentries != 0:
            curs.execute("SELECT * FROM journalentries WHERE username = ?", (un,))
            entries = curs.fetchall()


            MDApp.get_running_app().screen_manager.get_screen("journal").ids.entrylist.clear_widgets()
     
            for entry in entries:
                MDApp.get_running_app().screen_manager.get_screen("journal").ids.entrylist.add_widget(
                    Entry(text=entry[3], text1=entry[1])
                )           

        con.commit()
        con.close()
        self.menu.dismiss()
        
        
    
    #put code here to delete an entry
    def deleteentry(self):
        title = self.ids.title.text
        date = self.ids.date.text
        entry = Entry(text=date, text1=title)
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        task1 = curs.execute("SELECT * FROM journalentries WHERE username = :u AND title = :t AND date = :d",
            {
                'u' : un,
                't' : title,
                'd': date
            }
        ).fetchone()
        entryinfo = task1[2]
        task2= "DELETE FROM journalentries WHERE username= ? AND title=? AND entry = ? "
        curs.execute(task2, (un, title,entryinfo,))
        
        con.commit()
        con.close()
        MDApp.get_running_app().screen_manager.get_screen("journal").remove_widget(entry)

        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        check = f"SELECT COUNT (*) FROM journalentries WHERE username= '{un}';"
        numentries = curs.execute(check)
        if numentries != 0:
            curs.execute("SELECT * FROM journalentries WHERE username= ?", (un,))
            entries = curs.fetchall()


            MDApp.get_running_app().screen_manager.get_screen("journal").ids.entrylist.clear_widgets()
     
            for entry in entries:
                MDApp.get_running_app().screen_manager.get_screen("journal").ids.entrylist.add_widget(
                    Entry(text=entry[3], text1=entry[1])
                )           

        con.commit()
        con.close()
        self.menu.dismiss()


        
        
class UserMessage(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()

class RecommendedPlans(MDCard):
    plan_title = StringProperty()
    exercises = StringProperty() #number of exercises

    
    def choose_plan(self):
        plantype = self.ids.title.text
        numex = self.ids.num_exercises.text
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        curs.execute("INSERT INTO usersplans VALUES (:username, :plans, :exercises) ",
        {
            'username': un,
            'plans' : plantype,
            'exercises': numex
        }
        )
        
        con.commit()
        con.close()
        
        MDApp.get_running_app().screen_manager.transition.direction = "left"
        MDApp.get_running_app().screen_manager.current = "plans"
        
    

class ActivePlans(MDCard):
    plan_title = StringProperty() 
    exercises = StringProperty() #number of exercises

    #write code here to delete a plan, the steps are similar to deleting a journal entry
    def delete_plan(self): #incomplete- error in removing widgets
        planname = self.ids.title.text
        exerc = self.ids.num_exercises.text
        type = ActivePlans(plan_title=planname, exercises= exerc)
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        task= "DELETE FROM usersplans WHERE username = ? AND plans= ? AND exercises = ?"
        curs.execute(task, (un, planname, exerc,))
        
        con.commit()
        con.close()
        MDApp.get_running_app().screen_manager.get_screen("plans").remove_widget(type)

        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        check = f"SELECT COUNT (*) FROM usersplans WHERE username = '{un}';"
        numplans = curs.execute(check)
        if numplans != 0:
            curs.execute("SELECT * FROM usersplans WHERE username = ?", (un,))
            plans = curs.fetchall()


            MDApp.get_running_app().screen_manager.get_screen("plans").ids.aclist.clear_widgets()
     
            for plan in plans:
                MDApp.get_running_app().screen_manager.get_screen("plans").ids.aclist.add_widget(
                    ActivePlans(plan_title=plan[1], exercises= plan[2])
                )           

        con.commit()
        con.close()
        
    #write code here to display the exercises in a plan
    def view_exercises(self):
        type = self.ids.title.text
        MDApp.get_running_app().screen_manager.transition.direction = "left"
        MDApp.get_running_app().screen_manager.current = "progress"
        MDApp.get_running_app().screen_manager.current_screen.ids.exlist.clear_widgets()
        MDApp.get_running_app().screen_manager.current_screen.ids.title = self.plan_title

        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        getlist = "SELECT * FROM exerciselist WHERE types=?"
        exer = curs.execute(getlist, (type,))
        activities = list(exer)
        activities.pop(0)
        
        
        
        for activity in activities[0]:
            MDApp.get_running_app().screen_manager.current_screen.ids.exlist.add_widget(
                Label(
                    text=activity,
                    halign = "center",
                )
                )
        
        con.commit()
        con.close()

        
    
        

class SmallStepsApp(MDApp):
    def on_start(self):
        popup=Popup(title='Notice', title_color=[0,0,0,1], separator_color=[1,0,1,1], title_align='center', size_hint= (None, None),size=(600,400),background='white',content=Label(text='Small Steps is not to be used as a replacement for a mental health professional.\n If this application does not suit your needs you may visit www.imalive.org', color=[0,0,0,1]))
        popup.open()

    def build(self):
        con = sqlite3.connect('journaldata.db')
        curs = con.cursor()
        curs.execute("""CREATE TABLE if not exists user (name text, username text, password text)""")
        curs.execute("""CREATE TABLE if not exists journalentries (username text, title text, entry text, date text)""")
       
        curs.execute("""CREATE TABLE if not exists questions (nervous text, panic text, breathingrapidly text, sweating text, troubleinconcentration text,
            insomnia text, troublewithwork text, hopelessness text, anger text, changeineating text, suicidalthought text, feelingtired text,
            closefriend text, intrusivethoughts text, havenightmares text, antisocial text, feelingnegative text, troubleconcentrating text, blameself text)""")
        
        
        curs.execute("""CREATE TABLE if not exists plantypes (plans text, disorder text, exercises text)""")
        curs.execute("""CREATE TABLE if not exists usersplans (username text, plans text, exercises text)""")
        curs.execute("""CREATE TABLE if not exists exerciselist (types text, exercise1 text, exercise2 text,
            exercise3 text, exercise4 text, exercise5 text, exercise6 text, exercise7 text, exercise8 text, 
            exercise9 text, exercise10 text, exercise11 text)""")

        file = open('quests.csv')
        contents = csv.reader(file)
        insertrec = "INSERT INTO questions (nervous, panic, breathingrapidly, sweating, troubleinconcentration, insomnia, troublewithwork, hopelessness, anger, changeineating, suicidalthought, feelingtired, closefriend, intrusivethoughts, havenightmares, antisocial, feelingnegative, troubleconcentrating, blameself) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        curs.executemany(insertrec, contents)
        
        
        pfile = open('plans.csv')
        pcontents = csv.reader(pfile)
        insertp = "INSERT INTO plantypes (plans, disorder, exercises) VALUES (?, ?, ?)"
        curs.executemany(insertp, pcontents)
        
        efile = open('exercises.csv')
        econtents = csv.reader(efile)
        insertex = "INSERT INTO exerciselist (types, exercise1, exercise2, exercise3, exercise4, exercise5, exercise6, exercise7, exercise8, exercise9, exercise10, exercise11) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        curs.executemany(insertex, econtents)
        
        con.commit()
        con.close()

        self.screen_manager = WindowManager()
        

        return self.screen_manager

    

if __name__ == "__main__":
    SmallStepsApp().run()