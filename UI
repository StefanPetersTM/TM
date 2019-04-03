from tkinter import *
from tkinter import filedialog
window = Tk()
window.title("Simple UI")
window.geometry('350x300')
lbl = Label(window, text="Hello World")

lbl.grid(column=0, row=0)




def clicked():
    lbl.configure(text="The Button has been pressed")

def exit():
    sys.exit(0)

def loadfile():
        filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

btn1 = Button(window, text="Click Me", command=clicked)
btn1.grid(column=1, row=0)

btn2 = Button(window, text="Click to exit", command=exit)
btn2.grid(column=1, row=1)

button3 = Button(window, text=u"Choose a file", command=loadfile)
button3.grid(column=0, row=3, sticky="ew", columnspan=2)

window.mainloop()


