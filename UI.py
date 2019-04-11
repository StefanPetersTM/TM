from tkinter import *
from tkinter import filedialog
#import ObjectRecognition.py

import cv2 as cv
import argparse
import sys
import numpy as np
import os.path

# Initialize the parameters
confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4   #Non-maximum suppression threshold
inpWidth = 416       #Width of network's input image
inpHeight = 416      #Height of network's input image

def objrec():

window = Tk()
window.title("Simple UI")
window.geometry('250x100')
lbl = Label(window, text="Hello World!")
lbl.grid(column=0, row=0)


def clicked():
    lbl.configure(text="Please select an image/video to be processed")

    button1 = Button(window, text=u"Choose a file", command=loadfile)
    button1.grid(column=0, row=1, sticky="ew", columnspan=1)
    button3 = Button(window, text=u"Click to begin analysis", command=objrec)
    button3.grid(column=0, row=3, sticky="ew", columnspan=1)

#def objrec():
#    pass

def exit():
    sys.exit(0)

def loadfile():
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if filename:
            try:
                filename = self.settings["fileChosen"]

            except:
                print ("Selected file is %s" %filename)
                return


btn1 = Button(window, text="Click to start", command=clicked)
btn1.grid(column=0, row=1)

btn2 = Button(window, text="Click to exit", command=exit)
btn2.grid(column=0, row=2)



window.mainloop()

