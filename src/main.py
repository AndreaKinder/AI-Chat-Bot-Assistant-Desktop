import os
import json
import customtkinter as ctk
from hugchat import hugchat
from hugchat.login import Login
import tkinter as tk
from tkinter import ttk
import asyncio
import threading
from openai import OpenAI

Chat_GPT = False

 # Cambio de servicio Chat GPT y HugChat
def change_service(value):
    global Chat_GPT
    if value == "HugChat":
        Chat_GPT = False
        print("HugChat seleccionado:", Chat_GPT)
    else:
        Chat_GPT = True
        print("ChatGPT seleccionado:", Chat_GPT)

folder_name = 'storage'
file_path = os.path.join(folder_name, 'log.json')
file_path_Chat_GPT_API = os.path.join(folder_name, 'log_OpenAPI.json')
capture_id_chat = []


def capture_log_openAPI(openAPI):
    open_api = {'OpenAPI': openAPI}
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    with open(file_path_Chat_GPT_API, 'w') as file:
        json.dump(open_api, file)

def read_log_OpenAI():
    if not os.path.exists(file_path_Chat_GPT_API):
        select_window_log()
    else:
        try:
            with open(file_path_Chat_GPT_API, 'r') as log:
                log_data_openAPI = json.load(log)
                return log_data_openAPI['OpenAPI']
        except json.decoder.JSONDecodeError:
            select_window_log()

def import_ChatGPT(openAPI, text):
    client = OpenAI(api_key=openAPI)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

async def import_text_response_chatGPT(text):
    key_OpenAI = read_log_OpenAI()
    return import_ChatGPT(openAPI=key_OpenAI, text=text)

def check_file_GPT():
    directory = os.path.dirname(file_path_Chat_GPT_API)
    if check_directory(directory):
        check_file_true()
        return True
    else:
        check_file_false()
        select_window_log()
        return False

def capture_log_hug(us, passwd):
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

class InputKeyGPT(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label_key = ctk.CTkLabel(self, text="Key Open AI:", width=150)
        self.label_key.grid(row=0, column=0)
        self.entry_new_key = ctk.CTkEntry(self, width=300)
        self.entry_new_key.grid(row=0, column=1)

class App_log_ChatGPT(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Logging API Key Open AI")
        self.geometry("500x150")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.input_key = InputKeyGPT(master=self)

        def logging():
            new_key = self.input_key.entry_new_key.get()
            capture_log_openAPI(openAPI=new_key)
            self.destroy()
            read_log_OpenAI()

        self.log_button = ButtonLog(master=self, text="Logg In", command=logging)
        self.input_key.grid(row=0)
        self.log_button.grid(row=1)

class App_log_hug(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Logging HugChat")
        self.geometry("500x150")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.input_us = InputUs(master=self)
        self.input_passwd = InputPasswd(master=self)

        def logging():
            new_us = self.input_us.entry_new_us.get()
            new_passwd = self.input_passwd.entry_new_passwd.get()
            capture_log_hug(us=new_us, passwd=new_passwd)
            self.destroy()
            read_log()

        self.log_button = ButtonLog(master=self, text="Logg In", command=logging)
        self.input_us.grid(row=0)
        self.input_passwd.grid(row=1)
        self.log_button.grid(row=2)

def select_window_log():
    if not Chat_GPT:
        app_log = App_log_hug()
        app_log.mainloop()
    else:
        app_log = App_log_ChatGPT()
        app_log.mainloop()

def check_directory(directory):
    return os.path.exists(directory) and os.path.isdir(directory)

def check_file_true():
    print("The directory exists and contains a JSON file.")

def check_file_false():
    print("The directory does not exist or does not contain a JSON file.")

def check_file_log():
    if Chat_GPT == True:
        file_directory = file_path_Chat_GPT_API
    elif Chat_GPT == False:
        file_directory = file_path
    directory = os.path.dirname(file_directory)    
    if check_directory(directory):
        if os.path.isfile(file_directory):
            check_file_true()
            return True
        else:
            check_file_false()
            select_window_log()
            return False
    else:
        check_file_false()
        select_window_log()
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
    if Chat_GPT:
        response = await import_text_response_chatGPT(send)
    else:
        chatbot = create_chatbot()
        print(f"Chat init and send: {send}")
        try:
            if not capture_id_chat:
                new_chat = chatbot.new_conversation()
                capture_id_chat.append(new_chat.id)
            id_chat_capture = capture_id_chat[0]
            response = chatbot.chat(text=send, conversation_id=id_chat_capture)
            print(f"Id_chat: {id_chat_capture}, Response: {response}")
        except Exception as e:
            print(f"Error chat init: {e}")
            response = "Error chat init."
    return response

async def chat_continue(send):
    global capture_id_chat, global_chatbot
    if Chat_GPT:
        response = await import_text_response_chatGPT(send)
    else:
        if global_chatbot is None:
            response = await chat_init(send)
        chatbot = global_chatbot
        if not capture_id_chat:
            capture_id_chat.append("Id does not exist. It should have been captured.")
        id_chat_capture = capture_id_chat[0]
        print(f"Chat continue and send: {send}")
        try:
            response = chatbot.chat(text=send, conversation_id=id_chat_capture)
            print(f"Id_chat: {id_chat_capture}, Response: {response}")
        except Exception as e:
            print(f"Error chat continue: {e}")
            response = "Error chat continue."
    return response

def log_chat(send, response):
    log_file = "storage/log_chat.json"
    log_data = {"send": send, "response": response}

    if not os.path.exists(log_file):
        with open(log_file, "w") as file:
            json.dump([log_data], file, indent=4)
    else:
        with open(log_file, "r") as file:
            logs = json.load(file)
        logs.append(log_data)
        with open(log_file, "w") as file:
            json.dump(logs, file, indent=4)

def handle_send_event(event=None):
    send_message()

def send_message():
    send = entry.get()
    entry.delete(0, tk.END)
    response_text.configure(state=tk.NORMAL)
    response_text.insert(tk.END, f"\n\nUser: {send}")
    response_text.see(tk.END)
    response_text.configure(state=tk.DISABLED)
    
    def process_response():
        if response_text.compare("end-1c", "==", "1.0"):
            response_text.insert(tk.END, f"\n\nUser: {send}")
        asyncio.run(main(send))
    
    threading.Thread(target=process_response).start()

async def main(send):
    check_file_log()
    response = await chat_continue(send=send)
    response_text.configure(state=tk.NORMAL)
    response_text.insert(tk.END, f"\n\nBot: {response}")
    response_text.see(tk.END)
    response_text.configure(state=tk.DISABLED)
    log_chat(send, response)

def clear_chat_log():
    log_file = "storage/log_chat.json"
    if os.path.exists(log_file):
        os.remove(log_file)

clear_chat_log()

root = ctk.CTk()
root.title("Chatbot")
root.geometry("400x600")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

service_frame = ctk.CTkFrame(master=frame)
service_frame.pack(pady=10, padx=10, fill="x", expand=True)

label_service = ctk.CTkLabel(master=service_frame, text="Select Service:")
label_service.pack(side="left", padx=5)

service_var = tk.StringVar(value="HugChat")
service_dropdown = ctk.CTkOptionMenu(master=service_frame, variable=service_var, values=["HugChat", "ChatGPT"], command=change_service)
service_dropdown.pack(side="left", padx=5)

log_button = ctk.CTkButton(master=service_frame, text="Log In", command=select_window_log)
log_button.pack(side="right", padx=5)

response_text = tk.Text(master=frame, wrap="word", state=tk.DISABLED)
response_text.pack(pady=10, padx=10, fill="both", expand=True)

entry_frame = ctk.CTkFrame(master=frame)
entry_frame.pack(pady=10, padx=10, fill="x", expand=True)

entry = ctk.CTkEntry(master=entry_frame)
entry.pack(side="left", pady=10, padx=10, fill="x", expand=True)
entry.bind("<Return>", handle_send_event)

send_button = ctk.CTkButton(master=entry_frame, text="Send", command=send_message)
send_button.pack(side="right", pady=10, padx=10)

root.mainloop()
