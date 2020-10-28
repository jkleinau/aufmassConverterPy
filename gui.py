from tkinter import *

fenster = Tk()

fenster.title("Aufmass Converter")


def button_action():
    anweisungs_label.config(text="Ich wurde geändert!")


change_button = Button(fenster, text="Ändern", command=button_action)
exit_button = Button(fenster, text="Beenden", command=fenster.quit)

anweisungs_label = Label(fenster, text="Ich bin eine Anweisung:\n\
Klicke auf 'Ändern'.")

info_label = Label(fenster, text="Ich bin eine Info:\n\
Der Beenden Button schliesst das Programm.")
anweisungs_label.pack(side=LEFT)
change_button.pack(side=LEFT)
info_label.pack(side=LEFT)
exit_button.pack(side=LEFT)


fenster.mainloop()