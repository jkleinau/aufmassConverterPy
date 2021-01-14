import tkinter.filedialog
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile

import main
from magicPlanAPI import MagicPlanAPI, write_file_from_url


class GUI:

    def __init__(self):
        self.magic_plan_api = MagicPlanAPI()
        self.plans = dict()
        self.fenster = Tk()
        self.api_import_checker = False
        self.xml = StringVar()
        self.fenster.title("Aufmass Converter")
        self.import_path = StringVar()
        self.export_path = StringVar()
        self.username = StringVar()
        self.fenster.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.icon_path = "resources/data/icon/holding_favicon_300x300_cpz_icon.ico"

        self.fenster.iconbitmap(self.icon_path)

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

    def button_action_convert(self):
        magic_id = [plan for plan in self.plans if self.plans[plan] == self.import_path.get().split('/')[-1]]
        self.xml = self.magic_plan_api.get_project_plan(magic_id[0])
        # main.save_to_file(self, self.import_path.get().split('/')[-1])

        # saving Report to file
        files = self.magic_plan_api.get_files_by_plan(magic_id, filetype='pdf')
        if len(files) == 1:
            directory = self.export_path.get().removesuffix(self.export_path.get().split('/')[-1])
            write_file_from_url(list(files.values())[-1], str(directory) + list(files.keys())[-1])

        main.convert_to_xml(param_data=self.xml, api=self.api_import_checker, export_path=str(self.export_path.get()))
        tkinter.messagebox.showinfo("Convert", "Die Datei wurde erfolgreich umgewandelt.")

    def button_action_import(self):
        name = tkinter.filedialog.askopenfile()
        self.import_path.set(name.name)
        self.api_import_checker = False

    def button_action_export(self):
        name = asksaveasfile(mode='w', initialfile="AUFMASS-" + str(datetime.now().date()) + ".xml",
                             title="Save as")
        self.export_path.set(name.name)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            main.dataCentre.save_data()
            self.fenster.destroy()

    def login_check(self):
        user_label = Label(self.fenster, text=self.username_entry.get(), anchor=E)
        user_label.place(x=525, y=160, width=85, height=30)
        self.login.destroy()

    def setup_login(self):
        self.login = Tk()
        self.login.title("Login")
        self.login.iconbitmap(self.icon_path)
        self.login.resizable = False

        # username label and text entry box
        usernameLabel = Label(self.login, text="User Name:").grid(row=0, column=0, sticky=E, padx=5, pady=5)

        self.username_entry = Entry(self.login, textvariable=self.username)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

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
        self.api_select.iconbitmap(self.icon_path)
        self.search_term = StringVar()

        # Initializing widgets
        search_button = Button(self.api_select, text='Search', command=lambda: self.get_searched_list())
        self.search_box = Entry(self.api_select, textvariable=self.search_term)
        scrollbar = Scrollbar(self.api_select, orient=VERTICAL)
        self.listbox = Listbox(self.api_select, yscrollcommand=scrollbar.set, selectmode=BROWSE)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.config(font=20)
        browse_button = Button(self.api_select, text="Reload", command=lambda: self.reload_projects())
        select_button = Button(self.api_select, text="Select", command=lambda: self.select_project())

        # self.fenster.bind('<Return>', self.click())
        # Place the all widgets
        self.search_box.place(x=5, y=50, width=365, height=20)
        scrollbar.place(x=430, y=70, width=20, height=480)
        self.listbox.place(x=0, y=70, width=430, height=480)
        browse_button.place(x=5, y=5, width=100, height=30)
        select_button.place(x=345, y=5, width=100, height=30)
        search_button.place(x=370, y=50, width=80, height=20)

        self.search_box.bind('<Return>', self.click())

        self.load_projects()

    def click(self):
        print("You clicked")

    def get_searched_list(self):
        self.search_term.set(self.search_box.get())
        selection = main.dataCentre.get_search_plans(search=self.search_term.get())
        self.listbox.delete(0, END)
        self.show_plans(selection)

    def button_action_import_api(self):
        self.setup_api_select()

    def show_plans(self, plans):
        self.plans = plans

        for plan in self.plans:
            self.listbox.insert(END, str(self.plans[plan]))

    def load_projects(self):
        self.listbox.delete(0, END)
        self.plans = main.dataCentre.get_plans()
        self.show_plans(self.plans)

    def select_project(self):
        self.import_path.set("API/" + self.listbox.get(ANCHOR))
        self.api_select.destroy()
        self.api_import_checker = True

    def reload_projects(self):
        self.plans = main.dataCentre.reload_plans()
        self.load_projects()
