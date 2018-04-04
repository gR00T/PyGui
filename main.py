import tkinter as tk
from tkinter import messagebox
from functools import partial
import random


class GameZone(object):
    """ Class for the Game. Assists with making it easy
        to instantiate new games upon new game requests.
    """
    def __init__(self, event=None):
        # Initializes all tk settings and builds button grid
        self.tracker = 0
        self.root = tk.Tk()
        self.root.title("Guessing Game")
        self.top = tk.Frame(self.root)
        self.top.grid(row="1")
        self.middle = tk.Frame(self.root)
        self.middle.grid(row="2")
        self.bottom = tk.Frame(self.root)
        self.bottom.grid(row="3")
        
        self.topLabel = tk.Label(self.top, text="top")
        self.topLabel.grid()
        
        self.backImageFrame = [tk.PhotoImage(file="data/back.gif",format="gif -index %i" %(i)) for i in range(7)]
        
        self.buttonList = []                                 #holds the list of created buttons
        self.buttonMissList = []                             #hold the button ojbects of missed attempts
        self.randNum = random.randint(0,24)
        self.num = 0

        #for loop that builds the grid off buttons for the game
        for x in range(0,5):
            self.tempList = []
            for y in range(0,5):
                WinnerFunc = partial(self.Winner,x,y)   #enables the passing of arguments
                MissedFunc = partial(self.Missed,x,y)
                #print("x="+str(x)+" y="+str(y))
                if self.num == self.randNum:
                    self.tempList.append(tk.Button(self.middle,
                                                   bg="#89e48a",
                                                   fg="#89e48a",
                                                   activebackground="#89e48a",
                                                   image=self.backImageFrame[0],
                                                   command=WinnerFunc))
                    self.tempList[y].grid(row=x,column=y)
                else:
                    self.tempList.append(tk.Button(self.middle,
                                                   bg="#89e48a",
                                                   fg="#89e48a",
                                                   activebackground="#89e48a",
                                                   image=self.backImageFrame[0],
                                                   command=MissedFunc))
                    self.tempList[y].grid(row=x,column=y)
                self.num += 1
            self.buttonList.append(self.tempList)
        self.quitButton = tk.Button(self.bottom, text="Quit", command=self.QuitButton)
        self.quitButton.grid()

    def Winner(self,x,y):
        """
           Win function that replaces the button image and prompts user if they want
           to play again.
        """
        incMax = 8 
        loop = True 
        speed = 50
        #print(str(x)+","+str(y))
        winPhoto = [tk.PhotoImage(file="data/winner.gif",format="gif -index %i" %(i))for i in range(incMax)]
        self.buttonList[x][y].configure(image=winPhoto[0])
        self.buttonList[x][y].image = winPhoto[0]
        self.root.after(0,self.AnimateButtons,0,speed,x,y,incMax,winPhoto,loop)        
        result = messagebox.askyesno("Message",("You Won after " + str(self.tracker) + " attempt(s).\n Replay?"))
        
        if result:
            self.root.destroy()
            game = GameZone()
        else:
            self.root.destroy() 

    def Missed(self,x,y):
        """
           Function that keeps track of the missed attempts and sends
           a message to let them know they missed. Changes button
           image to an X graphic.
        """
        incMax = 7
        loop = False
        speed = 50
        #print(str(x)+","+str(y))
        missPhoto = [tk.PhotoImage(file="data/fail-x.gif",format="gif -index %i" %(i))for i in range(incMax)]
        self.buttonList[x][y].configure(image=missPhoto[0])
        self.buttonList[x][y].image = missPhoto[0]
        self.buttonMissList.append(self.buttonList[x][y])
        self.root.after(0,self.AnimateButtons,0,speed,x,y,incMax,missPhoto,loop)
        self.tracker += 1
        messagebox.showinfo("Message","You missed")

    def AnimateButtons(self, inc,speed,x,y,incMax,imageArray,loop):
        """
           Iterates through each frame of the buttons animations
        """
             
        if inc < incMax:
            frame = imageArray[inc]
            self.buttonList[x][y].configure(image=frame)
            self.buttonList[x][y].image = frame
            inc+=1
            self.root.after(speed, self.AnimateButtons,inc,speed,x,y,incMax,imageArray,loop) 
        elif loop:
            inc = 0
            self.root.after(speed, self.AnimateButtons,inc,speed,x,y,incMax,imageArray,loop)
        else:
            inc = 0

    def QuitButton(self, event=None):
        self.root.destroy()
        game = GameZone()

game = GameZone()

tk.mainloop()

