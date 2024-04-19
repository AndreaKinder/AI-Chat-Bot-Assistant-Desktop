import tkinter as tk
from tkinter import ttk
import asyncio
import threading
from window_log import create_window_log

# Suponiendo que chat_init y chat_continuo son asíncronos y están definidos en otro lugar
from hug_api import chat_init, chat_continuo

historial = []
capture_id_chat = []


def run_asyncio_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coroutine)
    loop.close()
    return result


def send_question_async(question):
    numero_de_entradas = len(historial)
    print(numero_de_entradas)
    if numero_de_entradas <= 1:
        coroutine = chat_init(mensaje=question)
    elif numero_de_entradas >= 2:
        coroutine = chat_continuo(mensaje=question, id_chat=capture_id_chat[0])

    def callback(result):
        # Asumiendo que result es una tupla (Message, id_chat) para chat_init
        # y solo Message para chat_continuo
        if isinstance(result, tuple):
            # Esto ocurre solo después de chat_init
            message, id_chat = result
            respuesta = message.text  # Accede al texto del mensaje
            if len(capture_id_chat) == 0:  # Si aún no hemos capturado el id_chat, lo hacemos
                capture_id_chat.append(id_chat)
        else:
            # Esto ocurre para chat_continuo
            message = result
            respuesta = message.text  # Accede al texto del mensaje

        messages.insert(tk.END, f"Chatbot: {respuesta}\n\n")
        messages.see(tk.END)

    def run_coroutine():
        result = run_asyncio_coroutine(coroutine)
        app.after(0, callback, result)

    threading.Thread(target=run_coroutine).start()


def send_question():
    question = entry.get().strip()
    if question:
        historial.append(question)
        entry.delete(0, tk.END)
        messages.insert(tk.END, f"Tú: {question}\n")
        send_question_async(question)


# Define la paleta de colores
naranja = "#FFA500"
fucsia = "#FF00FF"
blanco = "#FFFFFF"

app = tk.Tk()
app.title("Chatbot")
app.configure(bg=blanco)

# Establece ezl estilo de los widgets con bordes redondeados
style = ttk.Style()
style.configure("My.TButton", background=fucsia, foreground=blanco, borderwidth=0, padding=10, corner_radius=20)
style.configure("My.TEntry", background=blanco, foreground=naranja, borderwidth=0, padding=10, corner_radius=10)

messages = tk.Text(app, height=20, width=50, bg=blanco, fg=naranja, borderwidth=0, relief=tk.FLAT)
messages.pack(padx=20, pady=20)

# Campo de entrada para escribir las preguntas
entry = ttk.Entry(app, style="My.TEntry")
entry.pack(pady=10)
entry.focus()  # Pone el foco en el campo de entrada al iniciar la aplicación

# Botón para enviar la pregunta
send_button = ttk.Button(app, text="Enviar Pregunta", command=send_question, style="My.TButton")
send_button.pack()
log_button = ttk.Button(app, text="Abrir Ventana de Log", command=create_window_log, style="My.TButton")
log_button.pack(pady=10)


def main_window():
    app.mainloop()
