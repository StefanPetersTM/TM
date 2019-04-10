from tkinter import *
from tkinter import filedialog
#import ObjectRecognition
#ObjectRecognition.somefunction()


#Creating the window
window = Tk()
window.title("Simple UI")
window.geometry('250x150')
lbl = Label(window, text="Hello World!")
lbl.grid(column=0, row=0)


#Definig all the functions
def clicked():
    lbl.configure(text="The Button has been pressed")

def exit():
    sys.exit(0)

def loadfile():
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if filename:
            try:
                self.settings["fileChosen"] = filename

            except:
                print ("Selected file is %s" %filename)
                return

def start():
        pass


#Making the buttons
btn1 = Button(window, text="Click Me", command=clicked)
btn1.grid(column=0, row=1)

btn2 = Button(window, text="Click to exit", command=exit)
btn2.grid(column=0, row=2)

btn3 = Button(window, text=u"Choose a file", command=loadfile)
btn3.grid(column=0, row=3, sticky="ew", columnspan=1)

btn4 = Button(window, text=u"Start program.", command=start)
btn4.grid(column=0, row=4, sticky="ew", columnspan=1)


window.mainloop()