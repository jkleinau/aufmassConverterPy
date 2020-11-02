import tkinter.filedialog
from tkinter import *

from main import convert

fenster = Tk()
fenster.configure(bg='#c0c0c0')
fenster.title("Aufmass Converter")

global import_path
global export_path


def button_action_import():
    name = tkinter.filedialog.askopenfile()
    import_textfield.delete(0, END)
    import_textfield.insert(0, name.name)


def button_action_export():
    name = tkinter.filedialog.askdirectory()
    export_textfield.delete(0, END)
    export_textfield.insert(0, name)


import_button = Button(fenster, text="Import", command=button_action_import)
export_button = Button(fenster, text="Export", command=button_action_export)


def button_action_convert():
    convert()


convert_button = Button(fenster, text="Umwandeln", command=button_action_convert)

import_textfield = Entry(fenster, bd=2)
export_textfield = Entry(fenster, bd=2)

# Zuerst definieren wir die Grösse des Fensters
fenster.geometry("610x205")
# Wir benutzen die absoluten Koordinaten um die Komponenten zu
# setzen und definieren deren Grösse
# anweisungs_label.place(x = 0, y = 0, width=200, height=150)
import_button.place(x=15, y=15, width=100, height=50)
# info_label.place(x = 100, y = 160, width=300, height=100)
export_button.place(x=15, y=75, width=100, height=50)
import_textfield.place(x=130, y=25, width=465, height=30)
export_textfield.place(x=130, y=85, width=465, height=30)
convert_button.place(x=255, y=160, width=100, height=30)

fenster.mainloop()
