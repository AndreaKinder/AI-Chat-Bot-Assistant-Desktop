import os

import customtkinter as ctk
from logs.create_log import capture_log
from logs.create_log import read_log
from src.directory_guide import log_directory


class InputUs(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label_us = ctk.CTkLabel(self, text="Usuario:", width=150)
        self.label_us.grid(row=0, column=0)

        self.entry_new_us = ctk.CTkEntry(self, width=300)
        self.entry_new_us.grid(row=0, column=1)


class InputPasswd(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label_passwd = ctk.CTkLabel(self, text="Contraseña:", width=150)
        self.label_passwd.grid(row=0, column=0)

        self.entry_new_passwd = ctk.CTkEntry(self, show="*", width=300)
        self.entry_new_passwd.grid(row=0, column=1)


class ButtonLog(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.button_action = ctk.CTkButton(self, width=20)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Logging")
        self.geometry("500x150")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.input_us = InputUs(master=self)
        self.input_passwd = InputPasswd(master=self)

        def logging():
            new_us = self.input_us.entry_new_us.get()
            new_passwd = self.input_passwd.entry_new_passwd.get()
            capture_log(us=new_us, passwd=new_passwd)
            self.destroy()
            read_log()

        self.log_button = ButtonLog(master=self, text="Logg In", command=logging)

        self.input_us.grid(row=0)
        self.input_passwd.grid(row=1)
        self.log_button.grid(row=2)


def create_window_log():
    file_path = log_directory()
    if os.path.exists(file_path):
        os.remove(file_path)
    app = App()
    app.mainloop()