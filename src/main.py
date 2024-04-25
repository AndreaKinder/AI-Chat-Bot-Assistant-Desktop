import os
import json
import customtkinter as ctk
from hugchat import hugchat
from hugchat.login import Login
import tkinter as tk
from tkinter import ttk
import asyncio
import threading

folder_name = 'storage'

file_path: str = os.path.join(folder_name, 'log.json')

capture_id_chat = []


def capture_log(us, passwd):
    data = {'us': us, 'passwd': passwd}
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    with open(file_path, 'w') as file:
        json.dump(data, file)


def read_log():
    with open(file_path, 'r') as log:
        log_data = json.load(log)
        return log_data['us'], log_data['passwd']


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
    if os.path.exists(file_path):
        os.remove(file_path)
    app_log = App()
    app_log.mainloop()


def check_directory(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        return True
    else:
        return False


def check_file_true():
    print("The directory exists and contains a JSON file.")


def check_file_false():
    print("The directory does not exist or does not contain a JSON file.")


def check_file_log():
    directory = os.path.dirname(file_path)
    if check_directory(directory):
        if os.path.isfile(file_path):
            check_file_true()
            return True
        else:
            check_file_false()
            create_window_log()
            return False
    else:
        check_file_false()
        create_window_log()
        return False


def import_log():
    if check_file_log():
        email, passwd = read_log()
        return email, passwd
    else:
        print("No file log.json")
        return None, None


def create_cookies():
    EMAIL, PASSWD = import_log()
    cookie_path_dir = "./storage/"
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    return cookies


def capture_id_chat_id(id_chat):
    if not capture_id_chat:
        capture_id_chat.append(id_chat)
    return capture_id_chat


global_chatbot = None


def create_chatbot():
    global global_chatbot
    if global_chatbot is None:
        cookies = create_cookies()
        global_chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        new_chat = global_chatbot.new_conversation()
        new_id = new_chat.id
        capture_id_chat_id(id_chat=new_id)
    return global_chatbot


async def chat_init(send):
    global capture_id_chat
    chatbot = create_chatbot()
    print(f"Chat init and send: {send}")
    try:
        if not capture_id_chat:
            new_chat = chatbot.new_conversation()
            capture_id_chat.append(new_chat.id)
        id_chat_capture = capture_id_chat[0]
        query_result = chatbot.chat(text=send, conversation_id=id_chat_capture)
        print(f"Id_chat: {id_chat_capture}, Response: {query_result}")
        return query_result
    except Exception as e:
        print(f"Error chat init: {e}")
        return "Error chat init."


async def chat_continue(send):
    global capture_id_chat, global_chatbot
    chatbot = global_chatbot
    if chatbot is None:
        print("El chatbot no init.")
        return "El chatbot no init."

    if not capture_id_chat:
        print("Chat_id not found")
        return "Chat_id not found."
    id_chat_capture = capture_id_chat[0]
    try:
        print(f"Continue chat and send: {send}, {id_chat_capture}")
        query_result = chatbot.chat(text=send, conversation_id=id_chat_capture)
        print(f"Response: {query_result}")
        return query_result
    except Exception as e:
        print(f"Error continue chat: {e}")
        return "Error continue chat."


def chat_end():
    if import_log() is not None:
        create_chatbot().delete_all_conversations()


history = []
answer_color = 'green'


def run_asyncio_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coroutine)
    loop.close()
    return result


def send_question_async(question):
    num_entry = len(history)
    coroutine = chat_init(send=question) if num_entry <= 1 else chat_continue(send=question)

    def callback(result):
        messages.insert(tk.END, f"Chatbot: {result}\n\n", 'answer_tag')
        messages.tag_configure('answer_tag', foreground=answer_color)
        messages.see(tk.END)

    def run_coroutine():
        result = run_asyncio_coroutine(coroutine)
        app.after(0, callback, result)

    threading.Thread(target=run_coroutine).start()


def clear_chat():
    messages.delete(1.0, tk.END)
    history.clear()


def send_question(event=None):
    if check_file_log():
        question = entry.get().strip()
        if question:
            history.append(question)
            entry.delete(0, tk.END)
            messages.insert(tk.END, f"You: {question}\n")
            send_question_async(question)


colors = {
    "primary": "#2196F3",
    "secondary": "#FF9800",
    "background": "#FFFFFF",
    "text": "#333333",
    "accent": "#EEEEEE"
}

fonts = {
    "main": "Roboto",
    "secondary": "Open Sans"
}

app = tk.Tk()
app.title("Chatbot")

style = ttk.Style()
style.configure("My.TButton", background=colors["secondary"], foreground="black", borderwidth=2, padding=10,
                corner_radius=20)
style.configure("My.TEntry", background=colors["background"], foreground="black", borderwidth=2, padding=10,
                corner_radius=10)

messages = tk.Text(app, height=20, width=50, bg=colors["background"], fg="black", relief=tk.FLAT,
                   font=("System UI", 10))
messages.pack(padx=20, pady=20)

entry_send_frame = ttk.Frame(app)
entry_send_frame.pack(pady=10)

entry = ttk.Entry(entry_send_frame, style="My.TEntry", width=30)
entry.grid(row=0, column=0, padx=(0, 10))
entry.bind("<Return>", send_question)

send_button = ttk.Button(entry_send_frame, text="Send", command=send_question, style="My.TButton")
send_button.grid(row=0, column=1)

entry.focus()

buttons_frame = ttk.Frame(app)
buttons_frame.pack(pady=10)

log_button = ttk.Button(buttons_frame, text="Logging", command=create_window_log, style="My.TButton")
log_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(buttons_frame, text="Clear", command=clear_chat, style="My.TButton")
clear_button.pack(side=tk.LEFT, padx=5)


def main_window():
    app.mainloop()


if __name__ == '__main__':
    main_window()
