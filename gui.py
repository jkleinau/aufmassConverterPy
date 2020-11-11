from datetime import datetime
import tkinter.filedialog
from tkinter.filedialog import asksaveasfile
from tkinter import *
from tkinter import messagebox
from magicPlanAPI import MagicPlanAPI
from main import Main


class GUI:
    def button_action_convert(self):
        main = Main()
        id = [plan['id'] for plan in self.selection if plan['name'] == self.import_path.get().split('/')[-1]]
        self.xml = self.magic_plan_api.get_project_plan(id[0])
        main.convert_to_xml(self)
        tkinter.messagebox.showinfo("Convert", "Die Datei wurde erfolgreich umgewandelt.")

    def button_action_import(self):
        name = tkinter.filedialog.askopenfile()
        self.import_path.set(name.name)

    def button_action_export(self):
        name = asksaveasfile(mode='w', initialfile="AUFMASS-" + str(datetime.now().date()) + ".xml",
                             title="Save as")
        self.export_path.set(name.name)

    def __init__(self):
        self.magic_plan_api = MagicPlanAPI()
        self.selection = dict()
        self.fenster = Tk()
        self.xml = StringVar()
        self.fenster.title("Aufmass Converter")
        self.import_path = StringVar()
        self.export_path = StringVar()
        self.username = StringVar()
        import_textfield = Entry(self.fenster, textvariable=self.import_path, bd=2)
        export_textfield = Entry(self.fenster, textvariable=self.export_path, bd=2)

        account_label = Label(self.fenster, text="Account: ", anchor=E)
        user_label = Label(self.fenster, text="matthias.herzog", anchor=E)

        import_button = Button(self.fenster, text="Import",
                               command=lambda: self.button_action_import())
        import_button_api = Button(self.fenster, text="Import from API",
                                   command=lambda: self.button_action_import_api())
        # login_button = Button(self.fenster, text="Account",command=lambda: self.setup_login())
        export_button = Button(self.fenster, text="Export",
                               command=lambda: self.button_action_export())
        convert_button = Button(self.fenster, text="Convert",
                                command=lambda: self.button_action_convert())

        # Zuerst definieren wir die Grösse des Fensters
        self.fenster.geometry("610x205")

        import_button_api.place(x=15, y=160, width=100, height=30)
        import_button.place(x=15, y=15, width=100, height=50)

        export_button.place(x=15, y=75, width=100, height=50)
        import_textfield.place(x=130, y=25, width=465, height=30)
        export_textfield.place(x=130, y=85, width=465, height=30)
        convert_button.place(x=255, y=160, width=100, height=30)
        # login_button.place(x=360, y=160, width=100, height=30)
        account_label.place(x=400, y=160, width=120, height=30)
        user_label.place(x=510, y=160, width=95, height=30)
        self.fenster.mainloop()

    def login_check(self):
        user_label = Label(self.fenster, text=self.usernameEntry.get(), anchor=E)
        user_label.place(x=525, y=160, width=85, height=30)
        self.login.destroy()

    def setup_login(self):
        self.login = Tk()
        self.login.title("Login")
        self.login.resizable = False

        # username label and text entry box
        usernameLabel = Label(self.login, text="User Name:").grid(row=0, column=0, sticky=E, padx=5, pady=5)

        self.usernameEntry = Entry(self.login, textvariable=self.username)
        self.usernameEntry.grid(row=0, column=1, padx=5, pady=5)
        # password label and password entry box
        passwordLabel = Label(self.login, text="Password:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
        self.password = StringVar()
        passwordEntry = Entry(self.login, textvariable=self.password, show='*').grid(row=1, column=1, padx=5, pady=5)

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
        browse_button = Button(self.api_select, text="Reload", command=lambda: self.reload_projects())
        select_button = Button(self.api_select, text="Select", command=lambda: self.select_project())
        self.load_projects()

        scrollbar.place(x=430, y=50, width=20, height=500)
        self.listbox.place(x=0, y=50, width=430, height=500)
        browse_button.place(x=5, y=5, width=100, height=30)
        select_button.place(x=345, y=5, width=100, height=30)

    def button_action_import_api(self):
        self.setup_api_select()

    def load_projects(self):
        if not self.selection:
            self.reload_projects()
        for project in self.selection:
            self.listbox.insert(END, str(project['name']))

    def select_project(self):
        self.import_path.set("API/" + self.listbox.get(ANCHOR))
        self.api_select.destroy()

    def reload_projects(self):
        self.selection = self.magic_plan_api.get_projects()
