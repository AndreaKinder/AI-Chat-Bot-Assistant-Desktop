import tkinter as tk
from tkinter import ttk
import asyncio
import threading
from src.logs.check_log import check_file_log
from src.src_guides.hug_api import chat_init, chat_continue
from src.window.window_log import create_window_log

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
style.configure("My.TButton", background=colors["secondary"], foreground="black", borderwidth=2, padding=10, corner_radius=20)
style.configure("My.TEntry", background=colors["background"], foreground="black", borderwidth=2, padding=10, corner_radius=10)

messages = tk.Text(app, height=20, width=50, bg=colors["background"], fg="black", relief=tk.FLAT, font=("System UI", 10))
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
