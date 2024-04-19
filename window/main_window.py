import tkinter as tk
from tkinter import ttk
import asyncio
import threading

from logs.check_log import check_file_log
from src.hug_api import chat_init, chat_continue
from window.window_log import create_window_log

history = []


def run_asyncio_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coroutine)
    loop.close()
    return result


def send_question_async(question):
    num_entry = len(history)
    print(num_entry)
    if num_entry <= 1:
        coroutine = chat_init(send=question)
    else:
        coroutine = chat_continue(send=question)

    def callback(result):
        message = result
        response = message

        messages.insert(tk.END, f"Chatbot: {response}\n\n")
        messages.see(tk.END)

    def run_coroutine():
        result = run_asyncio_coroutine(coroutine)
        app.after(0, callback, result)

    threading.Thread(target=run_coroutine).start()


def send_question():
    boolean_check_log = check_file_log()
    if boolean_check_log:
        question = entry.get().strip()
        if question:
            history.append(question)
            entry.delete(0, tk.END)
            messages.insert(tk.END, f"Tú: {question}\n")
            send_question_async(question)


orange = "#F25022"
fucsia = "#FF00FF"
black = "#000000"
white = "#FFFFFF"

app = tk.Tk()
app.title("Chatbot")
app.configure(bg=orange)

style = ttk.Style()
style.configure("My.TButton", background=fucsia, foreground=white, borderwidth=2, padding=10, corner_radius=20)
style.configure("My.TEntry", background=orange, foreground=black, borderwidth=2, padding=10, corner_radius=10)

messages = tk.Text(app, height=20, width=50, bg=white, fg=black, borderwidth=0, relief=tk.FLAT)
messages.pack(padx=20, pady=20)

entry = ttk.Entry(app, style="My.TEntry", width=40)
entry.pack(pady=10)
entry.focus()

send_button = ttk.Button(app, text="Send", command=send_question, style="My.TButton")
send_button.pack(pady=5)
log_button = ttk.Button(app, text="Logging", command=create_window_log, style="My.TButton")
log_button.pack(pady=10)


def main_window():
    app.mainloop()
