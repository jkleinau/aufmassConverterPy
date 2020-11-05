import tkinter.filedialog
from tkinter import *
import time
import main
import random

from main import convert_to_xml


class GUI:
    def button_action_convert(self):
        convert_to_xml(self)

    def button_action_import(self):
        name = tkinter.filedialog.askopenfile()
        self.import_path.set(name.name)

    def button_action_export(self):
        name = tkinter.filedialog.askdirectory()
        self.export_path.set(name)

    def main(self):
        self.fenster = Tk()
        self.fenster.title("Aufmass Converter")
        self.import_path = StringVar()
        self.export_path = StringVar()
        import_textfield = Entry(self.fenster, textvariable=self.import_path, bd=2)
        export_textfield = Entry(self.fenster, textvariable=self.export_path, bd=2)

        import_button = Button(self.fenster, text="Import",
                                    command=lambda: self.button_action_import())
        import_button_api = Button(self.fenster, text="Import from API",
                                        command=lambda: self.button_action_import_api())
        export_button = Button(self.fenster, text="Export",
                                    command=lambda: self.button_action_export())
        convert_button = Button(self.fenster, text="Umwandeln",
                                     command=lambda: self.button_action_convert())
        # Zuerst definieren wir die Grösse des Fensters
        self.fenster.geometry("610x205")
        # Wir benutzen die absoluten Koordinaten um die Komponenten zu
        # setzen und definieren deren Grösse
        # anweisungs_label.place(x = 0, y = 0, width=200, height=150)
        import_button_api.place(x=15, y=160, width=100, height=30)
        import_button.place(x=15, y=15, width=100, height=50)
        # info_label.place(x = 100, y = 160, width=300, height=100)
        export_button.place(x=15, y=75, width=100, height=50)
        import_textfield.place(x=130, y=25, width=465, height=30)
        export_textfield.place(x=130, y=85, width=465, height=30)
        convert_button.place(x=255, y=160, width=100, height=30)

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

    def setup_api_select(self):
        self.api_select = Tk()
        self.api_select.title("Select Projekt")
        self.api_select.geometry("450x550")

        scrollbar = Scrollbar(self.api_select, orient=VERTICAL)
        self.listbox = Listbox(self.api_select, yscrollcommand=scrollbar.set, selectmode=BROWSE)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.config(font=20)
        browse_button = Button(self.api_select, text="Reload", command=lambda: self.load_projects())
        select_button = Button(self.api_select, text="Select", command=lambda: self.select_project())
        self.load_projects()

        scrollbar.place(x=430, y=50, width=20, height=500)
        self.listbox.place(x=0, y=50, width=430, height=500)
        browse_button.place(x=5, y=5, width=100, height=30)
        select_button.place(x=345, y=5, width=100, height=30)

    def button_action_import_api(self):
        self.setup_api_select()
        pass

    def load_projects(self):
        projects = [
            "Ruhlachplatz 14b",
            "Albin - Edelmann - St. 87c",
            "Im Bruch 62c",
            "Emil - Nolde - Str. 960",
            "Salamanderweg 19a",
            "Kolpingstr. 81",
            "Gustav - Heinemann - Str. 608",
            "Mühlenweg 4",
            "Nobelstr. 4",
            "Oskar - Moll - Str. 49",
            "Karl - Krekeler - Str. 62c",
            "Julius - Doms - Str. 434",
            "Heinrich - Lützenkirchen - Weg 44a",
            "Am Thelenhof 34b",
            "Bernhard - Lichtenberg - Str. 51b", " Apt. 725",
            "Auf dem Bruch 044",
            "Bracknellstr. 15a",
            "In der Hartmannswiese 622",
            "Rudolf - Stracke - Str. 36",
            "Carl - Duisberg - Str. 66a",
            "Ringstr. 36c", " 2 OG",
            "Leichlinger Str. 7",
            "Friesenweg 11b",
            "Teltower Str. 27c",
            "Werkstättenstr. 5",
            "Fritz - Henseler - Str. 3",
            "Carl - Rumpff - Str. 15c",
            "Van\'t-Hoff-Str. 77a",
        ]
        selection = random.choices(projects, k=6)
        for project in selection:
            self.listbox.insert(END, str(project))

    def select_project(self):
        self.import_path.set("API/" + self.listbox.get(ANCHOR))
        self.api_select.destroy()
