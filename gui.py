import tkinter.filedialog
from tkinter import *
import time
import main


class GUI:
    def button_action_convert(self):
        convert_to_xml(self)

    def button_action_import(self):
        name = tkinter.filedialog.askopenfile()
        self.import_textfield.delete(0, END)
        self.import_textfield.insert(0, name.name)

    def button_action_export(self):
        name = tkinter.filedialog.askdirectory()
        self.export_textfield.delete(0, END)
        self.export_textfield.insert(0, name)

    def main(self):
        self.fenster = Tk()
        self.fenster.configure(bg='#c0c0c0')
        self.fenster.title("Aufmass Converter")
        self.import_textfield = Entry(self.fenster, bd=2)
        self.export_textfield = Entry(self.fenster, bd=2)

        self.import_button = Button(self.fenster, text="Import",
                                    command=lambda: self.button_action_import())
        self.export_button = Button(self.fenster, text="Export",
                                    command=lambda: self.button_action_export())
        self.convert_button = Button(self.fenster, text="Umwandeln",
                                     command=lambda: self.button_action_convert())
        # Zuerst definieren wir die Grösse des Fensters
        self.fenster.geometry("610x205")
        # Wir benutzen die absoluten Koordinaten um die Komponenten zu
        # setzen und definieren deren Grösse
        # anweisungs_label.place(x = 0, y = 0, width=200, height=150)
        self.import_button.place(x=15, y=15, width=100, height=50)
        # info_label.place(x = 100, y = 160, width=300, height=100)
        self.export_button.place(x=15, y=75, width=100, height=50)
        self.import_textfield.place(x=130, y=25, width=465, height=30)
        self.export_textfield.place(x=130, y=85, width=465, height=30)
        self.convert_button.place(x=255, y=160, width=100, height=30)

        self.fenster.mainloop()

    def __init__(self):
        self.setup_login()

    def login_check(self):
        self.login.destroy()
        self.main()

    def setup_login(self):
        self.login = Tk()
        self.login.title("Login")
        self.login.resizable = False
        # username label and text entry box
        usernameLabel = Label(self.login, text="User Name:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
        username = StringVar()
        usernameEntry = Entry(self.login, textvariable=username).grid(row=0, column=1, padx=5, pady=5)

        # password label and password entry box
        passwordLabel = Label(self.login, text="Password:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
        password = StringVar()
        passwordEntry = Entry(self.login, textvariable=password, show='*').grid(row=1, column=1, padx=5, pady=5)

        # login button
        loginButton = Button(self.login, text="Login", command=self.login_check).grid(row=4, column=0, sticky=N,
                                                                                      columnspan=2, padx=5, pady=10)

        self.login.mainloop()
