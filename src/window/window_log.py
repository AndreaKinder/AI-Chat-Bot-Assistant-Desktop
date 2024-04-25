import os
import customtkinter as ctk
from src.logs.create_log import capture_log, read_log
from src.src_guides.directory_guide import log_directory


class InputUs(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label_us = ctk.CTkLabel(self, text="User:", width=150)
        self.label_us.grid(row=0, column=0)
        self.entry_new_us = ctk.CTkEntry(self, width=300)
        self.entry_new_us.grid(row=0, column=1)


class InputPasswd(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label_passwd = ctk.CTkLabel(self, text="Password:", width=150)
        self.label_passwd.grid(row=0, column=0)
        self.entry_new_passwd = ctk.CTkEntry(self, show="*", width=300)
        self.entry_new_passwd.grid(row=0, column=1)


class ButtonLog(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, fg_color="#FF9800", text_color="black")
        # The button_action is not used outside of ButtonLog's __init__, consider removing if not needed elsewhere


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