import tkinter as tk
from tkinter import Entry, Label, Button, StringVar, CENTER, Canvas, Frame, Listbox, END, LEFT, BOTH, HORIZONTAL, messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import *
import pandas as pd
import webbrowser  
from tkinter.ttk import Progressbar
from PIL import ImageTk
import PIL.Image
import keyboard
import random
import requests, tweepy
import datetime
 
 
'''
Lucas Iredale  
Webb Prosser AM Class
Capstone Project
5/13/22
Version 4.563
'''
 
#different keys for spotify and twitter API
 
client_id='af0fb869939d403f9bcc1f9db796b615'
client_secret='067ec26f1a0449639ed6a9a59b501de7'  
redirect_url='http://example.com'
 
consumer_key = "nLqXDKExYV4PvbUHlissgzmeR"
consumer_secret = "yBW9N0mqB8sRLO0ctY6e9rRPxcrCnTfjO2BOFlibeJp4iXJP8g"
access_token = "1524960183327268864-4ZYdJKK3TR6YEPQGgkPNdszt9TepdX"
access_token_secret = "mwiqUYKhb2J1FtZWIPF74FvR0cxocDguguFC5W61whzaw"
 
#Rgb To Hex for easy access to colors.
def rgbToHex(rgb):
  return '#%02x%02x%02x' % rgb
 
#Easy to call black and white hex
WHITE = '#FFFFFF'
BLACK = '#000000'
 
 
def start(): #function to start the code, log in code
    if __name__ == "__main__":
        lI = logIn()
        lI.mainloop()
 
def startMW(): #function to start the main window organizer
    if __name__ == "__main__":
        mw = mainWindow()
        mw.mainloop()
 
class logIn(tk.Tk): #class to log in window tkinter
    def __init__(self): #initialize tkinter log in window
        super().__init__()
        #sets simple background + size
        self.geometry("600x600")
        self.configure(bg = rgbToHex((100,100,100)))
        #buttons to go to register or sign in
        self.regButton = Button(self, text = "Register", font = "Helvetica 24", bg = rgbToHex((150, 100, 100)), fg = WHITE, command = self.register)
        self.regButton.place(relx = .5, rely = .3, anchor = CENTER)
        self.sigButton = Button(self, text = "Sign In", font = "Helvetica 24", bg = rgbToHex((150, 100, 100)), fg = WHITE, command = self.signIn)
        self.sigButton.place(relx = .5, rely = .5, anchor = CENTER)
 
    def regSubmit(self): #happens when register submits, writes the password and username to data.txt
        with open("data.txt", "a") as f:
            f.write(self.userVar.get() + ": " + self.passVar.get() + "\n")
        self.destroy()
        start()
       
    def logInSubmit(self): #this will take the log in code, check to see if it is in data.txt, and then takes to main window
        stat = False
        file=open('data.txt', 'r')
        f = file.readlines()
        for i in range(len(f)):
            if len(self.userVarSI.get()) > 0 and len(self.passVarSI.get()) > 0:
                if self.userVarSI.get() in f[i] and self.passVarSI.get() in f[i]:
                    self.destroy()
                    mw = mainWindow()
                    mw.mainloop()
           
 
               
 
    def register(self): #this creates different labels and entries for the username and password to register
        self.regButton.destroy()
        self.sigButton.destroy()
        self.titLab = Label(self, text = "Register", font = "Helvetica 24", bg = rgbToHex((100, 100, 100)), fg = BLACK).place(relx=.5, rely=0.05, anchor = CENTER)
        self.userVar = StringVar()
        self.userLab = Label(self, text = "Username: ", font = 'Helvetica 16', bg = rgbToHex((100, 100, 100)), fg = BLACK).place(relx=.3, rely=.4, anchor = CENTER)
        self.userEntry = Entry(self, width = 10, font = "Helvetica 16", textvariable = self.userVar).place(relx=.51, rely=.4, anchor = CENTER)
        self.passVar = StringVar()
        self.passLab = Label(self, text = "Password: ", font = "Helvetica 16", bg = rgbToHex((100, 100, 100)), fg = BLACK).place(relx=.3, rely= .5, anchor = CENTER)
        self.passEntry = Entry(self, width = 10, font = "Helvetica 16", textvariable = self.passVar).place(relx=.51, rely=.5, anchor = CENTER)
        self.subButton = Button(self, text = "Submit", font = "Helvetica 16", bg = rgbToHex((150, 100, 100)), fg = WHITE, command = lambda: self.regSubmit()).place(relx=.5, rely=.7, anchor = CENTER)
       
    def signIn(self): #this creates different labels and entries for the username and password to sign in
        self.regButton.destroy()
        self.sigButton.destroy()
        self.titLab = Label(self, text = "Log In", font = "Helvetica 24", bg = rgbToHex((100, 100, 100)), fg = BLACK).place(relx=.5, rely=0.05, anchor = CENTER)
        self.userVarSI = StringVar()
        self.userLab = Label(self, text = "Username: ", font = 'Helvetica 16', bg = rgbToHex((100, 100, 100)), fg = BLACK).place(relx=.3, rely=.4, anchor = CENTER)
        self.userEntry = Entry(self, width = 10, font = "Helvetica 16", textvariable = self.userVarSI).place(relx=.51, rely=.4, anchor = CENTER)
        self.passVarSI = StringVar()
        self.passLab = Label(self, text = "Password: ", font = "Helvetica 16", bg = rgbToHex((100, 100, 100)), fg = BLACK).place(relx=.3, rely= .5, anchor = CENTER)
        self.passEntry = Entry(self, width = 10, font = "Helvetica 16", textvariable = self.passVarSI).place(relx=.51, rely=.5, anchor = CENTER)
        self.subButton = Button(self, text = "Log In", font = "Helvetica 16", bg = rgbToHex((150, 100, 100)), fg = WHITE, command = self.logInSubmit).place(relx=.5, rely=.7, anchor = CENTER)
 
class spotRecommend(tk.Tk): #creates class for tkinter window for spotify recommendation
    def __init__(self): #this will intiailize and create the spotify window
        super().__init__()
        #does some basic lines of code to create and configure window
        self.configure(bg = rgbToHex((150,0,0)))
        self.geometry("600x600")
        #creates many different lists and objects for spotify, then runs continue onwards def
        self.genreFav = []
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret= client_secret, redirect_uri=redirect_url))
        self.songFav = []
        self.active = False
        self.continueOnwardsDef()
        self.goBackButt = Button(self, text = "Go Back", font = "Helvetica 12", bg = BLACK, fg = WHITE, command = lambda: self.goBack()).place(relx=.85, rely=.05)
   
   
    def callback(self): #this is the code for when someone clicks "search". creates a listbox then adds different search results to the listbox
        self.active = True
        self.ml = Listbox(self.fr, font = "Helvetica 12", bg = BLACK, fg = WHITE, width = 50)
        if len(self.search.get()) == 0:
            pass
        if __name__ == '__main__':
 
            #gets token for spotify API
            token = util.prompt_for_user_token("bobcat3610",client_id="af0fb869939d403f9bcc1f9db796b615", client_secret="067ec26f1a0449639ed6a9a59b501de7",redirect_uri="https://example.com/callback/")
           
 
            if token: #gets spotify object, searches for the search results, adds each to a pandas dataframe
                self.sp = spotipy.Spotify(auth=token)
                for i in range(0, 50, 50):
                    results = self.sp.search(q= self.search.get(), type = "track", limit = 10, offset = i)
                    self.artist_name = []
                    self.track_name = []
                    self.popularity = []
                    self.track_id = []
 
                    for i, t in enumerate(results['tracks']['items']):
                        self.artist_name.append(t['artists'][0]['name'])
                        self.track_name.append(t['name'])
                        self.track_id.append(t['id'])
                        self.popularity.append(t['popularity'])
                   
                    self.df = pd.DataFrame({'artist_name' : self.artist_name, 'track_name' : self.track_name, 'track_id' : self.track_id, 'popularity' : self.popularity})
                #adds objects to listbox to select
                for i in range(10):
                    self.searchButt.destroy()
                    self.ml.insert(END, str(i) + ". " + self.track_name[i] + " by " + self.artist_name[i])
                    self.ml.pack(side = LEFT, fill = BOTH)
                self.nextSearch = Button(self, text = "Do Another Search", font = "Helvetica 14", bg = WHITE, command = self.backFromCB)
                self.nextSearch.place(relx=.5,rely=.8,anchor = CENTER)
                   
    def makeLayout(self, num, col, row): #makes layout for the final search, then takes the search results and puts them all on the frame
        f = Frame(self, width = 200, height = 150, bg = rgbToHex((50*col,50*row,50)))
        f.place(x=col*200,y=50+row*183)
        song = Label(f, text = f"'{self.recomSong['tracks'][num]['name']}'", bg = rgbToHex((50*col,50*row,50)), fg = WHITE, font = "Helvetica 12", wraplength = 200)
        song.place(relx=.5,rely=.2,anchor = CENTER)
        artist = Label(f, text = f"{self.recomSong['tracks'][num]['artists'][0]['name']}", bg = rgbToHex((50*col,50*row,50)), fg = WHITE, font = 'Helvetica 12')
        artist.place(relx = .5, rely = .4, anchor = CENTER)
        goToButt = Button(f, text = "Play Song", bg = rgbToHex((50*col,50*row,50)), fg = WHITE, font = "Helvetica 12", command = lambda: self.openAndPlay(self.recomSong['tracks'][num]['external_urls']['spotify']))
        goToButt.place(relx=.5,rely=.6,anchor = CENTER)
        goBackButt = Button(self, text = "Go Back", font = "Helvetica 12", bg = BLACK, fg = WHITE, command = lambda: self.goBack()).place(relx=.85, rely=.05)
   
 
 
    def openAndPlay(self, link): #opens web link
        webbrowser.open(link)
 
    def goBack(self): #goes back to main window
        self.destroy()
        startMW()
 
    def findRecommended(self): #this is where it places all the labels and images on the frame
        if self.active == True and len(self.ml.curselection()) > 0:
            self.songFav.append(self.track_id[self.ml.curselection()[0]])
        self.ml.destroy()
        self.searchButt.destroy()
        self.search.destroy()
        self.nextSearch.destroy()
        self.nextStage.destroy()
        self.requestLab.destroy()
        self.titlFram = Frame(self, width = 600, height = 50, bg = rgbToHex((150,0,0)))
        self.titlFram.grid(row = 0, column = 0)
        self.titleLab = Label(self.titlFram, text = "Song Suggestions For You", font = "Helvetica 20", bg = rgbToHex((150,0,0)), fg = BLACK)
        self.titleLab.place(relx=.5,rely=.5,anchor = CENTER)
        self.recomSong = self.sp.recommendations(seed_tracks = self.songFav, limit = 9)
        col = 0
        row = 0
        for i in range(9):
            if row > 2:
                row = 0
                col += 1
            self.makeLayout(i, col, row)
 
            row += 1
 
    def backFromCB(self): #this is where it goes after one search to callback and selected a song
        self.active = False
        if len(self.ml.curselection()) > 0:
            self.songFav.append(self.track_id[self.ml.curselection()[0]])
        self.nextSearch.destroy()
        self.searchButt = Button(self, text = "Search", font = "Helvetica 20", bg = WHITE, command = lambda: self.callback())
        self.searchButt.place(relx=.5, rely=.4, anchor = CENTER)
        self.nextStage = Button(self, text = "Search For Recommended Songs", font = "Helvetica 16", bg = WHITE, command = self.findRecommended)
        self.nextStage.place(relx=.5,rely=.9,anchor = CENTER)
        self.ml.destroy()
        self.artist_name = []
        self.track_name = []
        self.popularity = []
        self.track_id = []
 
    def continueOnwardsDef(self): #this is the first function to run after it goes to spotify, sets some frames, entries, buttons, and labels
            self.requestLab = Label(self, text = "Search or Click for Songs You Enjoy", font = "Helvetica 18", bg=rgbToHex((150,0,0)))
            self.requestLab.place(relx=.5, rely=.13, anchor = CENTER)
            self.search = Entry(self, width = 40, font = 'Helvetica 16')
            self.search.place(relx=.5, rely=.2,anchor = CENTER)
            self.fr = Frame(self, height = 400, width = 250, bg = rgbToHex((150,0,0)))
            self.fr.place(x=300,y=350,anchor = CENTER)
            self.searchButt = Button(self, text = "Search", font = "Helvetica 20", bg = WHITE, command = lambda: self.callback())
            self.searchButt.place(relx=.5, rely=.4, anchor = CENTER)
 
 
 
 
 
class ticTac(tk.Tk): #tic tac toe class
    def changeTurn(self): #this will change the turn
        if self.turn == "O":
            self.turn = "X"
            return None
        if self.turn == "X":
            self.turn = "O"
            return None
    def winner(self): #this checks for a winner. it has multiple different conditions in which it destroys the canvas and displays a winner
        if self.winStat == False:
            if (self.one == "O" and self.two == "O" and self.three == "O" ) or (self.four == "O" and self.five == "O" and self.six == "O" ) or (self.seven == "O" and self.eight == "O" and self.nine == "O" ) or (self.one == "O" and self.four == "O" and self.seven == "O" ) or (self.two == "O" and self.five == "O" and self.eight == "O" ) or (self.three == "O" and self.six == "O" and self.nine == "O" ) or (self.one == "O"  and self.five == "O" and self.nine == "O" ) or (self.three == "O" and self.five == "O" and self.seven == "O"):
                self.canv.destroy()
                self.l = Label(self, text = "O Wins!", font = "Helvetica 36", bg = BLACK, fg = WHITE).place(relx=.5,rely=.3, anchor = CENTER)
                self.winStat = True
            if (self.one == "X" and self.two == "X" and self.three == "X" ) or (self.four == "X" and self.five == "X" and self.six == "X" ) or (self.seven == "X" and self.eight == "X" and self.nine == "X" ) or (self.one == "X" and self.four == "X" and self.seven == "X" ) or (self.two == "X" and self.five == "X" and self.eight == "X" ) or (self.three == "X" and self.six == "X" and self.nine == "X" ) or (self.one == "X"  and self.five == "X" and self.nine == "X" ) or (self.three == "X" and self.five == "X" and self.seven == "X"):
                self.winStat = True
                self.canv.destroy()
                self.l = Label(self, text = "X Wins!", font = "Helvetica 36", bg = BLACK, fg = WHITE).place(relx=.5,rely=.3, anchor = CENTER)
            self.after(100, lambda: self.winner())
        if self.winStat == True:
            self.after(3000, lambda: self.destroy())
 
    def changeStat(self, item, x, y): #chhanges the status of a place on the board. creates an x or o
        if item == "Z":
            if self.turn == "O":
                if x < 200:
                    if y < 200:
                        self.canv.create_oval(125, 125, 175, 175, outline = "white")
                    if y < 350 and y > 200:
                        self.canv.create_oval(125, 250, 175, 300, outline = "white")
                    if y > 350:
                        self.canv.create_oval(125, 375, 175, 425, outline = "white")
                if x < 350 and x > 200:
                    if y < 200:
                        self.canv.create_oval(250, 125, 300, 175, outline = "white")
                    if y < 350 and y > 200:
                        self.canv.create_oval(250, 250, 300, 300, outline = "white")
                    if y > 350:
                        self.canv.create_oval(250, 375, 300, 425, outline = "white")
                if x > 350:
                    if y < 200:
                        self.canv.create_oval(375, 125, 425, 175, outline = "white")
                    if y < 350 and y > 200:
                        self.canv.create_oval(375, 250, 425, 300, outline = "white")
                    if y > 350:
                        self.canv.create_oval(375, 375, 425, 425, outline = "white")
                self.changeTurn()
               
                return "O"
                       
            if self.turn == "X":
                if x < 200:
                    if y < 200:
                        self.canv.create_line(125, 125, 175, 175, fill = "white")
                        self.canv.create_line(125, 175, 175, 125, fill = "white")
                    if y < 350 and y > 200:
                        self.canv.create_line(125, 250, 175, 300, fill = "white")
                        self.canv.create_line(125, 300, 175, 250, fill = "white")
                    if y > 350:
                        self.canv.create_line(125, 375, 175, 425, fill = "white")
                        self.canv.create_line(125, 425, 175, 375, fill = "white")
                if x < 350 and x > 200:
                    if y < 200:
                        self.canv.create_line(250, 125, 300, 175, fill = "white")
                        self.canv.create_line(250, 175, 300, 125, fill = "white")
                    if y < 350 and y > 200:
                        self.canv.create_line(250, 250, 300, 300, fill = "white")
                        self.canv.create_line(250, 300, 300, 250, fill = "white")
                    if y > 350:
                        self.canv.create_line(250, 375, 300, 425, fill = "white")
                        self.canv.create_line(250, 425, 300, 375, fill = "white")
                if x > 350:
                    if y < 200:
                        self.canv.create_line(375, 125, 425, 175, fill = "white")
                        self.canv.create_line(375, 175, 425, 125, fill = "white")
                    if y < 350 and y > 200:
                        self.canv.create_line(375, 250, 425, 300, fill = "white")
                        self.canv.create_line(375, 300, 425, 250, fill = "white")
                    if y > 350:
                        self.canv.create_line(375, 375, 425, 425, fill = "white")
                        self.canv.create_line(375, 425, 425, 375, fill = "white")
                self.changeTurn()
               
                return "X"
            self.changeTurn()
       
   
    def clickDown(self, event): #this is when a click happens, checks where it happened at and sends to changestat
 
        if event.x < 200:
            if event.y < 200:
                self.one = self.changeStat(self.one, event.x, event.y)
            if event.y < 350 and event.y > 200:
                self.four = self.changeStat(self.four, event.x, event.y)
            if event.y > 350:
                self.seven = self.changeStat(self.seven, event.x, event.y)
 
        if event.x < 350 and event.x > 200:
            if event.y < 200:
                self.two = self.changeStat(self.two, event.x, event.y)
            if event.y < 350 and event.y > 200:
                self.five = self.changeStat(self.five, event.x, event.y)
            if event.y > 350:
                self.eight = self.changeStat(self.eight, event.x, event.y)
 
        if event.x > 350:
            if event.y < 200:
                self.three = self.changeStat(self.three, event.x, event.y)
            if event.y < 350 and event.y > 200:
                self.six = self.changeStat(self.six, event.x, event.y)
            if event.y > 350:
                self.nine = self.changeStat(self.nine, event.x, event.y)
 
 
    def goBack(self): #goes back to main window
        self.destroy()
        startMW()
 
    def __init__(self): #this initializes the tictactoe window
        super().__init__()
        #sets simple window, creates the board, and sets some labels, canvas, and buttons
        self.winStat = False
        self.configure(bg = BLACK)
        self.geometry("600x600")
        self.canv = Canvas(self, width = 600, height = 600, bg = BLACK)
        self.canv.place(relx=0, rely=0)
        self.titLab = Label(self.canv, text = "Tic Tac Toe", font = "Helvetica 24", bg = BLACK, fg = WHITE).place(relx=.5, rely=.1, anchor = CENTER)
        self.canv.create_line(200, 100, 200, 450, fill = "white")
        self.canv.create_line(350, 100, 350, 450, fill = "white")
        self.canv.create_line(100, 200, 450, 200, fill = "white")
        self.canv.create_line(100, 350, 450, 350, fill = "white")
        self.canv.bind("<Button-1>", self.clickDown)
        #sets assorted variables
        self.one = "Z"
        self.two = "Z"
        self.three = "Z"
        self.four = "Z"
        self.five = "Z"
        self.six = "Z"
        self.seven = "Z"
        self.eight = "Z"
        self.nine = "Z"
        self.goBackButt = Button(self, text = "Go Back", font = "Helvetica 12", bg = BLACK, fg = WHITE, command = lambda: self.goBack()).place(relx=.85, rely=.05)
        self.turn = "X"
        self.after(1000, lambda: self.winner())
 
 
class tweetSomething(tk.Tk): #creates twitter window
    def __init__(self):
        #creates background and assorted buttons and labels
        super().__init__()
        self.geometry("600x600")
        self.configure(bg = BLACK)
        self.titLab = Label(self, text = "Tweeter", font = "Helvetica 24", bg = BLACK, fg = WHITE).place(relx=.5, rely=0.05, anchor = CENTER)
        self.randTweet = Button(self, text = "Tweet a Random Kanye Tweet", font = "Helvetica 16", bg = BLACK, fg = WHITE, command = lambda: self.randTweetGo())
        self.randTweet.place(relx=.5, rely=.3, anchor = CENTER)
        self.chosenTweet = Button(self, text = "Tweet Anything", font = "Helvetica 16", bg = BLACK, fg = WHITE, command = lambda: self.chosenTweetGo())
        self.chosenTweet.place(relx=.5, rely=.5, anchor = CENTER)
        self.goBackButt = Button(self, text = "Go Back", font = "Helvetica 12", bg = BLACK, fg = WHITE, command = lambda: self.goBack()).place(relx=.85, rely=.05)
       
    def randTweetGo(self): #this is to go to the window to post a random kanye tweet
        self.randTweet.destroy()
        self.chosenTweet.destroy()
        self.k = requests.get("https://api.kanye.rest/")
        self.kanyeTweet = Label(self, text = f"{self.k.text[10:len(self.k.text)-2]}", font = "Helvetica 16", bg = BLACK, fg = WHITE, wraplength=600).place(relx=.5, rely=.3, anchor = CENTER)
        self.goButt = Button(self, text = "Tweet", font = "Helvetica 24", bg = BLACK, fg = WHITE, command = lambda: self.tweetKanye()).place(relx=.5, rely=.6, anchor = CENTER)
    def chosenTweetGo(self): #this is where you tweet the given tweet
        self.randTweet.destroy()
        self.chosenTweet.destroy()
        self.tweetVar = StringVar()
        self.tweetEntry = Entry(self, font = "Helvetica 16", width = 40, textvariable = self.tweetVar).place(relx=.5, rely=.4, anchor = CENTER)
        self.tweetButt = Button(self, text = "Tweet", font = "Helvetica 16", bg = BLACK, fg = WHITE, command = lambda: self.choseTweet()).place(relx=.5, rely=.6, anchor = CENTER)
    def choseTweet(self): #this will tweet the chosen tweet given
        messagebox.showinfo('information', 'Tweeted')
        self.after(2000, lambda: webbrowser.open("https://twitter.com/otd_quote"))
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(self.tweetVar.get())
    def tweetKanye(self): #this will tweet a random kanye quote
        messagebox.showinfo('information', 'Tweeted')
        self.after(2000, lambda: webbrowser.open("https://twitter.com/otd_quote"))
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(self.k.text[10:len(self.k.text)-2])
    def goBack(self): #goes back to main menu
        self.destroy()
        startMW()
 
class Hangman(tk.Tk): #hangman main class
 
    def checkWin(self): #this is the function to check for a win
        blanks = ""
        for i in range(len(self.word)):
                    if self.word[i] in self.correct:
                        blanks = blanks[:i] + self.word[i] + blanks[i+1:]
        if blanks == self.word[0:len(self.word)]:
            self.wordLab.destroy()
            self.wordLab = Label(self, text = blanks,font = "Helvetica 16", bg = BLACK, fg = WHITE)
            self.wordLab.place(relx=.6,rely=.4)
            return True
        if blanks != self.word[0:len(self.word)]:
            return False
       
 
 
    def drawWrong(self): #this is the code to draw the shapes of the body
        self.missLab.destroy()
        if len(self.wrong) == 1:
            self.missLab = Label(self, text = "Missed: " + self.wrong[0],font = "Helvetica 16", bg = BLACK, fg = WHITE)
            self.missLab.place(relx=.55,rely=.3)
            self.canv.create_oval(245, 222, 295, 272, outline = "white")
            self.canv.create_oval(255, 240, 260, 245, outline = "white")
            self.canv.create_oval(270, 240, 275, 245, outline = "white")
                       
 
        if len(self.wrong) == 2:
            self.missLab = Label(self, text = "Missed: " + self.wrong[0] + ", " + self.wrong[1], font = "Helvetica 16", bg = BLACK, fg = WHITE)
            self.missLab.place(relx=.55,rely=.3)
            self.canv.create_line(270, 272, 270, 350, fill = "white")
 
        if len(self.wrong) == 3:
            self.missLab = Label(self, text = "Missed: " + self.wrong[0] + ", " + self.wrong[1] + ", " + self.wrong[2],font = "Helvetica 16", bg = BLACK, fg = WHITE)
            self.missLab.place(relx=.55,rely=.3)
            self.canv.create_line(270, 290, 310, 310, fill = "white")
 
        if len(self.wrong) == 4:
            self.missLab = Label(self, text = "Missed: " + self.wrong[0] + ", " + self.wrong[1] + ", " + self.wrong[2] + ", " + self.wrong[3],font = "Helvetica 16", bg = BLACK, fg = WHITE)
            self.missLab.place(relx=.55,rely=.3)
            self.canv.create_line(270, 290, 230, 310, fill = "white")
 
        if len(self.wrong) == 5:
            self.missLab = Label(self, text = "Missed: " + self.wrong[0] + ", " + self.wrong[1] + ", " + self.wrong[2] + ", " + self.wrong[3] + ", " + self.wrong[4],font = "Helvetica 16", bg = BLACK, fg = WHITE)
            self.missLab.place(relx=.55,rely=.3)
            self.canv.create_line(270, 350, 230, 380, fill = "white")
 
        if len(self.wrong) == 6:
            self.missLab = Label(self, text = "You Lost, Word Was: " + self.word, font = "Helvetica 16", bg = BLACK, fg = WHITE)
            self.missLab.place(relx=.55,rely=.3)
            self.canv.create_line(270, 350, 310, 380, fill = "white")
            self.canv.create_line(255, 240, 260, 245, fill = "white")
            self.canv.create_line(270, 240, 275, 245, fill = "white")
            self.after(2000, self.destroy)
           
    def goBack(self): #go back to main menu
        self.destroy()
        startMW()
 
    def on_press(self, event): #this will check what key was pressed, and then do the commands for what needs to happen
        if event.name not in self.guessed and event.name in self.alpha:
            blanks = ""
            for i in range(len(self.word)):
                blanks = blanks + "_"
            if event.name in self.word:
                self.correct.append(event.name)
            if event.name not in self.word:
                self.wrong.append(event.name)
                self.drawWrong()
            if self.checkWin() == False:
                self.guessed.append(event.name)
               
               
                for i in range(len(self.word)):
                    if self.word[i] in self.correct:
                        blanks = blanks[:i] + self.word[i] + blanks[i+1:]
                self.wordLab.destroy()
                self.wordLab = Label(self, text = blanks,font = "Helvetica 16", bg = BLACK, fg = WHITE)
                self.wordLab.place(relx=.6,rely=.4)
            else:
                messagebox.showinfo('information', 'this is a good time to say holy smokes.')
                self.after(4000, lambda: self.destroy())
           
 
 
           
       
    def __init__(self): #intializes the object
        super().__init__()
        #creates simple windows, and then labels, buttons, and variables
        self.configure(bg = BLACK)
        self.geometry("600x600")
        self.title("Hangman")
        self.alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v','w','x','y','z']
        self.titLab = Label(self, text = "Hangman", font = "Helvetica 24", bg = BLACK, fg = WHITE)
        self.titLab.place(relx=.5, rely=.05, anchor = CENTER)
        self.byLonesome = Button(self, text = "Play Hangman By Yourself", font = "Helvetica 16", fg = BLACK, bg = WHITE, command = lambda: self.loneGame())
        self.byLonesome.place(relx=.5,rely=.4, anchor = CENTER)
        self.wrong = []
        self.correct = []
        self.guessed = []
        self.goBackButt = Button(self, text = "Go Back", font = "Helvetica 12", bg = BLACK, fg = WHITE, command = lambda: self.goBack()).place(relx=.85, rely=.05)
    def goBack(self): #goes back to main window
        self.destroy()
        startMW()
 
    def loneGame(self): #this is what happens when you start the game by yourself, creates labels and buttons and assorted variables. creates layout
        lines = []
        with open("words") as f:
            lines = f.readlines()
        k = random.randint(0, len(lines))
        self.word = lines[k][0:len(lines[k])-1]
        self.byLonesome.destroy()
        self.titLab.destroy()
        self.canv = Canvas(self, bg = BLACK)
        self.canv.pack(fill = BOTH, expand = 1)
        self.titLab = Label(self.canv, text = "Hangman", font = "Helvetica 24", bg = BLACK, fg = WHITE)
        self.titLab.place(relx=.5, rely=.05, anchor = CENTER)
        self.missLab = Label(self, text = "Missed: ", font = "Helvetica 16", bg = BLACK, fg = WHITE)
        self.missLab.place(relx=.55, rely=.3)
        self.wordVar = ""
        self.wordLab = Label(self, text = '_' * len(self.word), font = "Helvetica 16", bg = BLACK, fg = WHITE)
        self.wordLab.place(relx=.6,rely=.4)
        self.goBackButt = Button(self, text = "Go Back", font = "Helvetica 12", bg = BLACK, fg = WHITE, command = lambda: self.goBack()).place(relx=.85, rely=.05)
       
       
        self.canv.create_line(100, 400, 200, 400, fill = "white")
        self.canv.create_line(150, 400, 150, 200, fill = "white")
        self.canv.create_line(150, 200, 270, 200, fill = "white")
        self.canv.create_line(270, 200, 270, 220, fill = "white")
 
 
 
 
        keyboard.on_press(self.on_press)
 
 
 
 
 
class Clicker(tk.Tk): #clicker code
    def __init__(self): #initilaizes the clicker code
        super().__init__()
        #creates variables, window details, and labels/buttons and anything else needed
        self.count = 0
        self.niceGuyAmount = 0
        self.clickAmount = 1
        self.title("Clicker")
        self.geometry("1000x1000")
        self.configure(bg="#42EFE2")
        self.prestigeNum = 0
 
 
        self.goBackButt = Button(self, text = "Go Back", font = "Helvetica 12", bg = BLACK, fg = WHITE, command = lambda: self.goBack()).place(relx=.85, rely=.05)
       
        #button photo
        self.photo = PIL.Image.open('leman.jpg')
        self.resized_image=self.photo.resize((400,400),PIL.Image.ANTIALIAS)
        self.newimg = ImageTk.PhotoImage(self.resized_image)
 
        #num of clicks label
        self.label = Label(self, text="Pounds: 0",bg="#42EFE2", font="Helvetica 25")
        self.label.place(y=290, x=420)
 
        #big man button
        self.button = Button(self, command=self.click, image=self.newimg)
        self.button.place(y=335, x=300)
        self.button.configure(bg = "#42EFE2")
 
        #title
        self.title = Label(self,text="Big Man Clicker", font = "Helvetica 50")
        self.title.place(x=270,y=0)
        self.title.configure(bg="#42EFE2")
 
        #Thin Guy Upgrade
        self.thinGuy = Button(self, text = 'Thin Guy Upgrade \n 500 Pounds',command=self.tGTrue)
        self.thinGuy.place(x=0,y=300)
        self.thinGuy.configure(bg="#32BDB2")
        #Thin Guy Progress Bar
        self.progress = Progressbar(self, orient = HORIZONTAL, length = 110, mode = 'determinate')
        self.progress.place(x=0,y=360)
        self.updateTGProgressBar()
        #Thin Guy Counter
        self.TGCounter = Label(self, text = 'Thin Guy Amount: ',bg="#32BDB2",font="Helvetica, 9")
        self.TGCounter.place(x=0,y=340)
        self.after(10,self.TGCounterDef)
 
        #Rice Upgrade
        self.rice = Button(self,text="Rice \n 10 Pounds", command=self.Rice)
        self.rice.place(x=931,y=350)
        self.rice.configure(bg="#32BDB2")
        #Rice Progress Bar
        self.riceProgress = Progressbar(self, orient=HORIZONTAL, length=70,mode='determinate')
        self.riceProgress.place(x=931,y=410)
        self.updateRiceBar()
        #Rice Counter
        self.riceCounter = Label(self,text='Rice Amount: ',bg="#32BDB2",font="Helvetica 8")
        self.riceCounter.place(x=920,y=390)
        self.after(10,self.riceCounterDef)
        #prestige
        self.prestige = Button(self,text = "Prestige \n 1,000,000 Pounds", command=self.Prestige)
        self.prestige.place(x=0,y=0)
        self.prestige.configure(bg="#32BDB2")
       
    def TGCounterDef(self): #this is to change thin guy amount
        self.TGCounter.config(text="Thin Guy Amount: " + str(self.niceGuyAmount))
        self.after(10,self.TGCounterDef)
    def updateTGProgressBar(self): #changes thin guy progress bar
        if self.count == 0:
            self.progress['value'] = 0
        elif self.count >= 500:
            self.progress['value'] = 100
        elif self.count >=1 and self.count <= 499:
            self.progress['value'] = (self.count/500)*100
        self.update_idletasks()
        self.after(10,self.updateTGProgressBar)
    def updateRiceBar(self): #this updates rice bar progress bar
        if self.count == 0:
            self.riceProgress['value'] = 0
        elif self.count >= 10:
            self.riceProgress['value'] = 100
        elif self.count >=1 and self.count <= 9:
            self.riceProgress['value'] = (self.count/10)*100
        self.update_idletasks()
        self.after(10,self.updateRiceBar)
    def riceCounterDef(self): #this changes the rice amount
        self.riceCounter.config(text="Rice Amount: " + str(self.clickAmount))
        self.after(10,self.riceCounterDef)
    def updateAmount(self,amount): #updates the amount of pounds you have
        self.count+=amount
        self.label.config(text="Pounds: " + str(self.count))
   
    def click(self): #adds click amount to pounds
        self.updateAmount(self.clickAmount)
 
    def punishment(self): #when something bad happens, changes color to red
        self.changeColor()
        self.after(4000,self.changeColorBack)
 
    def changeColor(self):
        self.configure(bg= "#FF3A00")
        self.thinGuy.configure(bg= "#FF3A00")
        self.title.configure(bg= "#FF3A00")
        self.button.configure(bg= "#FF3A00")
        self.label.configure(bg="#FF3A00")
        self.rice.configure(bg="#FF3A00")
        self.TGCounter.configure(bg="#FF3A00")
        self.riceCounter.config(bg="#FF3A00")
        self.prestige.config(bg="#FF3A00")
    def changeColorBack(self): #changes color back
        self.configure(bg = "#42EFE2")
        self.thinGuy.configure(bg = "#32BDB2")
        self.title.configure(bg = "#42EFE2")
        self.button.configure(bg = "#42EFE2")
        self.label.configure(bg = "#42EFE2")
        self.rice.configure(bg="#32BDB2")
        self.TGCounter.configure(bg="#32BDB2")
        self.riceCounter.config(bg="#32BDB2")
        self.prestige.config(bg="#32BDB2")
 
    def tGTrue(self): #this is tochange the text
        if self.count >= 500:
            self.niceGuyAmount +=1
            self.count-=500
            self.label.config(text="Pounds: " + str(self.count))
            self.after(1000,self.tGBoost)
        else:
            self.punishment()
 
    def tGBoost(self): #checks the boost
        if self.niceGuyAmount == 1:
            self.updateAmount(self.niceGuyAmount)
            self.boost = self.after(10000,self.tGBoost)
        else:
            self.after_cancel(self.boost)
            self.updateAmount(self.niceGuyAmount)
            self.boost = self.after(10000,self.tGBoost)
 
    def Rice(self): #this is for the rice to change click amount
        if self.count>=10:
            self.clickAmount += 1
            self.count-=10
            self.label.config(text="Pounds: " + str(self.count))
        else:
            self.punishment()
    def Prestige(self): #prestige stuff. changes everything back to normal
        if self.prestigeNum == 0:
 
 
            if self.count >= 1000000:
                self.clickAmount = 1
                self.count = 0
                self.niceGuyAmount = 0
                self.prestigeNum+=1
                self.label.config(text="Pounds: " + str(self.count))
                self.prestigeLabel = Label(self, text = "Prestige: 1",font = "Helvetica 15")
                self.prestigeLabel.place(x=750,y=0)
                self.prestigeLabel.config(bg = "#FFD700")
 
 
 
            else:
                self.punishment()
 
 
 
        else:
 
 
            if self.count >= 1000000:
                self.clickAmount = 1
                self.count = 0
                self.niceGuyAmount = 0
                self.prestigeNum+=1
                self.label.config(text="Pounds: " + str(self.count))
                self.prestigeLabel.config(text = "Prestige: " + str(self.prestigeNum))
 
 
 
            else:
                self.punishment()
    def goBack(self): #goes back to maain window
        self.destroy()
        startMW()
 
class ageCalc(tk.Tk): #age calculator
    def __init__(self):
        #intializes the code, creates assorted labels, entries, and buttons to get data
        super().__init__()
        self.geometry("500x500")
        self.configure(bg = "BLACK")
        self.titLab = Label(self, text = "Age Calculator", font = 'Helvetica 24', bg = BLACK, fg = WHITE).place(relx=.5, rely=.1, anchor = CENTER)
       
        self.yearLab = Label(self, text = "Year Born: ", font = "Helvetica 16", bg = BLACK, fg = WHITE)
        self.yearLab.place(relx=.2, rely=.3, anchor = CENTER)
        self.yearSV = StringVar()
        self.yearEntry = Entry(self, width = 10, font = "Helvetica 16", textvariable = self.yearSV)
        self.yearEntry.place(relx=.5, rely=.3, anchor = CENTER)
 
        self.monthLab = Label(self, text = "Month Born: ", font = "Helvetica 16", bg = BLACK, fg = WHITE)
        self.monthLab.place(relx=.2, rely=.4, anchor = CENTER)
        self.monthSV = StringVar()
        self.monthEntry = Entry(self, width = 10, font = "Helvetica 16", textvariable = self.monthSV)
        self.monthEntry.place(relx=.5, rely=.4, anchor = CENTER)
 
        self.dayLab = Label(self, text = "Day Born: ", font = "Helvetica 16", bg = BLACK, fg = WHITE)
        self.dayLab.place(relx=.2, rely=.5, anchor = CENTER)        
        self.daySV = StringVar()
        self.dayEntry = Entry(self, width = 10, font = "Helvetica 16", textvariable = self.daySV)
        self.dayEntry.place(relx=.5, rely=.5, anchor = CENTER)
 
        self.continueButt = Button(self, text = "Move On", font = "Helvetica 16", bg = BLACK, fg = WHITE, command = self.continueOn)
        self.continueButt.place(relx=.5, rely=.7, anchor = CENTER)
        self.goBackButt = Button(self, text = "Go Back", font = "Helvetica 12", bg = BLACK, fg = WHITE, command = lambda: self.goBack()).place(relx=.85, rely=.05)
 
    def goBack(self): #goes back to main window
        self.destroy()
        startMW()
    def continueOn(self): #this will destroy items, then show the age through labels
        self.yearLab.destroy()
        self.yearEntry.destroy()
        self.monthLab.destroy()
        self.monthEntry.destroy()
        self.dayLab.destroy()
        self.dayEntry.destroy()
        self.continueButt.destroy()
        birthday = datetime.date(int(self.yearSV.get()),int(self.monthSV.get()),int(self.daySV.get()))
        now = datetime.date.today()
        delta = now - birthday
        self.daysAgo = delta.days
        self.dayText = Label(self, text = f'You were born {self.daysAgo} days ago.', font = "Helvetica 16", bg = BLACK, fg = WHITE).place(relx=.5,rely=.3, anchor = CENTER)
        self.monthsAgo = round(self.daysAgo/30, 2)
        self.monthsText = Label(self, text = f'You were born {self.monthsAgo} months ago', font = "Helvetica 16", bg = BLACK, fg = WHITE).place(relx=.5, rely=.5, anchor = CENTER)
        self.yearsAgo = round(self.daysAgo/365, 2)
        self.monthsText = Label(self, text = f'You were born {self.yearsAgo} years ago', font = "Helvetica 16", bg = BLACK, fg = WHITE).place(relx=.5, rely=.7, anchor = CENTER)
 
 
 
class mainWindow(tk.Tk): #main window class
    def __init__(self):
        #intializes the different labels and buttons to contiue onwards
        super().__init__()
        self.geometry("600x600")
        self.configure(bg = BLACK)
        self.titLab = Label(self, text = "Organizer", font = "Helvetica 24", bg = BLACK, fg = WHITE).place(relx=.5, rely=.1, anchor = CENTER)
        self.hangmanButt = Button(self, text = "Hangman", font = "Helvetica 16", command = lambda: self.runHangman()).place(relx=.2, rely=.2)
        self.ticTacToeButt = Button(self, text = "Tic Tac Toe", font = "Helvetica 16", command = lambda: self.runTicTacToe()).place(relx=.6, rely=.2)
        self.spotRecButt = Button(self, text = "Song Suggestion", font = "Helvetica 16", command = lambda: self.runSongRec()).place(relx=.15, rely=.5)
        self.ageCalc = Button(self, text = "Age Calculator", font = "Helvetica 16", command = lambda: self.runAgeCalc()).place(relx=.6, rely=.5)
        self.surprise = Button(self, text = "Surprise", font = "Helvetica 16", command = lambda: self.runSurprise()).place(relx=.5, rely=.9, anchor = CENTER)
        self.tweeter = Button(self, text = "Tweeter", font = "Helvetica 16", command = lambda: self.runTweeter()).place(relx=.5, rely=.7, anchor = CENTER)
    #different functions to run different games and apps
    def runHangman(self):
        self.destroy()
        hg = Hangman()
        hg.mainloop()
    def runTicTacToe(self):
        self.destroy()
        ttt = ticTac()
        ttt.mainloop()
    def runSongRec(self):
        self.destroy()
        sR = spotRecommend()
        sR.mainloop()
    def runAgeCalc(self):
        self.destroy()
        aC = ageCalc()
        aC.mainloop()
    def runSurprise(self):
        self.destroy()
        clicker = Clicker()
        clicker.mainloop()
    def runTweeter(self):
        self.destroy()
        tS = tweetSomething()
        tS.mainloop()
 
 
#starts the code
start()