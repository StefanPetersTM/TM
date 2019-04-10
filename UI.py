from tkinter import *
from tkinter import filedialog
import ObjectRecognition.py

window = Tk()
window.title("Simple UI")
window.geometry('250x100')
lbl = Label(window, text="Hello World!")
lbl.grid(column=0, row=0)


def clicked():
    lbl.configure(text="Please select an image/video to be processed")

    button1 = Button(window, text=u"Choose a file", command=loadfile)
    button1.grid(column=0, row=1, sticky="ew", columnspan=1)

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


